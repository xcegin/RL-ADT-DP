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
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext


class RetrieveVariablesFromConditionVisitor(ABCVisitor):

    def __init__(self, Context):
        super().__init__(Context)
        self.currentArguments = []

    def reset(self):
        self.context = enviromentWalkerContext()
        self.currentArguments = []

    def visit_loop(self, loopNode: LoopNode):
        pass

    def visit_forloop(self, forLoop: ForLoop):
        pass

    def visit_assigment(self, assigment: AssignmentStatement):
        assigment.variable.accept(self)
        assigment.value.accept(self)

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        binaryOperator.leftOperand.accept(self)
        binaryOperator.rightOperand.accept(self)

    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        variableDeclaration.variable.accept(self)
        from ADT.ADTNode import ADTNode
        if variableDeclaration.initialValue is not None and isinstance(variableDeclaration.initialValue, ADTNode):
            variableDeclaration.initialValue.accept(self)

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        unaryOperator.operand.accept(self)

    def visit_statement(self, statementNode: StatementNode):
        pass

    def visit_variable(self, variableNode: VariableNode):
        self.currentArguments.append(variableNode.variableName)

    def visit_ifnode(self, ifNode: IfNode):
        pass

    def visit_literal(self, literalNode: LiteralNode):
        pass

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        pass

    def visit_functioncall(self, functioncall: FunctionCall):
        for argument in functioncall.arguments:
            argument.accept(self)
