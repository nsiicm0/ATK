from typing import Callable
from ATK.lib import Meta


class Base(metaclass=Meta.MetaClass):
    def __init__(self):
        pass

def entering(func, calling, *args) -> None:
    """ Pre function logging """
    calling.log_as.info("Entered %s", func.__name__)

def exiting(func, calling) -> None:
    """ Post function logging """
    calling.log_as.info("Exited  %s", func.__name__)

def wrap(pre: Callable, post: Callable, guard: bool = False) -> Callable:
    """ Logging Wrapper
        A calling function can be guarded from errors, this means that the errors will be logged but not re-raised.
    """
    def decorate(func):
        """ Decorator """
        def call(self,*args, **kwargs):
            """ Actual wrapping """
            pre(func, self, *args)
            try:
                result = func(self, *args, **kwargs)
            except Exception:
                self.log_as.debug("Error in execution", exc_info=True)
                if not guard:
                    raise
            post(func, self)
            try:
                return result
            except UnboundLocalError:
                return None
            except:
                raise
        return call
    return decorate