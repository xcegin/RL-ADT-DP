from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.LoopNode import LoopNode
from ADT.Operators.BinaryArithmeticOperator import BinaryArithmeticOperator
from ADT.Operators.BinaryBitwiseOperator import BinaryBitwiseOperator
from ADT.Operators.BinaryLogicalOperator import BinaryLogicalOperator
from ADT.Operators.BinaryOperator import BinaryOperator
from ADT.Operators.ComparisonOperator import ComparisonOperator
from ADT.Operators.UnaryBitwiseOpeartor import UnaryBitwiseOperator
from ADT.Operators.UnaryOperator import UnaryOperator
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.FunctionCall import FunctionCall
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.ReturnStatement import ReturnStatement
from ADT.Statements.StatementNode import StatementNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.Variables.VariableNode import VariableNode
from ADT.Visitors.ABCVisitor import ABCVisitor
# TODO GENERAL EXCEPTION CATCHING AND LOGGER
bulgarianConstantPlusMinus = 1
bulgarianBitwiseOperation = 2
bulgarianConstantDivisionMultiply = 4


class AssigmentComplexityVisitor(ABCVisitor):

    def __init__(self, Context):
        super().__init__(Context)
        self.complexityOfCurrExpression = 0

    def visit_loop(self, loopNode: LoopNode):
        loopNode.condition.accept(self)
        loopNode.nodeBlock.accept(self)

    def visit_forloop(self, forLoop: ForLoop):
        forLoop.condition.accept(self)
        forLoop.nodeBlock.accept(self)
        forLoop.nodeInit.accept(self)
        forLoop.nodeAfter.accept(self)

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        if isinstance(binaryOperator, BinaryArithmeticOperator):
            if binaryOperator.operation < 2:
                self.complexityOfCurrExpression += bulgarianConstantPlusMinus
            else:
                self.complexityOfCurrExpression += bulgarianConstantDivisionMultiply
        if isinstance(binaryOperator, BinaryBitwiseOperator):
            self.complexityOfCurrExpression += bulgarianBitwiseOperation
        if isinstance(binaryOperator, BinaryLogicalOperator):
            self.complexityOfCurrExpression += bulgarianBitwiseOperation
        binaryOperator.leftOperand.accept(self)
        binaryOperator.rightOperand.accept(self)

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        if isinstance(unaryOperator, BinaryBitwiseOperator):
            self.complexityOfCurrExpression += bulgarianConstantPlusMinus
        elif isinstance(unaryOperator, UnaryBitwiseOperator):
            self.complexityOfCurrExpression += bulgarianConstantPlusMinus
        else:
            self.complexityOfCurrExpression += bulgarianBitwiseOperation
        unaryOperator.operand.accept(self)

    def visit_statement(self, statementNode: StatementNode):
        if isinstance(statementNode, ReturnStatement):
            statementNode.value.accept(self)

    def visit_variable(self, variableNode: VariableNode):
        pass

    def visit_ifnode(self, ifNode: IfNode):
        ifNode.condition.accept(self)
        ifNode.nodeThen.accept(self)
        if ifNode.nodeElse is not None:
            ifNode.nodeElse.accept(self)

    def visit_literal(self, literalNode: LiteralNode):
        return literalNode.value

    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        if variableDeclaration.initialValue is not None:
            variableDeclaration.initialValue.accept(self)

    def visit_assigment(self, assigment: AssignmentStatement):
        assigment.variable.accept(self)
        assigment.value.accept(self)

    def visit_functioncall(self, functioncall: FunctionCall):
        for argument in functioncall.arguments:
            argument.accept(self)
        functioncall.functionDeclaration.accept(self)

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        functionDecl.body.accept(self)
