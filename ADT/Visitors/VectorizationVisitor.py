from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.LoopNode import LoopNode
from ADT.Operators.BinaryOperator import BinaryOperator
from ADT.Operators.UnaryOperator import UnaryOperator
from ADT.SequenceNode import SequenceNode
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.FunctionCall import FunctionCall
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.StatementNode import StatementNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.Variables.VariableNode import VariableNode
from ADT.Visitors.ABCVisitor import ABCVisitor
from ADT.Visitors.ConditionSolverVisitor import ConditionSolverVisitor
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext

if_embedding = 1
loop_embedding = 4


class VectorizationVisitor(ABCVisitor):

    def __init__(self, Context, rowExpressionValues, arguments):
        super().__init__(Context)
        self.rowExpressionValues = rowExpressionValues
        self.embedding = 0
        self.functionName = ""
        self.numOfStaticRecursionCalls = 0
        self.currentArgumentVectorDependency = None
        self.arguments = arguments

    def reset(self):
        self.context = enviromentWalkerContext()
        self.embedding = 0
        self.functionName = ""
        self.numOfStaticRecursionCalls = 0
        self.currentArgumentVectorDependency = None

    def visit_loop(self, loopNode: LoopNode):
        conditionSolver = ConditionSolverVisitor(enviromentWalkerContext(), self.rowExpressionValues)
        loopNode.condition.accept(conditionSolver)
        if conditionSolver.isConditionTrue():
            self.embedding = self.embedding + loop_embedding
            resultVectors = loopNode.return_vector(self)
            self.embedding = self.embedding - loop_embedding
            return resultVectors
        else:
            pass

    def visit_forloop(self, forLoop: ForLoop):
        conditionSolver = ConditionSolverVisitor(enviromentWalkerContext(), self.rowExpressionValues)
        forLoop.condition.accept(conditionSolver)
        if conditionSolver.isConditionTrue():
            self.embedding = self.embedding + loop_embedding
            resultVectors = forLoop.return_vector(self)
            self.embedding = self.embedding - loop_embedding
            return resultVectors
        else:
            pass

    def visit_assigment(self, assigment: AssignmentStatement):
        return assigment.return_vector(self)

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        return binaryOperator.return_vector(self)

    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        return variableDeclaration.return_vector(self)

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        return unaryOperator.return_vector(self)

    def visit_statement(self, statementNode: StatementNode):
        return statementNode.return_vector(self)

    def visit_variable(self, variableNode: VariableNode):
        return variableNode.return_vector(self)

    def visit_functioncall(self, functioncall: FunctionCall):
        if self.functionName == functioncall.name:
            self.numOfStaticRecursionCalls = self.numOfStaticRecursionCalls + 1
        return functioncall.return_vector(self)

    def visit_ifnode(self, ifNode: IfNode):
        list = []
        conditionSolver = ConditionSolverVisitor(enviromentWalkerContext(), self.rowExpressionValues)
        ifNode.condition.accept(conditionSolver)
        list = list + ifNode.condition.accept(self)
        self.embedding = self.embedding + if_embedding
        if conditionSolver.isConditionTrue():
            list = list + ifNode.nodeThen.accept(self)
        else:
            if ifNode.nodeElse is not None:
                list = list + ifNode.nodeElse.accept(self)
        self.embedding = self.embedding + if_embedding
        return list

    def visit_literal(self, literalNode: LiteralNode):
        return literalNode.return_vector(self)

    def visit_sequence(self, sequence: SequenceNode):
        list = []
        for node in sequence.nodes:
            list = list + node.return_vector(self)
        return list

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        self.functionName = functionDecl.name
        list = functionDecl.body.accept(self)
        return functionDecl.body.accept(self)
