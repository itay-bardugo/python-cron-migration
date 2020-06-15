class LazyProperty:
    def __init__(self, func):
        self._func = func
        self._func_name = self._func.__name__

    def __get__(self, instance, owner):
        instance.__dict__[self._func_name] = self._func(instance)
        return instance.__dict__[self._func_name]
