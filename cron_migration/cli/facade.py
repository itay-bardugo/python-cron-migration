from .manager import CommandsManager
from cron_migration.system.meta.proxies import SimpleProxyMeta


class OperationProxy(SimpleProxyMeta):

    def _fwd_object(cls):
        return CommandsManager()


class OperationsFacade(metaclass=OperationProxy):
    """
    A proxy class to OpeartaionManager
    """
