from scheduler import Scheduler
import schedule
import asyncio
import json

async def check_stop():
    with open("scheduler/data.json", "r", encoding="utf-8") as file:
        j_file = json.load(file)
    print(j_file)
    return j_file.get("stop")
async def test(value = 1):
    run = True
    def hello():
        print(f"hello {value}")
    schedule.every().minute.do(hello)
    new_routine = Scheduler()
    stop = new_routine.run_continuously()
    # while check := await check_stop() is False:
    #     # print(check)
    #     # print("hello schedule still on")
    #     pass
    # stop.set()
