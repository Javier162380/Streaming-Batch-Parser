import typing
import operator
import gc
import sys
import os
import concurrent.futures
import queue
import shutil
import multiprocessing

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base import BaseParser


def clean_message(message: str) -> typing.List:

    return message.replace('\n', '').split(' ')


def process_events_batch(batch: typing.List, target_host: str) -> typing.Dict:

    host_analysis = {
        "host_counter": {},
        "input_host": [],
        "output_host": []
    }

    for raw_message in batch:
        _, input_host, output_host = clean_message(raw_message)

        if input_host == target_host:
            host_analysis["input_host"].append(output_host)

        if output_host == target_host:
            host_analysis["output_host"].append(input_host)

        if input_host not in host_analysis["host_counter"]:
            host_analysis["host_counter"][input_host] = 1
        else:
            host_analysis["host_counter"][input_host] = host_analysis["host_counter"][input_host] + 1

    return host_analysis


class StreamingParser(BaseParser):

    QUEUE = queue.Queue()

    def __init__(self,
                 logger,
                 queue_size: int,
                 host_name: str,
                 time: int,
                 target_directory: str,
                 batch_size: int,
                 **kwargs):
        """Main interface for processing hosts in a streaming model.

        Args:
            logger: Logging instance
            qeue_size (int): Size of messages that can be push to the qeueu
            host_name (str): Host name we are looking at
            time (int):
            target_directory (str): Directory where files to be processed arrived.append()
            batch_size (int): Micro-batch size.
        """
        self.queue_size = queue_size
        self.host_name = host_name
        self.time = time
        self.batch_size = batch_size
        self.target_directory = target_directory
        self.logger = logger
        self.host_aggregate = {}
        self.hostnames_received = set()
        self.hostnames_connected = set()

    @property
    def processed_directory(self):
        return f"{self.target_directory}/processed"

    @staticmethod
    def process_messages(
            queue,
            event,
            target_directory: str,
            processed_directory: str,
            target_host: str,
            batch_size: int,
            logger):

        logger.info("Processing thread is Active!")
        while not queue.full():
            logger.debug(f"Analyzing files in directory {target_directory}")
            for targetfile in os.listdir(target_directory):
                batch_chunk = []
                if targetfile.endswith('.txt'):
                    with open(f"{target_directory}/{targetfile}") as f:
                        logger.info(f"Processing file {target_directory}/{targetfile}")
                        while chunk := f.readline():
                            if len(batch_chunk) == batch_size:

                                host_analysis = process_events_batch(batch_chunk, target_host)
                                logger.debug(f"Adding a chunk: {host_analysis} to the queue")
                                queue.put(host_analysis, block=True)
                                batch_chunk = []
                                gc.collect()

                            batch_chunk.append(chunk)

                    logger.info(f"File {target_directory}/{targetfile} proccessed")
                    shutil.move(f"{target_directory}/{targetfile}", processed_directory)
                    logger.info(f"File {target_directory}/{targetfile} moved to {processed_directory}")

        logger.info(f"Queue is full releasing the main event")
        event.set()

    @staticmethod
    def aggregate_hosts(host_aggregate: typing.Dict, host_counter: typing.Dict):

        for host in host_counter:
            if host in host_aggregate:
                host_aggregate[host] = host_aggregate[host] + host_counter[host]

            else:
                host_aggregate[host] = host_counter[host]

    @staticmethod
    def aggregate_target_host_connections(target_host_connections: typing.Set, hosts_connected: typing.List):
        for host in hosts_connected:
            target_host_connections.add(host)

    @staticmethod
    def get_higher_host(hosts: typing.Dict) -> typing.List:

        if hosts:
            return max(hosts.items(), key=operator.itemgetter(1))

    def setup(self):

        StreamingParser.QUEUE.maxsize = self.queue_size
        os.makedirs(self.processed_directory, exist_ok=True)

    def results_printer(self, higher_host: typing.List, hostnames_received: typing.Dict,
                        hostnames_connected: typing.Dict):
        print("#####################################################")
        print("#####################################################")
        print("\n")

        if higher_host:
            print(f"The target host {self.host_name}:\n"
                  f"received this connections in the last {self.time} seconds \n"
                  f"{' ,'.join(hostnames_received)}")

            print(f"The target host {self.host_name}:\n"
                  f"was connected to this hosts in the last {self.time} seconds\n"
                  f"{' ,'.join(hostnames_connected)}")

            print(f"The host that received more connections in the last {self.time}\n"
                  f"it is the host {higher_host[0]} with {higher_host[1]} connections\n")

        else:
            print(f"New Hosts where not processed in the last {self.time} seconds")

    def execute(self):

        self.logger.info("Creating the setup for the streaming application")
        self.setup()
        self.logger.info("Setup was succesfull")

        manager = multiprocessing.Manager()
        event = manager.Event()

        with concurrent.futures.ThreadPoolExecutor(1) as worker:
            while True:
                queue_future = {worker.submit(self.process_messages, StreamingParser.QUEUE, event,
                                              self.target_directory, self.processed_directory,
                                              self.host_name, self.batch_size,
                                              self.logger)}
                self.logger.info("Future submit sleeping the main thread")
                event.wait(self.time)
                self.logger.info("Main thread released analyzing queue messages")

                for index in range(StreamingParser.QUEUE.qsize()):
                    message = StreamingParser.QUEUE.get()
                    if message["host_counter"]:
                        self.aggregate_hosts(self.host_aggregate, message["host_counter"])
                    if message["input_host"]:
                        self.aggregate_target_host_connections(self.hostnames_received, message["input_host"])
                    if message["output_host"]:
                        self.aggregate_target_host_connections(
                            self.hostnames_connected, message["output_host"])

                higher_host = self.get_higher_host(hosts=self.host_aggregate)

                self.results_printer(higher_host, self.hostnames_received, self.hostnames_connected)

                self.host_aggregate = {}
                self.hostnames_received = {}
                self.hostnames_connected = {}
                gc.collect()

                self.logger.info("Host processed releasing the main thread")
                event.clear()
