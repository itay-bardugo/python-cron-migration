from .task import Task
from typing import Type


class TaskManager:
    def __init__(self, task: Type[Task], path):
        self.task = task
        self._all_down_revisions = set()
        self.next: Task = None
        self.prev: Task = None
        self.path = path

    def get_down_revision(self):
        return self.task.get_prev_revision_id()

    def get_revision_id(self):
        return self.task.get_revision_id()

    def set_next(self, task: Task):
        self.next = task

    def set_prev(self, task: Task):
        self.prev = task

    def upgrade(self):
        self.task().upgrade()
