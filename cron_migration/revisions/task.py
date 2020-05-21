from abc import abstractmethod


class Task:
    @abstractmethod
    def upgrade(self):
        ...

    @abstractmethod
    def downgrade(self):
        ...

    @classmethod
    @abstractmethod
    def get_revision_id(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def get_prev_revision_id(cls) -> str:
        ...
