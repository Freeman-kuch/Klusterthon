import threading


class BackgroundThread(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        while True:
            task: dict = self.task_queue.get()
            if task is None:
                break
            task_func = task.get("task_func", None)
            if args := task.get("args", None):
                task_func(*args)
            else:
                task_func()
