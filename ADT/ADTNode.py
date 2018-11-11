import abc
from abc import ABC


class ADTNode(ABC):

    def __init__(self, id):
        self.id = id
        super().__init__()

    @abc.abstractmethod
    def accept(self, visitor):
        pass

    def return_vector(self, visitor):
        return []
