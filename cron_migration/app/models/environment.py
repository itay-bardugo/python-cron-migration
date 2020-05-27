from cron_migration.files.models.path import Path
import os


class Environment:
    def __init__(self, path: Path = None, template: str = "default"):
        self.path = path
        self.template = template

    def get_real_path(self):
        return self.path.path

    def get_revisions_path(self) -> Path:
        return Path(path=os.path.join(self.get_real_path() + os.path.sep + "versions"))
