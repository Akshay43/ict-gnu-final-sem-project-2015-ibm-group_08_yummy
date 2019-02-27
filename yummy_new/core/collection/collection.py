from .base_collection import BaseCollection
from typing import List, Dict, Any, AnyStr


DATA = Dict[str, Any]
DATAList = List[DATA]


class Collection(BaseCollection):

    def __post_init__(self):
        self.__container = dict()

    @property
    def container(self):
        return self.__container

    @container.setter
    def container(self, value):
        pass

    def add(self, data: DATA):
        key = data.get('name', hash(data))
        self.container[key] = data

    def add_all(self, datalist: DATAList):
        for data in datalist:
            self.add(data)

    def __iter__(self):
        pass

    def __getitem__(self, key: AnyStr) -> Any:
        return self.container.get(key, None)

    def __setitem__(self, key: AnyStr, value: Any) -> None:
        self.container[key] = value

    def __len__(self):
        return len(self.container)

    def __add__(self, other):
        pass
