import typing
import gc
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base import BaseParser


class BatchParser(BaseParser):

    def __init__(self,
                 logger,
                 start_time: int,
                 end_time: int,
                 file_path: str,
                 host_name: str,
                 batch_size: int,
                 **kwargs):
        """Main interface for processing hosts in a batch mode.

        Args:
            logger: Logging instance.
            start_time (int): Start time we are looking for in unix time.
            end_time (int): End time we are looking for in unix time
            file_path (str): File path where the file is located.
            host_name (str): Host name we are looking at.
            batch_size (int): Batch size for proccessing the file path in micro batches.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.file_path = file_path
        self.host_name = host_name
        self.batch_size = batch_size
        self.logger = logger

    @staticmethod
    def process_file_per_batches(file_path: str, batch_size: int) -> typing.Iterable:
        batch_chunk = []
        with open(file_path) as f:
            while chunk := f.readline():
                if len(batch_chunk) == batch_size:
                    yield batch_chunk
                    batch_chunk = []
                    gc.collect()

                batch_chunk.append(chunk)

            yield batch_chunk

    @staticmethod
    def clean_host(host: str) -> str:
        return host.replace("\n", "")

    @staticmethod
    def analyze_batch(batch: typing.List) -> typing.Dict:
        end_batch_time = int(batch[-1].split(' ')[0])
        pivot = int(len(batch) / 2)
        middle_batch_time = int(batch[pivot].split(' ')[0])
        start_batch_time = int(batch[0].split(' ')[0])

        return {"end_batch_time": end_batch_time,
                "middle_batch_time": middle_batch_time,
                "start_batch_time": start_batch_time,
                "pivot": pivot}

    def process_hosts(self, batch) -> typing.List:

        connected_host = []

        for connection in batch:
            connection_time, input_host, output_host = connection.split(' ')
            if input_host == self.host_name and self.start_time <= int(connection_time) <= self.end_time:
                connected_host.append(self.clean_host(output_host))

        return connected_host

    def process_batch(self, batch: typing.List, batch_analysis: typing.Dict) -> typing.List:

        if self.end_time >= batch_analysis["middle_batch_time"] > self.start_time:
            return self.process_hosts(batch)
        if batch_analysis["middle_batch_time"] >= self.end_time:
            return self.process_hosts(batch[:batch_analysis["pivot"]])

        if self.start_time >= batch_analysis["middle_batch_time"]:
            return self.process_hosts(batch[batch_analysis["pivot"]:])

    def execute(self):

        host_names = []
        self.logger.info(f"processing  file {self.file_path}")
        for batch in self.process_file_per_batches(file_path=self.file_path, batch_size=self.batch_size):
            batch_analysis = self.analyze_batch(batch)
            self.logger.debug(f"Batch analysis {batch_analysis}")
            if self.start_time > batch_analysis["end_batch_time"]:
                self.logger.info(f"Batch not analyze:"
                                 f"batch end_time: {batch_analysis['end_batch_time']}"
                                 f"target start_time: {self.start_time}")
                continue
            if self.end_time < batch_analysis["start_batch_time"]:
                self.logger.info("Interval already proccessed exiting the loop")
                break

            host_connected = self.process_batch(batch, batch_analysis)
            self.logger.info("Batch processed succesfully")
            self.logger.debug(f"Batch results {host_connected}")
            if host_connected:
                host_names.extend(host_connected)
        print("###################"
              "###################"
              "###################")
        print("\n")
        print(f"Hostnames connected to {self.host_name}:")
        print(','.join(set(host_names)))
