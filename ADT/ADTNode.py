import abc
from abc import ABC


class ADTNode(ABC):

    @abc.abstractmethod
    def accept(self, visitor):
        pass

    def return_vector(self, visitor):
        return []
