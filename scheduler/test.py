from reminder import Reminder
import schedule
import asyncio
import json
import time


def test(value = 1, seconds = None):
    def hello():
        print(f"hello {value}")
    schedule.every().minute.do(hello)
    new_routine = Reminder("paracetamol")
    new_routine.start_schedule("quad_daily")
    # if seconds:
    #     time.sleep(seconds)
    #     stop.set()


test()