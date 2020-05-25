from cron_migration.files.models.path import Path


class NewEnvironment:
    def __init__(self, path: Path = None, template: str = "default"):
        self.path = path
        self.template = template
