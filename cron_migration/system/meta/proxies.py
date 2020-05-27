from abc import ABCMeta, abstractmethod


class SimpleProxyMeta(type, metaclass=ABCMeta):
    _instance = None

    @abstractmethod
    def _fwd_object(cls):
        """
        should returns a target object
        :return:
        """

    def _get_object(cls):
        if cls._instance is None:
            cls._instance = cls._fwd_object()
        return cls._instance

    def __getattr__(cls, item):
        def wrapper(*args, **kwargs):
            return getattr(cls._get_object(), item)(*args, **kwargs)

        return wrapper