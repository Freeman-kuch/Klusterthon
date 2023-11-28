"""Module for scheduler base functions"""
import schedule
import time
import threading
import json
from datetime import datetime
from typing import Callable


class Reminder(schedule.Scheduler):
    """The scheduler class"""

    def __init__(self, name_of_drug):
        """Initialize a reminder"""
        super().__init__()
        self.name_of_drug = name_of_drug

    def __run_continuously(self) -> threading.Event:
        """run a schedule indefinitely"""
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    interval = self.idle_seconds
                    if interval is None:
                        # This means there's no more schedule to be run
                        # e.g if the schedule was set to run once or end at a particular time
                        # when that time reaches, there would be nothing more to run, so it
                        # would return None
                        break
                    elif interval > 0:
                        # sleep exactly the right amount of time
                        # If time is up, it would return -1
                        print(f"Time till reminder reset: { interval } seconds")
                        time.sleep(interval)
                    self.run_pending()
                    cls.check_stop()
                print("Terminating continuous")

            @classmethod
            def check_stop(cls):
                with open("scheduler/data.json", "r", encoding="utf-8") as file:
                    j_file = json.load(file)
                # print(j_file)
                if j_file.get("stop"):
                    cease_continuous_run.set()

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run
    
    def start_schedule(self, interval: str, schedule_func: Callable, args: list) -> None:
        """start the medication schedule"""
        possible_hours = {
            "daily": 24,
            "bi_daily": 12,
            "tri_daily": 8,
            "quad_daily": 6
        }
        if possible_hours[interval] == 24:
            self.every().day.at(datetime.now().strftime("%X")).do(schedule_func, *args).tag(self.name_of_drug)
        self.every(possible_hours[interval]).hours.do(schedule_func, *args).tag(self.name_of_drug)
        self.__run_continuously()
