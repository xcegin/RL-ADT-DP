import json
from copy import deepcopy

from gym import spaces

from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Utils.MathOperationsUtil import randomValue, resolveMathOperation
from ADT.Utils.ResolverUtil import resolveNodeViaType
from ADT.Visitors.DataDependenciesVisitor import DataDependenciesVisitor
from ADT.Visitors.VectorizationVisitor import VectorizationVisitor
from Enviroment import Utils
from Enviroment.ResolveJsonRef import resolveRef
from Enviroment.Utils import getTypeOfExpression
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext
from Heuristic.HeuristicCalculator import HeuristicCalculator
from Heuristic.HeuristicResolver import resolveHeuristic


class Enviroment():

    def __init__(self):
        with open('Enviroment/mcdc.json') as f:
            data = json.load(f)

        self.currentVector = 0
        self.currentNumOfTable = 0
        self.currentNumOfRow = 0
        self.argumentChangedVal = 0
        self.currentHeuristicValue = 0
        self.expressions = {}
        self.currentHeuristics = []
        self.currentVectors = []
        self.currentHeuristicRow = []
        self.currentVectorRow = []

        self.heuristicCalc = HeuristicCalculator()
        self.data = resolveRef(data, {})
        self.mcdc = data
        self.logicTable = None
        self.rootAdtNode = {}
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
        self.createVectorsForRows()

        self.action_space = spaces.Discrete(34)

    def startTable(self):
        self.currentHeuristics = self.listOfTableHeuristics[self.currentNumOfTable]
        self.currentVectors = self.listOfTableVectors[self.currentNumOfTable]
        self.currentNumOfTable = self.currentNumOfTable + 1

    def startRow(self):
        self.initializeArgumentValues()
        self.currentHeuristicRow = self.currentHeuristics[self.currentNumOfRow]
        self.currentVectorRow = self.currentVectors[self.currentNumOfRow]
        self.currentNumOfRow = self.currentNumOfRow + 1
        self.startingHeuristicValue = resolveHeuristic(self.argumentValues, self.arguments, self.currentHeuristicRow)
        self.currentHeuristicValue = self.startingHeuristicValue
        return self.currentVectorRow[0]

    def step(self, action):
        #self.currentVector = self.currentVector + 1
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        argumentValue = self.argumentValues[self.argumentChangedVal]
        argument = self.arguments[self.argumentChangedVal]
        self.argumentValues[self.argumentChangedVal] = resolveMathOperation(action, argumentValue,
                                                                            argument.variableType.typeName)
        currentHeuristicValue = resolveHeuristic(self.argumentValues, self.arguments, self.currentHeuristicRow)
        reward = self.returnReward(currentHeuristicValue)
        self.currentHeuristicValue = currentHeuristicValue
        self.argumentChangedVal = self.argumentChangedVal + 1
        #nextState = self.currentVectorRow[self.currentVector]

        done = False
        #TODO: reconsider the done checks
        if self.currentHeuristicValue < 0.5:
            done = True
        return reward, done, {}

        # ADD CHECK IF DONE - ITERATE THROUGH VECTORS IN ROW AND HEURISTIC VALUE CHECK
        # ADD RETURN VALUES

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
        self.rootTreeAdtNode = FunctionDeclarationStatement(self.rootAdtNode["$id"],
                                                            self.rootAdtNode["ReturnType"],
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
                self.expressions[expression["AdtNode"]["$id"]] = expression
                self.retrieveExpressions(expression["Children"]["$values"], expressions)
            else:
                self.expressions[expression["AdtNode"]["$id"]] = expression
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
                dataDependencyVisitor = DataDependenciesVisitor(enviromentWalkerContext(), dictForRow, self.expressions)
                self.rootTreeAdtNode.accept(dataDependencyVisitor)
                self.vectorizationVisitor = VectorizationVisitor(dataDependencyVisitor.context, dictForRow,
                                                                 self.arguments, self.expressions)
                list = self.rootTreeAdtNode.accept(self.vectorizationVisitor)
                list = [x for x in list if x != []]
                numOfTimes = int(round(len(list)) ** 1/4) + 1
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
        return finalDict

    def returnReward(self, currentHeuristicValue):
        difference = abs(self.currentHeuristicValue) - abs(currentHeuristicValue)
        if difference > 0:
            return difference / abs(self.currentHeuristicValue)
        else:
            return difference / abs(self.currentHeuristicValue)
