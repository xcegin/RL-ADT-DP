import json

from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement


class Enviroment():

    def __init__(self):
        with open('data.json') as f:
            data = json.load(f)
        self.data = data
        self.rootAdtNode = None
        self.arguments = []
        self.rootTreeAdtNode = None
        self.getRootADTNode()
        self.extractFunctionParams()
        self.parseLoadedJsonIntoTree()

    def getRootADTNode(self):
        found_root_node = False
        while not found_root_node:
            if "RootAdtNode" in self.data:
                self.rootAdtNode = self.data["RootAdtNode"]
                found_root_node = True
            else:
                self.data = self.data["properties"]

    def extractFunctionParams(self):
        arguments = self.rootAdtNode["Arguments"]
        for value in arguments["$values"]:
            variable = VariableDeclarationStatement(value["VariableTypeModifiers"], value["VariableType"],
                                                    value["Variable"], value["InitialValue"])
            self.arguments.append(variable)

    def parseLoadedJsonIntoTree(self):
        self.rootTreeAdtNode = FunctionDeclarationStatement(self.rootAdtNode["ReturnTypeModifiers"],
                                                            self.rootAdtNode["ReturnType"],
                                                            self.rootAdtNode["Name"], self.rootAdtNode["Arguments"],
                                                            self.rootAdtNode["Body"])

env = Enviroment()
