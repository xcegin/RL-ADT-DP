from abc import ABC
from copy import deepcopy


class Context(ABC):
    def __init__(self):
        self.dataDependencies = {}
        self.redLabels = []


class enviromentWalkerContext(Context):
    def __init__(self):
        super().__init__()


class redLabel():
    def __init__(self):
        self.embed = []

    def __int__(self, cloned):
        self.embed = deepcopy(cloned)
