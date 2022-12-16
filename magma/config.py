from abc import ABC, abstractmethod
from os import getenv


class ConfigBase(ABC):
    @abstractmethod
    def get(self):
        raise NotImplementedError()

    @abstractmethod
    def set(self, value):
        raise NotImplementedError()


class RuntimeConfig(ConfigBase):
    def __init__(self, init):
        self.value = init

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class EnvConfig(RuntimeConfig):
    """
    Class for capturing runtime variables which can be read from environment
    variables.

    @env_key: Key for environment variable. Can be different than magma runtime
    config key.

    @default: Default value for variable if not found in environment.

    @typ: Optional argument for the type of this variable. Since all environment
    variables are stored as strings, specifying this argument automatically
    promotes strings to the provided type.
    """
    def __init__(self, env_key, default, typ=None):
        init = getenv(env_key, default)
        if typ is not None:
            init = typ(init)
        super().__init__(init)
        self.env_key = env_key
        self.default = default
        self.typ = typ

    def reset(self, default=None):
        if not default:
            default = self.default
        value = getenv(self.env_key, default)
        if self.typ is not None:
            value = typ(value)
        self.set(value)


class ConfigManager:
    __entries = {}

    def __init__(self, **kwargs):
        self._register(**kwargs)

    def _register(self, **kwargs):
        for key, value in kwargs.items():
            if key in ConfigManager.__entries:
                raise RuntimeError(f"Config with key '{key}' already exists")
            ConfigManager.__entries[key] = value

    def register(self, **kwargs):
        self._register(**kwargs)

    def __get(self, key):
        return ConfigManager.__entries[key].get()

    def __set(self, key, value):
        ConfigManager.__entries[key].set(value)

    def __getattr__(self, key):
        return self.__get(key)

    def __setattr__(self, key, value):
        self.__set(key, value)

    def __getitem__(self, key):
        return self.__get(key)

    def __setitem__(self, key, value):
        self.__set(key, value)


config = ConfigManager(
    compile_dir=RuntimeConfig("normal"),
    debug_mode=RuntimeConfig(False)
)


def get_debug_mode():
    return config.debug_mode


def get_compile_dir():
    return config.compile_dir


def set_debug_mode(value):
    config.debug_mode = value


def set_compile_dir(value):
    config.compile_dir = value
