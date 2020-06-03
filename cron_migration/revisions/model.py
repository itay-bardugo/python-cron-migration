import os


class Revision:
    def __init__(self, **kwargs):
        self.signature: str = kwargs.get("signature", "")
        self._message: str = kwargs.get("message", "")
        self.date = kwargs.get("date", "")
        self.down_revision = None

    def __str__(self):
        return f"{self.signature}\t{self.message}\t{self.date}"

    @property
    def message(self):
        return os.path.normpath(self._message)

    @message.setter
    def message(self, m: str):
        self._message = m.replace(" ", "_")
