import json
from copy import deepcopy

from gym import spaces

from Enviroment import Utils
from ADT.Utils.ResolverUtil import resolveNodeViaType
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Visitors.DataDependenciesVisitor import DataDependenciesVisitor
from ADT.Visitors.VectorizationVisitor import VectorizationVisitor
from ADT.Utils.MathOperationsUtil import randomValue
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext
from Heuristic.HeuristicCalculator import HeuristicCalculator
from Enviroment.Utils import getTypeOfExpression


class Enviroment():

    def __init__(self):
        with open('data.json') as f:
            data = json.load(f)
        with open('mcdc.json') as f:
            mcdc = json.load(f)

        self.heuristicCalc = HeuristicCalculator()
        self.data = data
        self.mcdc = mcdc
        self.logicTable = None
        self.rootAdtNode = None
        self.arguments = {}
        self.argumentValues = {}
        self.rootTreeAdtNode = None
        self.listOfTables = []
        self.listOfTableHeuristics = []
        self.listOfTableVectors = []
        self.context = enviromentWalkerContext()

        self.getRootADTNode()
        self.extractFunctionParams()
        self.getLogicExpressionsFromMcDc()
        self.parseLoadedJsonIntoTree()
        self.createListOfMcDcTableRows()
        self.createHeuristicEquationsForRows()
        self.initializeArgumentValues()
        self.createVectorsForRows()

        self.action_space = spaces.Discrete(34)

    #TODO make some env reset function
    def reset(self):
        pass

    def step(self, action):
        pass

    def getRootADTNode(self):
        found_root_node = False
        while not found_root_node:
            if "RootAdtNode" in self.data:
                self.rootAdtNode = self.data["RootAdtNode"]
                found_root_node = True
            else:
                self.data = self.data["properties"]

    def getLogicExpressionsFromMcDc(self):
        found_logic_table = False
        while not found_logic_table:
            if "LogicTables" in self.mcdc:
                self.logicTable = self.mcdc["LogicTables"]
                found_logic_table = True
            else:
                self.mcdc = self.mcdc["properties"]

    def extractFunctionParams(self):
        arguments = self.rootAdtNode["Arguments"]
        for value in arguments["$values"]:
            variableDecl = resolveNodeViaType(value["$type"], value)
            self.arguments[variableDecl.variable.variableName] = variableDecl

    def parseLoadedJsonIntoTree(self):
        self.rootTreeAdtNode = FunctionDeclarationStatement(self.rootAdtNode["ReturnType"],
                                                            self.rootAdtNode["Name"], self.rootAdtNode["Arguments"],
                                                            self.rootAdtNode["Body"])

    def createListOfMcDcTableRows(self):
        for table in self.mcdc["LogicTables"]["$values"]:
            tableRows = []
            rootLogicExpression = table["LogicExpression"]
            expressions = []
            self.retrieveExpressions(rootLogicExpression["Children"]["$values"], expressions)
            # Extract values for each column according to one row
            for row in table["TruthTable"]["$values"]:
                rowList = []
                columnCounter = 0
                for value in row["RowValues"]["$values"]:
                    keyValuePair = {expressions[columnCounter]: value}
                    rowList.append(keyValuePair)
                    columnCounter = columnCounter + 1
                tableRows.append(rowList)
            self.listOfTables.append(tableRows)

    def retrieveExpressions(self, values, expressions):
        for expression in values:
            if getTypeOfExpression(expression["$type"]) == Utils.COMPOSITE_EXPRESSION:
                self.retrieveExpressions(expression["Children"]["$values"], expressions)
            else:
                expressions.append(expression["Token"])
        return expressions

    def createHeuristicEquationsForRows(self):
        for table in self.listOfTables:
            tableRows = []
            # Extract values for each column according to one row
            for row in table:
                rowList = [self.heuristicCalc.calculateHeuristicFerOneFeckinRowM8(row)]
                tableRows.append(rowList)
            self.listOfTableHeuristics.append(tableRows)

    def createVectorsForRows(self):
        for table in self.listOfTables:
            tableRows = []
            # Extract values for each column according to one row
            for row in table:
                dictForRow = self.mergeDictsInRow(row)
                dataDependencyVisitor = DataDependenciesVisitor(enviromentWalkerContext(), dictForRow)
                self.rootTreeAdtNode.accept(dataDependencyVisitor)
                self.vectorizationVisitor = VectorizationVisitor(dataDependencyVisitor.context, dictForRow, self.arguments)
                list = self.rootTreeAdtNode.accept(self.vectorizationVisitor)
                list = [x for x in list if x != []]
                numOfTimes = int(round(len(list)) ** 1/3) + 1
                for x in range(numOfTimes):
                    toBeAppended = deepcopy(list)
                    list = list + toBeAppended
                tableRows.append(list)
            self.listOfTableVectors.append(tableRows)

    def initializeArgumentValues(self):
        for argument in self.arguments:
            self.argumentValues[self.arguments[argument].variable.variableName] = \
                randomValue(self.arguments[argument].variableType)

    def mergeDictsInRow(self, row):
        finalDict = {}
        for dictionary in row:
            finalDict = {**finalDict, **dictionary}
        for key in list(finalDict.keys()):
            if "~" in key:
                tmpKey = key + " "
                newKey = self.replaceTildeVariableNames(tmpKey)
                finalDict[newKey] = finalDict[key]
                del finalDict[key]
        return finalDict

    #TODO: Replace with tilde addition in datadependenciesvisitor
    def replaceTildeVariableNames(self, key):
        indexOfTilde = key.find("~")
        tmp = key[indexOfTilde:]
        indexOfSpace = tmp.find(" ")
        newKey = key[:indexOfTilde] + tmp[indexOfSpace:]
        if "~" in newKey:
            return self.replaceTildeVariableNames(newKey)
        return newKey[:-1]


env = Enviroment()
