from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.LoopNode import LoopNode
from ADT.Operators.BinaryLogicalOperator import BinaryLogicalOperator
from ADT.Operators.BinaryOperator import BinaryOperator
from ADT.Operators.ComparisonOperator import ComparisonOperator
from ADT.Operators.UnaryOperator import UnaryOperator
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.StatementNode import StatementNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.Variables.VariableNode import VariableNode
from ADT.Visitors.ABCVisitor import ABCVisitor

space = " "
leftBracket = "("
rightBracket = ")"


class ConditionSolverVisitor(ABCVisitor):

    def __init__(self, Context, rowExpressionValues):
        super().__init__(Context)
        self.simpleExpressions = []
        self.expression = ""
        self.rowExpressionValues = rowExpressionValues

    def visit_loop(self, loopNode: LoopNode):
        pass

    def visit_forloop(self, forLoop: ForLoop):
        pass

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        if isinstance(binaryOperator, BinaryLogicalOperator):
            if self.checkIfIsComposite(binaryOperator.leftOperand):
                length = len(self.expression)
                composite = binaryOperator.leftOperand.accept(self)
                self.expression = self.expression[:length] + leftBracket + composite + rightBracket + \
                                  self.expression[length:]
            else:
                simpleExpression = binaryOperator.leftOperand.accept(self)
                self.simpleExpressions.append(simpleExpression)
                self.expression = simpleExpression
                return simpleExpression

            self.expression += space + binaryOperator.resolveOperationToString() + space

            if self.checkIfIsComposite(binaryOperator.rightOperand):
                length = len(self.expression)
                composite = binaryOperator.rightOperand.accept(self)
                self.expression = self.expression[:length] + leftBracket + composite + rightBracket + \
                                  self.expression[length:]
            else:
                simpleExpression = binaryOperator.rightOperand.accept(self)
                self.simpleExpressions.append(simpleExpression)
                self.expression = simpleExpression
                return simpleExpression

        else:
            expression = binaryOperator.leftOperand.accept(self)
            expression += space + binaryOperator.resolveOperationToString()
            expression += space + binaryOperator.rightOperand.accept(self)
            if self.expression == "":
                self.simpleExpressions.append(expression)
                self.expression = expression
            return expression

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        expression = unaryOperator.operation + space + unaryOperator.operand.accept(self)
        if self.expression == "":
            self.simpleExpressions.append(expression)
            self.expression = expression
        return expression

    def visit_statement(self, statementNode: StatementNode):
        pass

    def visit_variable(self, variableNode: VariableNode):
        return variableNode.variableName

    def visit_ifnode(self, ifNode: IfNode):
        pass

    def visit_literal(self, literalNode: LiteralNode):
        return literalNode.value

    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        pass

    def visit_assigment(self, assigment: AssignmentStatement):
        pass

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        pass

    def isConditionTrue(self):
        for expression in self.simpleExpressions:
            self.expression = self.expression.replace(expression, str(self.rowExpressionValues[expression]))
        return eval(self.expression)

    def checkIfIsComposite(self, node):
        if isinstance(node, BinaryLogicalOperator) or isinstance(node, ComparisonOperator):
            return True
        else:
            return False
