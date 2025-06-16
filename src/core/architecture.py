class Singleton(type):
    """A singleton metaclass. Ensures a single instance of the class"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Service(metaclass=Singleton):
    """A base class for services, implementing singleton pattern"""

    pass
