from cron_migration.files.models.path import Path
import os


class Environment:
    def __init__(self, path: Path = None, template: str = "default"):
        self._path = path
        self.template = template

    def get_real_path(self):
        return self.path.path

    def get_script_path(self) -> Path:
        return Path(
            path=os.path.join(
                self.get_real_path() +
                os.path.sep +
                "revision.py.mako"
            )
        )

    def get_revisions_path(self, filename=None) -> Path:
        return Path(
            path=os.path.join(
                self.get_real_path() +
                os.path.sep +
                "revisions" +
                (os.path.sep + filename if filename else "")

            )
        )

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, p):
        self._path = p
