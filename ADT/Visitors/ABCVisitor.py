import abc
from abc import ABC

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
from ADT.UnknowNode import UnknownNode
from ADT.Variables.VariableNode import VariableNode


class ABCVisitor(ABC):
    def __init__(self, Context):
        self.context = Context

    @abc.abstractmethod
    def visit_loop(self, loopNode: LoopNode):
        pass

    @abc.abstractmethod
    def visit_forloop(self, forLoop: ForLoop):
        pass

    @abc.abstractmethod
    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        pass

    @abc.abstractmethod
    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        pass

    @abc.abstractmethod
    def visit_statement(self, statementNode: StatementNode):
        pass

    @abc.abstractmethod
    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        pass

    @abc.abstractmethod
    def visit_assigment(self, assigment: AssignmentStatement):
        pass

    @abc.abstractmethod
    def visit_functioncall(self, functioncall: FunctionCall):
        pass


    @abc.abstractmethod
    def visit_variable(self, variableNode: VariableNode):
        pass

    def visit_sequence(self, sequence: SequenceNode):
        for node in sequence.nodes:
            node.accept(self)

    @abc.abstractmethod
    def visit_ifnode(self, ifNode: IfNode):
        pass

    @abc.abstractmethod
    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        pass

    @abc.abstractmethod
    def visit_literal(self, literalNode: LiteralNode):
        pass

    def visit_unknown(self, unknownNode: UnknownNode):
        pass
