import os


class Path:
    def __init__(self, path: str):
        self.path = path

    def join(self, *args):
        return os.path.join(self.path, *args)