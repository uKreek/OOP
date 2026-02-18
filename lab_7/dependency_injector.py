import inspect
from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Type, Dict, Optional, List
from contextlib import contextmanager


class LifeStyle(Enum):
    PER_REQUEST = 1
    SCOPED = 2
    SINGLETON = 3


class ScopeContext:
    def __init__(self):
        self._instances = {}

    def get(self, interface) -> Optional[Any]:
        return self._instances.get(interface)

    def set(self, interface, instance):
        self._instances[interface] = instance


class Injector:
    def __init__(self):
        self._registry = {}
        self._singletons = {}
        self._scope_stack: List[Dict[Any, Any]] = []
    def register(self, interface_type: Type, implementation: Any,
                 life_style: LifeStyle = LifeStyle.PER_REQUEST,
                 params: Dict[str, Any] = None):
        self._registry[interface_type] = {
            'impl': implementation,
            'life_style': life_style,
            'params': params or {},
            'is_factory': inspect.isfunction(implementation) or inspect.ismethod(implementation)
        }

    def get_instance(self, interface_type: Type) -> Any:
        if interface_type not in self._registry:
            raise ValueError(f"Интерфейс {interface_type.__name__} не зарегистрирован.")

        reg_info = self._registry[interface_type]
        life_style = reg_info['life_style']

        if life_style == LifeStyle.SINGLETON:
            if interface_type in self._singletons:
                return self._singletons[interface_type]

            instance = self._create_instance(reg_info)
            self._singletons[interface_type] = instance
            return instance

        if life_style == LifeStyle.SCOPED:
            if self._scope_stack is None:
                raise RuntimeError("Попытка получить SCOPED зависимость вне контекста (with injector.scope())")

            cached = self._scope_stack.get(interface_type)
            if cached:
                return cached

            instance = self._create_instance(reg_info)
            self._scope_stack.set(interface_type, instance)
            return instance

        return self._create_instance(reg_info)

    def _create_instance(self, reg_info: Dict) -> Any:
        impl = reg_info['impl']
        manual_params = reg_info['params']

        if reg_info['is_factory']:
            return impl()

        signature = inspect.signature(impl.__init__)
        constructor_args = {}

        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue

            if param_name in manual_params:
                constructor_args[param_name] = manual_params[param_name]
                continue

            if param.annotation in self._registry:
                constructor_args[param_name] = self.get_instance(param.annotation)
                continue
            if param.default == inspect.Parameter.empty:
                raise ValueError(f"Не удалось разрешить зависимость '{param_name}' для {impl.__name__}")

        return impl(**constructor_args)

    @contextmanager
    def scope(self):
        scope_cache = {}
        self._scope_stack.append(scope_cache)
        try:
            yield
        finally:
            self._scope_stack.pop()

    def scope(self):
        class ScopeManager:
            def __init__(self, injector):
                self.injector = injector
                self.prev_scope = None

            def __enter__(self):
                self.prev_scope = self.injector._current_scope
                self.injector._current_scope = ScopeContext()
                return self.injector

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.injector._current_scope = self.prev_scope

        return ScopeManager(self)


class ILogger(ABC):
    @abstractmethod
    def log(self, message: str): pass


class IDatabase(ABC):
    @abstractmethod
    def connect(self): pass


class INotificationService(ABC):
    @abstractmethod
    def send(self, msg: str): pass


class ConsoleLogger(ILogger):
    def __init__(self, prefix="[LOG]"):
        self.prefix = prefix

    def log(self, message: str):
        print(f"{self.prefix} Console: {message}")


class FileLogger(ILogger):
    def log(self, message: str):
        print(f"[FILE] Writing to disk: {message}")


class MySQLDatabase(IDatabase):
    def __init__(self):
        self.id = id(self)

    def connect(self):
        return f"MySQL Connection (ID: {self.id})"


class PostgresDatabase(IDatabase):
    def __init__(self):
        self.id = id(self)

    def connect(self):
        return f"Postgres Connection (ID: {self.id})"


class EmailService(INotificationService):
    def __init__(self, logger: ILogger, db: IDatabase):
        self.logger = logger
        self.db = db
        self.id = id(self)

    def send(self, msg: str):
        self.logger.log(f"Preparing to send '{msg}' via DB: {self.db.connect()}")
        print(f"--> Email sent! Service ID: {self.id}")


class SmsService(INotificationService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def send(self, msg: str):
        self.logger.log("SMS sending...")
        print(f"--> SMS sent: {msg}")


def simple_logger_factory():
    return ConsoleLogger(prefix="[FACTORY-CREATED]")
