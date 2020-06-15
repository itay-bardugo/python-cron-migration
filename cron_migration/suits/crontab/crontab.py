import os
from .job import Job
from .scheduler import Scheduler
from .driver import Driver
from .utils import LazyProperty


class Crontab:

    def __init__(self, user=None, scheduler: Scheduler = None):
        self._driver = Driver()
        self._scheduler = scheduler
        if user:
            self._driver.user(user)

    def new_job(self, *args, **kwargs) -> Job:
        return Job(*args, **kwargs)

    @LazyProperty
    def all_jobs(self) -> set:
        exist_code, stdout, stderr = self._driver.all_jobs()
        commands = set()
        while (line := stdout.readline()):
            line = line.decode("utf-8")
            commands.add(line)
        return commands

    def insert(self, job: Job):
        commands = self.all_jobs
        commands.add(job.__str__())
        self._save_changes(commands)

    def remove(self, job: Job):
        commands = self.all_jobs
        commands.discard(job.__str__())
        self._save_changes(commands)

    def _save_changes(self, commands):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tab.txt")

        try:
            os.unlink(path)
        except:
            ...

        with open(path, "a") as f:
            for command in commands:
                f.write(command)
        self._driver.insert(path)
        os.unlink(path)

