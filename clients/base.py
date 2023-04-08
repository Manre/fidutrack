from abc import ABC, abstractmethod


class BaseClient(ABC):

    @abstractmethod
    def add(self, *args, **kwargs):
        pass

    @abstractmethod
    def authenticate(self, *args, **kwargs):
        pass
