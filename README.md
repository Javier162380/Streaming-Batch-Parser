### TECH CHALLENGE.

# Install deps.

All the application code used just packages from the python standard library, you should be able to execute the challenge with a python distribution equal or greater than 3.8

Moreover, the application uses poetry as a package manager, so if you would like to use it to execute the application, you need to install the poetry environment.

```pip3 install poetry```

```poetry shell```

If you like to install the test dependencies, once you are inside the virtual environment, try.

```poetry install```


# Considerations.
All the challenge has been developed with the packages from the python standard library.
For adding some test coverage to my code, I used pytest, which it is not part of the standard library, but personally gives me a lot of speed when I like to test something. I hope it is not an issue.

Even though the tech challenge description refers to a script. I create two different interfaces with two different scripts, one for streaming and another for batch.

Both interfaces shared the same cli for the execution for simplicity. For executing the interfaces from the root of the project type.

```bash
python src/main.py -h
```
You should get an output similar to this one.

```
python src/main.py -h                                                                                
usage: main.py [-h] [-v] {batch,streaming} ...

Host processor

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Increase output verbosity

execution-mode:
  {batch,streaming}

```

As you could see, the first argument for the execution is a positional argument that can receive batch or streaming attributes. The batch option is referred for exercise 1, and the streaming option is referred for exercise 2.


# Exercise 1.


For executing the batch interface, first look at the cli attributes.

```bash
python src/main.py batch -h
```

You should receive an output similar to this one. 

```bash

usage: main.py batch [-h] [-v] -H HOST_NAME -s START_TIME -e END_TIME -f FILE_PATH [-b BATCH_SIZE]
                     {batch,streaming} ...

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -H HOST_NAME, --host-name HOST_NAME
                        Host Name we are analyzing
  -s START_TIME, --start-time START_TIME
                        Start time of the execution
  -e END_TIME, --end-time END_TIME
                        End time of the execution
  -f FILE_PATH, --file-path FILE_PATH
                        File abs path where the log file is located
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Size of the batch for processing data

```

For the first exercise, I use a pointer over a file provided by the CLI using the ```-f``` or ```--file-path``` parameter, and I create a python generator to read the file line by line and not overload the memory. Once the generator is created, I generate a sequential list of micro batches. The size of these micro-batches, is controlled by the flag ```-b``` or ```-batch-size```.  After that, I iter over the generator and analyzing if the micro-batch is in the target interval. This interval is defined by the cli with the flags ```-s``` or ```--start-time``` and ```-e``` or ```--end-time```. This way, I could limit the number of iterations.

The output requested by the challenge, is print by console in a rudimentary way. 

For this exercise, I considered that the challenge statement suggests that the records are ordered by timestamp, so I choose a single thread solution over a multithread solution to avoid extra complexity.

The target host to look at it is defined by the flag ```H``` or ```--host-name``` 

Example of execution.

```python
python src/main.py batch -H Aadvik -s 1565647212986 -e 1565647460814 -f data/batch/input-file-10000.txt
```

Output:

```
2021-02-07 12:15:46,856 [MainThread  ] [INFO ]  processing  file data/batch/input-file-10000.txt
2021-02-07 12:15:46,857 [MainThread  ] [INFO ]  Batch processed succesfully
2021-02-07 12:15:46,859 [MainThread  ] [INFO ]  Interval already proccessed exiting the loop
#########################################################


Hostnames connected to Aadvik:
Jadon,Nafeesa,Averyanna
```
The interface in charge of executing all the process it is located in this path ```src/batch_parser.py```.


# Exercise 2.

For the streaming part, I considered that the challenge force you to have all the part of the interface in the same process, and I am continue limited to use just the python standard libraries.

I don't like my solution as I will try to have an actor model connected by a queue in separate interfaces, running in two different processes. 

Given these limitations, I create a thread for reading data from a directory and send it in micro-batches to a python standard queue. The main thread is going to be in charge of processing the records coming from this queue. I used the python ```event``` built-in module. My idea is that when the thread in charge of reading the file or the main thread is working sleep the other one. This is a bottleneck for my system, but given the python GIL limitations, I tried to do it a to improve the CPU performance.

Similarly, as with the first exercise, the point of entry to this interface is handled by a CLI. From the root directory of the project execute.

```bash
python src/main.py batch -h
```

You should receive an output similar to this one.

```bash
usage: main.py streaming [-h] [-v] [-q QUEUE_SIZE] [-b BATCH_SIZE] [-t TIME] [-T TARGET_DIRECTORY] -H HOST_NAME
                         {batch,streaming} ...

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -q QUEUE_SIZE, --queue-size QUEUE_SIZE
                        Max number of messages retain by the qeue
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Size of the batch for proccessing data
  -t TIME, --time TIME  Time in seconds while the qeue continue accept receiving events
  -T TARGET_DIRECTORY, --target-directory TARGET_DIRECTORY
                        Target directory where files are located
  -H HOST_NAME, --host-name HOST_NAME
                        Host Name we are analyzing

execution-mode:
  {batch,streaming}

```

Some considerations event though the challenge says that the output should return results in an hourly basis. I add an attribute ```-q``` or ```--queue-size``` that it is in charge of limiting the number of messages the queue could retain. This way I could save my interface to consume a huge amount of memory and kill the proccess. When the queue is full it released the event and the main thread start processing those events even though the result on that particular case it is not going to be for the last hour. An extra implementation should be done, to guarantee this scenario.

Example of execution.

```
python src/main.py streaming -q 1000000000000 --time 10 --host-name Aadvik --batch-size 10 --target-directory data/streaming
```

You should received an output similar to this one.

```
2021-02-07 12:40:47,793 [MainThread  ] [INFO ]  Creating the setup for the streaming application
2021-02-07 12:40:47,793 [MainThread  ] [INFO ]  Setup was succesfull
2021-02-07 12:40:47,927 [ThreadPoolEx] [INFO ]  Processing thread is Active!
2021-02-07 12:40:47,927 [MainThread  ] [INFO ]  Future submit sleeping the main thread
2021-02-07 12:40:47,928 [ThreadPoolEx] [INFO ]  Processing file data/streaming/input-file-10000.txt
2021-02-07 12:40:51,979 [ThreadPoolEx] [INFO ]  File data/streaming/input-file-10000.txt proccessed
2021-02-07 12:40:51,980 [ThreadPoolEx] [INFO ]  File data/streaming/input-file-10000.txt moved to data/streaming/processed
2021-02-07 12:40:57,928 [MainThread  ] [INFO ]  Main thread released analyzing queue messages
#####################################################
#####################################################


The target host Aadvik:
received this connections in the last 10 seconds 
Manit ,Zinn ,Matina ,Athanasios ,Averyanna ,Nafeesa ,Jadon
The target host Aadvik:
was connected to this hosts in the last 10 seconds
Khiem
The host that received more connections in the last 10
it is the host Aadvik with 7 connections

2021-02-07 12:40:57,941 [MainThread  ] [INFO ]  Host processed releasing the main thread
2021-02-07 12:40:57,941 [MainThread  ] [INFO ]  Future submit sleeping the main thread
2021-02-07 12:41:07,990 [MainThread  ] [INFO ]  Main thread released analyzing queue messages
#####################################################
#####################################################


New Hosts where not processed in the last 10 seconds
2021-02-07 12:41:07,992 [MainThread  ] [INFO ]  Host processed releasing the main thread
2021-02-07 12:41:07,993 [MainThread  ] [INFO ]  Future submit sleeping the main thread
2021-02-07 12:41:17,994 [MainThread  ] [INFO ]  Main thread released analyzing queue messages
#####################################################
#####################################################


New Hosts where not processed in the last 10 seconds
2021-02-07 12:41:17,997 [MainThread  ] [INFO ]  Host processed releasing the main thread
2021-02-07 12:41:17,998 [MainThread  ] [INFO ]  Future submit sleeping the main thread
````

In this solution, I continue using python generators for reading files and micro-batches for process data. When the target directory is specified in that directory, a new sub folder called ```processed``` is created. On that folder are moved all the files analyzed by the reading thread. I avoid processing the same message twice as I assume it is something expected by the challenge. Also all new files added to the directory specify by the CLI will be processed when the reader thread it is relased so I assume this cover the funcionality required of proccessing new data.

# Testing.

In this solution, I continue using python generators for reading files and micro-batches for process data. When the target directory is specified in that directory, a new subfolder called ```processed``` is created. On that folder are moved all the files analyzed by the reading thread. I avoid processing the same message twice as I assume it is something expected by the challenge. Also, all new files added to the directory specified by the CLI will be processed when the reader thread is released, so I assume this covers the functionality required for processing new data.

# Testing.

Inside the test folder, I create a typical pytest project structure. I divide my test into unit and integration, although I perform unit testing for time reasons. This makes a lack of coverage in the streaming application.

For executing the test, you need to install the poetry environment, as defined in the install deps section. Once it is installed, type.

```python
pytest -vv --disable-warnings --cov=src

```

If you don't want to install poetry, you could build the root directory's docker image. It will run the test as part of the compilation process.

```bash
docker build -t clarity-challenge .
```

Thanks for submitting the challenge! 

If something is not clear, please do not hesitate and contact me.

Cheers 

Javier