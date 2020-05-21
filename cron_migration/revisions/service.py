from .model import Revision
import uuid


def generate_revision_id():
    return uuid.uuid4().hex[-12:]


def generate(revision: Revision):
    revision.signature = generate_revision_id()
    return str(revision)
