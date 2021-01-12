"""定义peewee_async代理对象的模块

这个模块使用url初始化,同时提供一个默认的代理对象`db_proxy`.
"""
from typing import Optional, List
import peewee_async
from playhouse.db_url import connect
from playhouse.reflection import generate_models
from .proxy import Proxy


class PeeweeAsyncProxy(Proxy):
    """peewee_async的代理类."""
    __slots__ = ('instance', "_callbacks", "_instance_check", "sync_instance", "models", "url")

    def __init__(self, url: Optional[str] = None, *, table_names: Optional[List[str]] = None) -> None:
        if url:
            instance = self.new_instance(url, table_names=table_names)
            super().__init__(instance)
        else:
            super().__init__()

    def new_instance(self, url: str, table_names: Optional[List[str]] = None) -> peewee_async.Manager:
        self.url = url
        self.sync_instance = connect(url)
        if table_names:
            self.models = generate_models(self.sync_instance, table_names=table_names, include_views=True)
        else:
            self.models = generate_models(self.sync_instance, include_views=True)
        return peewee_async.Manager(self.sync_instance)

    def initialize_from_URL(self, url: str, *, table_names: Optional[List[str]] = None) -> None:
        """初始化."""
        instance = self.new_instance(url, table_names=table_names)
        self.initialize(instance)


db_proxy = PeeweeAsyncProxy()
