from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.LoopNode import LoopNode
from ADT.Operators.BinaryOperator import BinaryOperator
from ADT.Operators.UnaryOperator import UnaryOperator
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.FunctionCall import FunctionCall
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.StatementNode import StatementNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.Variables.VariableNode import VariableNode
from ADT.Visitors.ABCVisitor import ABCVisitor
from ADT.Visitors.ConditionSolverVisitor import ConditionSolverVisitor
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext


class DataDependenciesVisitor(ABCVisitor):

    def __init__(self, Context, rowExpressionValues):
        super().__init__(Context)
        self.rowExpressionValues = rowExpressionValues
        self.isInModifyingVariableState = False
        self.lastAssignedVariable = None

    def reset(self):
        self.context = enviromentWalkerContext()

    def visit_loop(self, loopNode: LoopNode):
        conditionSolver = ConditionSolverVisitor(enviromentWalkerContext(), self.rowExpressionValues)
        loopNode.condition.accept(conditionSolver)
        loopNode.condition.accept(self)
        if conditionSolver.isConditionTrue():
            loopNode.nodeBlock.accept(self)
        else:
            pass

    def visit_forloop(self, forLoop: ForLoop):
        conditionSolver = ConditionSolverVisitor(enviromentWalkerContext(), self.rowExpressionValues)
        forLoop.nodeInit.accept(self)
        forLoop.condition.accept(conditionSolver)
        forLoop.condition.accept(self)
        if conditionSolver.isConditionTrue():
            forLoop.nodeBlock.accept(self)
            forLoop.nodeAfter(self)
        else:
            pass

    def visit_assigment(self, assigment: AssignmentStatement):
        self.isInModifyingVariableState = True
        self.lastAssignedVariable = assigment.variable
        assigment.variable.accept(self)
        assigment.value.accept(self)
        self.isInModifyingVariableState = False

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        if self.isInModifyingVariableState:
            if binaryOperator.leftOperand is VariableNode:
                self.context.dataDependencies[self.lastAssignedVariable.name].append(binaryOperator.leftOperand.name)
            if binaryOperator.rightOperand is VariableNode:
                self.context.dataDependencies[self.lastAssignedVariable.name].append(binaryOperator.rightOperand.name)
        binaryOperator.leftOperand.accept(self)
        binaryOperator.rightOperand.accept(self)

    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        if variableDeclaration.variable.variableName not in self.context.dataDependencies:
            self.context.dataDependencies[variableDeclaration.variable.variableName] = []
        variableDeclaration.variable.accept(self)
        variableDeclaration.variableType.accept(self)

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        if self.isInModifyingVariableState:
            if unaryOperator.operand is VariableNode:
                self.context.dataDependencies[self.lastAssignedVariable.name].append(unaryOperator.operand.name)
        unaryOperator.operand.accept(self)

    def visit_statement(self, statementNode: StatementNode):
        pass

    def visit_variable(self, variableNode: VariableNode):
        if variableNode.variableName not in self.context.dataDependencies:
            self.context.dataDependencies[variableNode.variableName] = []

    def visit_ifnode(self, ifNode: IfNode):
        conditionSolver = ConditionSolverVisitor(enviromentWalkerContext(), self.rowExpressionValues)
        ifNode.condition.accept(conditionSolver)
        ifNode.condition.accept(self)
        if conditionSolver.isConditionTrue():
            ifNode.nodeThen.accept(self)
        else:
            ifNode.nodeElse.accept(self)

    def visit_literal(self, literalNode: LiteralNode):
        pass

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        for argument in functionDecl.arguments:
            argument.accept(self)
        functionDecl.body.accept(self)

    def visit_functioncall(self, functioncall: FunctionCall):
        for argument in functioncall.arguments:
            argument.accept(self)
