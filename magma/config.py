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
    def __init__(self, env_key, default):
        init = getenv(env_key, default)
        super().__init__(init)
        self.env_key = env_key
        self.default = default

    def reset(self, default=None):
        if not default:
            default = self.default
        self.set(getenv(self.env_key, default))


class ConfigManager:
    __entries = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            ConfigManager.__entries[key] = value

    def _register(self, **kwargs):
        for key, value in kwargs.items():
            if key in ConfigManager.__entries:
                raise RuntimeError(f"Config with key '{key}' already exists")
            ConfigManager.__entries[key] = value

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
    debug_mode=RuntimeConfig(False),
)


def get_debug_mode():
    return config.debug_mode


def get_compile_dir():
    return config.compile_dir


def set_debug_mode(value):
    config.debug_mode = value


def set_compile_dir(value):
    config.compile_dir = value
