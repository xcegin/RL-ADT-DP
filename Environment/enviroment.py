import json
from copy import deepcopy

from gym import spaces

from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Utils.MathOperationsUtil import resolveMathOperation, resolveContinuousTypeWithOperation
from ADT.Utils.ResolverUtil import resolveNodeViaType, ResolverUtil
from ADT.Visitors.DataDependenciesVisitor import DataDependenciesVisitor
from ADT.Visitors.VectorizationVisitor import VectorizationVisitor
from Environment import Utils
from Environment.ResolveJsonRef import resolveRef
from Environment.Utils import getTypeOfExpression
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext
from Reward.Coverage.CoverageRewarder import CoverageRewarder
from Reward.StaticRewarder import StaticRewardCalculator
from Vectorizer.SampleVisitorCovEnv import SampleVisitorEnvWithConv
from Vectorizer.SampleVisitorForEnviroment import SampleVisitorEnv


class Enviroment:

    def __init__(self):
        self.reset()
        self.dict_of_max_r = {}

    def reset(self):
        import glob
        self.listOfFiles = glob.glob("jsons/*.json")
        self.iterator = iter(self.listOfFiles)
        self.currentF = 0

    def prepareNextFile(self):
        if self.currentF < len(self.listOfFiles):
            item = next(self.iterator)
            with open(item) as f:
                data = json.load(f)
            self.initialize_def(data)
            self.currentF += 1

    def prepareNextFileConv(self):
        if self.currentF < len(self.listOfFiles):
            item = next(self.iterator)
            with open(item) as f:
                data = json.load(f)
            self.initialize_conv(data)
            self.currentF += 1

    def prepareNextFileConvWithCov(self, numberOfWorker=0):
        if self.currentF < len(self.listOfFiles):
            item = next(self.iterator)
            with open(item) as f:
                data = json.load(f)
            self.initialize_conv_cov(data, numberOfWorker)
            self.currentF += 1

    def initialize_conv_cov(self, data, numOfWorker):
        self.initialize(data)
        self.prepareVectorsForTablesConvWithCov()
        self.argumentMatrix = []
        self.rewarder = CoverageRewarder()
        self.initializeArgumentValuesCov()

        self.initialCov = self.rewarder.resolveReward(self.rootTreeAdtNode.name, str(numOfWorker), self.argumentMatrix)
        if self.rootTreeAdtNode.name not in self.dict_of_max_r:
            self.dict_of_max_r[self.rootTreeAdtNode.name] = self.initialCov
        self.argumentColumnValue = 0

        self.action_space = spaces.Discrete(9)

    def initialize(self, data):
        self.resolverUtil = ResolverUtil()
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

        self.rewarder = StaticRewardCalculator()
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

    def initialize_def(self, data):
        self.initialize(data)
        self.createVectorsForRows()

        self.action_space = spaces.Discrete(9)

    def initialize_conv(self, data):
        self.initialize(data)
        self.prepareVectorsForRowsConv()
        self.initializeArgumentValues()
        self.argumentColumnValue = 0

        self.action_space = spaces.Discrete(9)

    def prepareVectorsForTablesConvWithCov(self):
        for table in self.listOfTables:
            self.vectorizationVisitor = SampleVisitorEnvWithConv(enviromentWalkerContext(), self.rootTreeAdtNode.name)
            mainNode = self.rootTreeAdtNode.accept(self.vectorizationVisitor)
            self.listOfTableVectors.append(mainNode)

    def startTable(self):
        #self.currentHeuristics = self.f[self.currentNumOfTable]
        self.currentVectors = self.listOfTableVectors[self.currentNumOfTable]
        self.currentNumOfTable = self.currentNumOfTable + 1

    def startRow(self, numOfFile=None):
        self.initializeArgumentValues()
        self.currentVectorRow = self.currentVectors[self.currentNumOfRow]
        self.currentNumOfRow = self.currentNumOfRow + 1
        self.startingHeuristicValue = self.rewarder.resolveReward(self.listOfTables[self.currentNumOfTable - 1]
                                                                  [self.currentNumOfRow - 1], self.argumentValues,
                                                                  numOfFile)
        self.currentHeuristicValue = self.startingHeuristicValue
        return self.currentVectorRow[0]

    def step(self, action, numOfFile=None):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        keyOfArg = list(self.arguments.keys())[self.argumentChangedVal % len(list(self.arguments.keys()))]
        argumentValue = self.argumentValues[keyOfArg]
        if isinstance(argumentValue, complex):
            return -1, True, {}
        argument = self.arguments[keyOfArg]
        try:
            self.argumentValues[keyOfArg] = resolveMathOperation(action, argumentValue,
                                                                 argument.variableType.typeName)
        except TypeError:
            return -1, True, {}
        except OverflowError:
            return -1, True, {}
        currentHeuristicValue = self.rewarder.resolveReward(self.listOfTables[self.currentNumOfTable - 1]
                                                            [self.currentNumOfRow - 1], self.argumentValues, numOfFile)
        reward = self.returnRewardCov(currentHeuristicValue)
        self.currentHeuristicValue = currentHeuristicValue
        self.argumentChangedVal = self.argumentChangedVal + 1

        done = False
        if self.currentHeuristicValue >= 0.9:
            done = True
        return reward, done, currentHeuristicValue

    def step_cov(self, action, numOfWorker, numOfFile=None):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        if self.argumentChangedVal % len(list(self.arguments.keys())) == 0 and self.argumentChangedVal != 0:
            self.argumentColumnValue += 1
        argColVal = self.argumentColumnValue % self.totalRows
        keyOfArg = self.argumentChangedVal % len(list(self.arguments.keys()))
        keyForDict = list(self.arguments.keys())[self.argumentChangedVal % len(list(self.arguments.keys()))]
        argumentValue = self.argumentMatrix[argColVal][keyOfArg]
        self.argumentChangedVal = self.argumentChangedVal + 1
        if isinstance(argumentValue, complex):
            return -1, True, {}
        argument = self.arguments[keyForDict]
        try:
            self.argumentMatrix[argColVal][keyOfArg] = resolveMathOperation(action, argumentValue,
                                                                            argument.variableType.typeName)
        except TypeError:
            return -1, True, {}
        except OverflowError:
            return -1, True, {}
        currentCoverage = self.rewarder.resolveReward(self.rootTreeAdtNode.name, str(numOfWorker), self.argumentMatrix)
        if currentCoverage == 0:
            return 0, False, 0, {}
        reward = self.returnRewardCov(currentCoverage, self.rootTreeAdtNode.name)
        # nextState = self.currentVectorRow[self.currentVector]

        done = False
        if currentCoverage >= 100:
            done = True
        return reward, done, (currentCoverage / 100), {}


    def step_cov_continuos(self, action, numOfWorker):
        keyOfArg = list(self.arguments.keys())[self.argumentChangedVal % len(list(self.arguments.keys()))]
        argumentValue = self.argumentValues[keyOfArg]
        if isinstance(argumentValue, complex):
            return -1, True, {}
        argument = self.arguments[keyOfArg]
        try:
            self.argumentValues[keyOfArg] = resolveContinuousTypeWithOperation(action, argument.variableType.typeName, argumentValue)
        except TypeError:
            return -1, True, {}
        except OverflowError:
            return -1, True, {}
        currentHeuristicValue = self.rewarder.resolveReward(self.listOfTables[self.currentNumOfTable - 1]
                                                            [self.currentNumOfRow - 1], self.argumentValues, numOfWorker)
        reward = self.returnRewardCov(currentHeuristicValue)
        self.currentHeuristicValue = currentHeuristicValue
        self.argumentChangedVal = self.argumentChangedVal + 1
        done = False
        if self.currentHeuristicValue >= 0.9:
            done = True
        return reward, done, currentHeuristicValue

    def step_cov_continuos_without_reward(self, action, numOfWorker):
        if self.argumentChangedVal % len(list(self.arguments.keys())) == 0 and self.argumentChangedVal != 0:
            self.argumentColumnValue += 1
        argColVal = self.argumentColumnValue % self.totalRows
        keyOfArg = self.argumentChangedVal % len(list(self.arguments.keys()))
        keyForDict = list(self.arguments.keys())[self.argumentChangedVal % len(list(self.arguments.keys()))]
        argumentValue = self.argumentMatrix[argColVal][keyOfArg]
        self.argumentChangedVal = self.argumentChangedVal + 1
        if isinstance(argumentValue, complex):
            return -1, True, {}
        argument = self.arguments[keyForDict]
        self.argumentMatrix[argColVal][keyOfArg] = resolveContinuousTypeWithOperation(action, argument.variableType.typeName, argumentValue)

    def step_cov_continuos_entire_matrix(self, numOfWorker):
        currentCoverage = self.rewarder.resolveReward(self.rootTreeAdtNode.name, str(numOfWorker), self.argumentMatrix)
        if currentCoverage == 0:
            return 0, False, 0, {}
        reward = self.returnRewardCov(currentCoverage, self.rootTreeAdtNode.name)

        done = False
        if currentCoverage >= 90:
            done = True
        return reward, done, (currentCoverage / 100), {}


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
            variableDecl = resolveNodeViaType(value["$type"], value, self.resolverUtil)
            self.arguments[variableDecl.variable.variableName] = variableDecl

    def parseLoadedJsonIntoTree(self):
        self.rootTreeAdtNode = FunctionDeclarationStatement(self.rootAdtNode["$id"],
                                                            self.rootAdtNode["ReturnType"],
                                                            self.rootAdtNode["Name"], self.rootAdtNode["Arguments"],
                                                            self.rootAdtNode["Body"], self.resolverUtil)

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
                lists = self.rootTreeAdtNode.accept(self.vectorizationVisitor)
                lists = [x for x in lists if x != []]
                numOfTimes = int(round(len(lists)) ** (1 / 4)) + 1
                for x in range(numOfTimes):
                    toBeAppended = deepcopy(lists)
                    lists = lists + toBeAppended
                tableRows.append(lists)
            self.listOfTableVectors.append(tableRows)

    def prepareVectorsForRowsConv(self):
        for table in self.listOfTables:
            tableRows = []
            # Extract values for each column according to one row
            for row in table:
                dictForRow = self.mergeDictsInRow(row)
                self.vectorizationVisitor = SampleVisitorEnv(enviromentWalkerContext(), dictForRow, self.expressions)
                mainNode = self.rootTreeAdtNode.accept(self.vectorizationVisitor)
                tableRows.append(mainNode)
            self.listOfTableVectors.append(tableRows)

    def initializeArgumentValues(self):
        for argument in self.arguments:
            self.argumentValues[self.arguments[argument].variable.variableName] = 0

    def initializeArgumentValuesCov(self):
        self.argumentMatrix = []
        totalRows = 0
        for table in self.listOfTables:
            totalRows += len(table)
        self.totalRows = totalRows
        for row in range(totalRows):
            currentRow = []
            for argument in self.arguments:
                currentRow.append(0)
            self.argumentMatrix.append(currentRow)

    def mergeDictsInRow(self, row):
        dictOfCond = {}
        keys = []
        finalDict = {}
        for entry in row:
            for key in entry.keys():
                if not key in keys:
                    keys.append(key)
                    finalDict[key] = entry[key]
                else:
                    if key in dictOfCond:
                        dictOfCond[key] += 1
                    else:
                        dictOfCond[key] = 0
                    newkey = key + str(dictOfCond[key])
                    finalDict[newkey] = entry[key]
        return finalDict

    def returnRewardCov(self, coverageValue, function_name=None):
        if function_name is not None and function_name not in self.dict_of_max_r:
            self.dict_of_max_r[function_name] = coverageValue
        if function_name is not None and self.dict_of_max_r[function_name] < coverageValue:
            self.dict_of_max_r[function_name] = coverageValue
        return self.returnRewardPoly(coverageValue, function_name) # for the negative reward, switch to rewardPoly

    def returnGreedyNegativeReward(self, function_name, coverageValue):
        expected_reward = (coverageValue - self.dict_of_max_r[function_name]) / 100
        return expected_reward

    def returnRewardPoly(self, coverageValue, function_name=None):
        expected_reward = (-9.70e-06 * (coverageValue ** (6))) + (0.00269 * (coverageValue ** (5))) - (0.2743 * (coverageValue ** (4))) + (12.781 * (coverageValue ** (3))) - (266.2 * (coverageValue ** (2))) + (2164.2 * coverageValue) - 1754.7
        return expected_reward / 103665.3
