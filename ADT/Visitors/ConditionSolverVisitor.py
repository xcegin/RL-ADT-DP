from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.LoopNode import LoopNode
from ADT.Operators.BinaryLogicalOperator import BinaryLogicalOperator
from ADT.Operators.BinaryOperator import BinaryOperator
from ADT.Operators.ComparisonOperator import ComparisonOperator
from ADT.Operators.UnaryOperator import UnaryOperator
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.FunctionCall import FunctionCall
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
        self.isRoot = True

    def visit_loop(self, loopNode: LoopNode):
        pass

    def visit_forloop(self, forLoop: ForLoop):
        pass

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        if isinstance(binaryOperator, BinaryLogicalOperator):
            tmpExpression = ""
            self.isRoot = False
            if self.checkIfIsComposite(binaryOperator.leftOperand):
                length = len(self.expression)
                binaryOperator.leftOperand.accept(self)
                self.expression = self.expression[:length] + leftBracket + \
                                  self.expression[length:] + rightBracket
            else:
                simpleExpression = binaryOperator.leftOperand.accept(self)
                self.simpleExpressions.append(simpleExpression)
                self.expression += simpleExpression
                tmpExpression += simpleExpression

            self.expression += space + binaryOperator.resolveOperationToString() + space

            if self.checkIfIsComposite(binaryOperator.rightOperand):
                length = len(self.expression)
                binaryOperator.rightOperand.accept(self)
                self.expression = self.expression[:length] + leftBracket + rightBracket + \
                                  self.expression[length:]
            else:
                simpleExpression = binaryOperator.rightOperand.accept(self)
                self.simpleExpressions.append(simpleExpression)
                self.expression += simpleExpression
                tmpExpression += simpleExpression
            return tmpExpression

        else:
            expression = binaryOperator.leftOperand.accept(self)
            expression += space + binaryOperator.resolveOperationToString()
            expression += space + binaryOperator.rightOperand.accept(self)
            if self.expression == "" and self.isRoot:
                self.simpleExpressions.append(expression)
                self.expression += expression
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

    def visit_functioncall(self, functioncall: FunctionCall):
        pass

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        pass

    def isConditionTrue(self):
        for expression in self.simpleExpressions:
            self.expression = self.expression.replace(expression, str(self.rowExpressionValues[expression]))
        self.expression = self.expression.replace("And", "and")
        self.expression = self.expression.replace("Or", "or")
        return eval(self.expression)

    def checkIfIsComposite(self, node):
        if isinstance(node, BinaryLogicalOperator) or isinstance(node, ComparisonOperator):
            if isinstance(node.leftOperand, BinaryLogicalOperator) or isinstance(node.leftOperand, ComparisonOperator) \
                    or isinstance(node.rightOperand, BinaryLogicalOperator) or \
                    isinstance(node.leftOperand, ComparisonOperator):
                return True
            else:
                return False
        else:
            return False
