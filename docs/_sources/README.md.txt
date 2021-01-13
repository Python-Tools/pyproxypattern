# pyproxypattern

根据peewee的proxy做的单独的python对象代理模式.

## 特性

+ 提供一个相对通用的代理类`Proxy`
+ 提供用于检测代理对象类型的回调函数`attach_instance_check`
+ 提供在初始化代理对象后的回调函数注册器`attach_callback`,回调函数回按注册的顺序执行
+ 可以代理上下文对象,迭代器对象
+ 可以代理异步上下文对象,异步迭代器对象

## 安装

`pip install pyproxypattern`

## 使用

两种方式:

1. 直接使用`Proxy`的实例代理对象

    ```python
    class Test_B:
        def get2(self) -> int:
            return 2
    B = Test_B()
    proxy = Proxy()
    proxy.attach_instance_check(lambda x: isinstance(x, Test_B))
    proxy.initialize(B)
    proxy.get2() == 2
    ```

2. 将`Proxy`类作为父类构造一个更加负载的代理类,然后再用它的实例代理特定对象

    ```python
    class AredisProxy(Proxy):
        """aredis的代理类."""
        __slots__ = ('instance', "_callbacks", "_instance_check", "url")

        def __init__(self, url: Optional[str] = None, decode_responses: bool = True, **kwargs: Any) -> None:
            if url:
                instance = self.new_instance(url, decode_responses, **kwargs)
                super().__init__(instance)
            else:
                super().__init__()

        def new_instance(self, url: str, decode_responses: bool, **kwargs: Any) -> Any:
            self.url = url
            return StrictRedis.from_url(url, decode_responses=decode_responses, **kwargs)

        def initialize_from_url(self, url: str, *, decode_responses: bool = False, **kwargs: Any) -> None:
            """初始化."""
            instance = self.new_instance(url, decode_responses, **kwargs)
            self.initialize(instance)
    ```
