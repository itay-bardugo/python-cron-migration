from cron_migration.files.models.path import Path


class NewEnvironment:
    def __init__(self):
        self.path: Path = None
        self.template: str = ""
