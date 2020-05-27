from cron_migration.revisions.model import Revision
from .mapper import RevisionMap
import uuid
import datetime


class NewRevisionService:
    def __init__(self, revision: Revision, revision_map: 'RevisionMap'):
        self._revision = revision
        self._mapper = revision_map

    def _set_revision_signature(self, sig=None):
        self._revision.signature = uuid.uuid4().hex.strip("-")[-16:] if sig is None else sig
        return self._revision.signature

    def _set_date(self, dt_format=""):
        self._revision.date = datetime.datetime.now().strftime(dt_format if dt_format else "%d/%m/%Y %H:%M:%S")
        return self._revision.date

    def _set_message(self, message):
        self._revision.message = message
        return self._revision.message

    def _set_head(self):
        self._mapper.get_review()
        for revision in self._mapper.stream_revisions():
            ...

    def get(self):
        return self._revision

    def create_revision(self, message):
        self._set_revision_signature()
        self._set_date()
        self._set_message(message)
        self._set_head()
        return self.get()
