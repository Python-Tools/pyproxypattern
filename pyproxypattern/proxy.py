import functools
from typing import Optional, Callable, Any, TypeVar, List, Generic, Awaitable
T = TypeVar('T')


def passthrough(method: str) -> Callable[..., Any]:
    """构造被代理对象的接口

    Args:
        method ([type]): [description]
    """

    def inner(self: 'Proxy', *args: Any, **kwargs: Any) -> Any:
        if self.instance is None:
            raise AttributeError('Cannot use uninitialized Proxy.')
        return getattr(self.instance, method)(*args, **kwargs)
    return inner


def apassthrough(method: str) -> Callable[..., Awaitable[Any]]:
    """构造被代理对象的接口

    Args:
        method ([type]): [description]
    """

    async def inner(self: 'Proxy', *args: Any, **kwargs: Any) -> Awaitable[Any]:
        if self.instance is None:
            raise AttributeError('Cannot use uninitialized Proxy.')
        return await getattr(self.instance, method)(*args, **kwargs)
    return inner


class Proxy(Generic[T]):
    """任意对象的代理对象.

    Attributes:
        instance (T): 被代理的实例
        _callbacks (List[Callabel[[Any], None]]): 注册成功后执行的回调函数

    """
    __slots__ = ('instance', '_callbacks', '_instance_check')
    instance: Optional[T]
    _callbacks: List[Callable[[T], None]]
    _instance_check: Optional[Callable[[T], bool]]

    def __init__(self, instance: Optional[T] = None) -> None:
        self._callbacks = []
        self.instance = None
        self._instance_check = None
        if instance:
            self.initialize(instance)

    def attach_instance_check(self, func: Callable[[T], bool]) -> Callable[[T], bool]:
        """代理注册实例前进行的校验.

        可以作为装饰器使用.如果未注册则不进行校验

        Args:
            func ( Callable[[T], bool]): [description]
        """
        @functools.wraps(func)
        def warp(instance: T) -> bool:
            return func(instance)

        self._instance_check = warp
        return warp

    def initialize(self, instance: T) -> None:
        """将被代理的实例注册到代理上."""
        if self._instance_check:
            if self._instance_check(instance):
                self.instance = instance
            else:
                raise AttributeError("实例校验失败")
        else:
            self.instance = instance

        for callback in self._callbacks:
            callback(self.instance)

    def attach_callback(self, callback: Callable[[T], None]) -> Callable[[T], None]:
        """代理被注册时的回调.

        可以作为装饰器使用.

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

    __enter__ = passthrough('__enter__')
    __exit__ = passthrough('__exit__')
    __aenter__ = apassthrough('__aenter__')
    __aexit__ = apassthrough('__aexit__')

    __next__ = passthrough('__next__')
    __iter__ = passthrough('__iter__')
    __anext__ = apassthrough('__anext__')
    __aiter__ = apassthrough('__aiter__')
