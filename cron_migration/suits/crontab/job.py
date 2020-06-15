import os
from .scheduler import Scheduler


class Job:
    def __init__(self, command, minute="*", hour="*", month_day="*", month="*", week_day="*"):
        self._timing = [minute, hour, month_day, month, week_day]
        self.command = command + os.linesep
        self._scheduler = None

    @property
    def timing(self):
        return " ".join(self.scheduler.time if self.scheduler is not None else self._timing)

    def set_timing(self, t: list):
        """
        :param t: a list with 5 cells  [minute, hour, month_day, month, week_day]
        :return:
        """
        length = len(t)
        if length > 5:
            raise Exception("timing format: [minute, hour, month_day, month, week_day]")
        self._timing[length:5] = ["*"] * (5 - length)

    def set_minute(self, m):
        self._timing[0] = m

    def set_hour(self, h):
        self._timing[1] = h

    def set_month_day(self, md):
        self._timing[2] = md

    def set_month(self, m):
        self._timing[3] = m

    def set_week_day(self, wd):
        self._timing[4] = wd

    @property
    def scheduler(self):
        return self._scheduler

    @scheduler.setter
    def scheduler(self, s: Scheduler):
        self._scheduler = s

    def __str__(self):
        return "{} {}".format(self.timing, self.command)
