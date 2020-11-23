import functools
from typing import Optional, Callable, Any, TypeVar, List, Generic
T = TypeVar('T')


class Proxy(Generic[T]):
    """任意对象的代理对象.

    Attributes:
        instance (T): 被代理的实例
        _callbacks (List[Callabel[[Any], None]]): 注册成功后执行的回调函数

    """
    __slots__ = ('instance', '_callbacks')
    instance: Optional[T]
    _callbacks: List[Callable[[T], None]]

    def __init__(self, instance: Optional[T] = None) -> None:
        self._callbacks = []
        self.instance = instance

    def initialize(self, instance: T) -> None:
        """将被代理的实例注册到代理上."""
        self.instance = instance

        for callback in self._callbacks:
            callback(self.instance)

    def attach_callback(self, callback: Callable[[T], None]) -> Callable[[T], None]:
        """代理被注册时的回调.

        Args:
            callback (function): [description]
        """
        @functools.wraps(callback)
        def warp(instance: T) -> None:
            return callback(instance)
        self._callbacks.append(warp)
        return warp

    def __getattr__(self, attr: str) -> Any:
        if self.instance is None:
            raise AttributeError('Cannot use uninitialized Proxy.')
        return getattr(self.instance, attr)

    def __setattr__(self, attr: str, value: Any) -> Any:
        if attr not in self.__slots__:
            raise AttributeError('Cannot set attribute on proxy.')
        return super().__setattr__(attr, value)
