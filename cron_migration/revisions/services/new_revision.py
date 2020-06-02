from cron_migration.revisions.model import Revision
from .mapper import RevisionMapper
import uuid
import datetime
from mako.template import Template


class NewRevisionService:
    def __init__(self, revision: Revision, revision_map: 'RevisionMapper', environment: 'Environment'):
        self._revision = revision
        self._mapper = revision_map
        self._environment = environment

    def _set_revision_signature(self, sig=None):
        self._revision.signature = uuid.uuid4().hex.strip("-")[-16:] if sig is None else sig
        return self._revision.signature

    def _set_date(self, dt_format=""):
        self._revision.date = datetime.datetime.now().strftime(dt_format if dt_format else "%d/%m/%Y %H:%M:%S")
        return self._revision.date

    def _set_message(self, message):
        self._revision.message = message
        return self._revision.message

    def _set_down_revision(self, down_revision):
        self._revision.down_revision = down_revision

    def get(self):
        return self._revision

    def review(self):
        self._mapper.review()

    def _make_template_file(self):
        revision = self.get()
        template = Template(filename=u"{}".format(self._environment.get_script_path().path))
        dst = u"{}_{}.py".format(revision.signature, revision.message)
        with open(self._environment.get_revisions_path(dst).path, "wb") as f:
            f.write(
                template.render_unicode(
                    revision=revision.signature,
                    prev_revision=revision.down_revision,
                    date=revision.date
                ).encode("utf-8")
            )
        return self._environment.get_revisions_path(dst).path

    def make_revision_file(self, message):
        self.review()
        self._set_revision_signature()
        self._set_date()
        self._set_message(message)
        self._set_down_revision(self._mapper.get_latest_revision())
        return self._make_template_file()
