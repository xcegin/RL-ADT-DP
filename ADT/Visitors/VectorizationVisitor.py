from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.LoopNode import LoopNode
from ADT.Operators.BinaryOperator import BinaryOperator
from ADT.Operators.UnaryOperator import UnaryOperator
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.StatementNode import StatementNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.Variables.VariableNode import VariableNode
from ADT.Visitors.ABCVisitor import ABCVisitor
from ADT.Visitors.ConditionSolverVisitor import ConditionSolverVisitor
from Enviroment.enviromentWalkerRedLabel import enviromentWalkerContext


class VectorizationVisitor(ABCVisitor):

    def __init__(self, Context, rowExpressionValues):
        super().__init__(Context)
        self.rowExpressionValues = rowExpressionValues

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
        # TODO: this should be resolved into data dependecies
        assigment.variable.accept(self)
        assigment.value.accept(self)

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        binaryOperator.leftOperand.accept(self)
        binaryOperator.rightOperand.accept(self)

    #TODO: compose into data dependencies
    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        variableDeclaration.variable.accept(self)
        variableDeclaration.variableType.accept(self)

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        unaryOperator.operand.accept(self)

    #TODO: more types of statements
    def visit_statement(self, statementNode: StatementNode):
        pass

    def visit_variable(self, variableNode: VariableNode):
        pass

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
        functionDecl.body.accept(self)