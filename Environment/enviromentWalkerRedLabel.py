from abc import ABC


class Context(ABC):
    def __init__(self):
        self.dataDependencies = {}
        self.redLabels = []

# context used for visitors
class enviromentWalkerContext(Context):
    def __init__(self):
        super().__init__()
