from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def execute(self):
        return NotImplementedError("Subclasses should implement this funcionality")