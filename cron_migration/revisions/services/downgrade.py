from cron_migration.revisions.model import Revision
from .mapper import RevisionMapper
import uuid
import datetime
from mako.template import Template


class DowngradeService:
    def __init__(self, revision_map: 'RevisionMapper', environment: 'Environment'):
        self._mapper = revision_map
        self._environment = environment
        self._mapper.review()

    def get_waiting_list(self):
        revision = self._mapper.revisions[self._mapper.get_revision_to_upgrade]
        while revision:
            yield (self._mapper.revisions[revision.get_revision_id()])
            revision = self._mapper.revisions[revision.get_revision_id()].next

    def upgrade(self, revision):
        self._mapper.upgrade(revision)
