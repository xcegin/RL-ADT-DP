from abc import ABC


class Rewarder(ABC):
    def __init__(self):
        pass

    def resolveReward(self, currentRow, argumentValues, currentFile):
        pass