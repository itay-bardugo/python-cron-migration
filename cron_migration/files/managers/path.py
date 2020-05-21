from cron_migration.system.meta.singleton import Singleton
from cron_migration.files.models.path import Path
import os
import shutil


class PathManager(metaclass=Singleton):

    def __init__(self):
        self.path: Path = None

    def set_path(self, path: Path):
        self.path = path

    def is_dir(self):
        return os.path.isdir(self.path.path)

    def has_access(self):
        return os.access(self.path.path, os.F_OK)

    def remove_tree(self):
        try:
            shutil.rmtree(self.path.path)
        except Exception:
            return False
