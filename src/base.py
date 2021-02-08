from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def execute(self):
        return NotImplementedError("Subclasses should implement this funcionality")