import time
import random

from multiprocessing import Process, Queue, current_process


#
# Function run by worker processes
#
def worker(input, output):
    for func, args in iter(input.get, 'STOP'):

        result = calculate(func, args)

        output.put(result)


#
# Function used to calculate result
#
def calculate(func, args):
    result = func(*args)
    return '%s: %s = %s' % \
        (current_process().name, args[1], result)


def multi_thread_process(NUMBER_OF_PROCESSES, TASKS):
    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    for i in range(len(TASKS)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')
