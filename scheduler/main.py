# from test import test
import asyncio
import queue
from background_worker import BackgroundThread

# async def main():
#     await asyncio.gather(test(), test(2))

# asyncio.run(main())

# initialize the background thread and task queue
task_queue = queue.Queue()
background_thread = BackgroundThread(task_queue)
background_thread.start()


def test_q(*args):
    statement, = args
    if statement:
        print(statement)
    else:
        print("hello")


user_input = "start"

# task_queue.put({"task_func": test_q})
while user_input != "End":
    task_queue.put({"task_func": test_q, "args": [user_input]})
    user_input = input("Enter something: ")

task_queue.put(None)
