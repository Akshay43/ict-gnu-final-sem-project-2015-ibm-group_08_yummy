from dataclasses import dataclass
from abc import abstractmethod, ABCMeta


@dataclass
class BaseCollection(ABCMeta):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

