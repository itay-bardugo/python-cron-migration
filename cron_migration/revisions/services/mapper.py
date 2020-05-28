from cron_migration.app.models.environment import Environment
import os
import importlib.util


class RevisionMap:
    def __init__(self, environment: Environment):
        self._environment = environment

    def stream_revisions(self):
        # for file_ in os.listdir(self._environment.get_revisions_path().path):
        #     spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
        #     foo = importlib.util.module_from_spec(spec)
        #     spec.loader.exec_module(foo)
        #     foo.MyClass()
        #     yield 1
        ...

    def review(self):
        # for revision in self.stream_revisions():
            ...
