from .manager import CommandsManager


class _Class(type):
    _service = CommandsManager()

    def __getattr__(cls, item):
        def wrapper(*args, **kwargs):
            return getattr(_Class._service, item)(*args, **kwargs)

        return wrapper


class OperationsFacade(metaclass=_Class):
    ...
