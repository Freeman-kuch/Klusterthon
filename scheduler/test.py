from scheduler.scheduler import Scheduler
import schedule
import asyncio
import json
import time


async def test(value = 1, seconds = None):
    def hello():
        print(f"hello {value}")
    schedule.every().minute.do(hello)
    new_routine = Scheduler()
    stop = new_routine.run_continuously()
    if seconds:
        time.sleep(seconds)
        stop.set()
