class Revision:
    def __init__(self, **kwargs):
        self.signature: str = kwargs.get("signature", "")
        self.message: str = kwargs.get("message", "")
        self.date = kwargs.get("date", "")
        self.head = None

    def __str__(self):
        return f"{self.signature}\t{self.message}\t{self.date}"
