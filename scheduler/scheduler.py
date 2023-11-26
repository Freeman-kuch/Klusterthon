"""Module for scheduler base functions"""
import schedule
import time
import threading
import json


class Reminder(schedule.Scheduler):
    """The scheduler class"""

    def __init__(self, name_of_drug):
        """Initialize a reminder"""
        super().__init__()
        self.name_of_drug = name_of_drug

    def run_continuously(self):
        """run a schedule indefinitely"""
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    interval = self.idle_seconds()
                    if interval is None:
                        break
                    elif interval > 0:
                        # sleep exactly the right amount of time
                        print(f"Time till Analytics reset: { interval } seconds")
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
    
    def start_schedule(self, interval):
        """start the medication schedule"""
        possible_hours = {
            "daily": 24,
            "bi_daily": 12,
            "tri_daily": 8,
            "quad_daily": 6
        }
        if possible_hours[interval] == 24:
            self.every().day.at().do()
        self.every().hours.do()
        self.run_continuously()
