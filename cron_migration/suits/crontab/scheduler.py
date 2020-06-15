class Scheduler:
    def __init__(self, time: list = ["*"] * 5):
        self._time = time

    @property
    def time(self):
        return tuple(self._time)

    def every_5_minutes(self):
        self._time[0] = "*/5"
        self._time[1:] = ["*"] * 4

    def every_10_minutes(self):
        self._time[0] = "*/10"
        self._time[1:] = ["*"] * 4

    def every_15_minutes(self):
        self._time[0] = "*/15"
        self._time[1:] = ["*"] * 4

    def every_30_minutes(self):
        self._time[0] = "*/30"
        self._time[1:] = ["*"] * 4

    def once_per_hour(self):
        self._time[0] = "0"
        self._time[1:] = ["*"] * 4

    def at_midnight(self):
        self._time[0:2] = ["0"] * 2
        self._time[1:] = ["*"] * 4
