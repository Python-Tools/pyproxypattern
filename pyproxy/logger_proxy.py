import sys
import logging
from typing import Optional, Any
import structlog
from .proxy import Proxy


class StructlogProxy(Proxy):
    """Structlog的代理,使用app_name和loglevel初始化."""
    __slots__ = ('app_name', 'log_level', 'instance', "_callbacks", "_instance_check")

    def __init__(self, app_name: Optional[str] = None, log_level: Optional[str] = None) -> None:
        self.app_name = app_name
        self.log_level = log_level

        if app_name and log_level:
            instance = self.new_instance(app_name, log_level)
            super().__init__(instance)
        else:
            super().__init__()

    def new_instance(self, app_name: str, log_level: str, **kwargs: Any) -> structlog.BoundLogger:
        self.app_name = app_name
        self.log_level = log_level
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,  # 判断是否接受某个level的log消息
                structlog.stdlib.add_logger_name,  # 增加字段logger
                structlog.stdlib.add_log_level,  # 增加字段level
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(
                    fmt="iso"),  # 增加字段timestamp且使用iso格式输出
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,  # 捕获异常的栈信息
                structlog.processors.StackInfoRenderer(),  # 详细栈信息
                structlog.processors.JSONRenderer()  # json格式输出,第一个参数会被放入event字段
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        handler = logging.StreamHandler(sys.stdout)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(self.log_level)  # 设置最低log等级
        return structlog.get_logger(self.app_name, **kwargs)

    def initialize_for_app(self, app_name: str, *, log_level: str = "DEBUG", **kwargs: Any) -> None:
        """初始化log对象.
        Args:
            app_name (str): app名
            log_level (str): log等级
        """
        instance = self.new_instance(app_name, log_level, **kwargs)
        self.initialize(instance)


log = StructlogProxy()
