import datetime


class Revision:
    def __init__(self):
        self.signature: str = ""
        self.message: str = ""
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return f"{self.signature}\t{self.message}\t{self.date}"
