import json
from typing import Sequence
from abc import ABC, abstractmethod


class IStructureDriver(ABC):
    @abstractmethod
    def read(self) -> Sequence:
        pass

    @abstractmethod
    def write(self, data: Sequence) -> None:
        pass


class SimpleFileDriver(IStructureDriver):
    def __init__(self, filename):
        self.filename = filename

    def read(self) -> Sequence:
        with open(self.filename) as f:
            return [int(line) for line in f]

    def write(self, data: Sequence) -> None:
        with open(self.filename, "w") as f:
            for value in data:
                f.write(str(value))
                f.write('\n')

    def __repr__(self):
        return f"{self.__class__.__name__}(\"{self.filename}\")"


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def is_valid(data):
        if not isinstance(data, list):
            raise TypeError


    def read(self):
        with open(self.filename) as f:
            data = json.load(f)
            self.is_valid(data)
            return data

    def write(self, data):
        data = [i for i in data]
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def __repr__(self):
        return f"{self.__class__.__name__}(\"{self.filename}\")"


if __name__ == '__main__':
    write_data = [1, 2, 3]
    driver = SimpleFileDriver('tmp.txt')
    driver.write(write_data)

    read_data = driver.read()
    print(read_data)
