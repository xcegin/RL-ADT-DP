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
from ADT.Visitors.ABCVisitor import ABCVisitor
from ADT.Visitors.ConditionSolverVisitor import ConditionSolverVisitor
from Environment.Utils import getTypeOfExpression
from Environment import Utils
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext


# TODO: consider variable types with involvement like 0 1 2 for given argument
#  (if route of argument multiplying is taken)
class SampleVisitor(ABCVisitor):

    def __init__(self, Context, rowExpressionValues, expressions):
        super().__init__(Context)
        self.rowExpressionValues = rowExpressionValues
        self.expressions = expressions

    def reset(self):
        self.context = enviromentWalkerContext()

    def traverse_tree(self, startNode):
        queue = [(startNode, None)]
        samples = []
        while queue:
            node = queue.pop(0)
            if node[0] is None:
                continue
            children = node[0].accept(self)
            sample = {
                    'node': self.get_name(node[0]),
                    'parent': None if node[1] is None else self.get_name(node[1]),
                    'children': [self.get_name(child) for child in children]
                }  # TODO: Unknown node pri function declaration check
            samples.append(sample)
            for child in children:
                if child is not None:
                    queue.append((child, node[0]))
        return samples

    def get_name(self, node):
        if isinstance(node, BinaryOperator) or isinstance(node, UnaryOperator):
            return type(node).__name__ + str(node.operation)
        elif isinstance(node, LoopNode) or isinstance(node, IfNode):
            return type(node).__name__ + self.resolve_expression(node)
        else:
            return type(node).__name__

    def visit_loop(self, loopNode: LoopNode):
        expression = self.expressions[loopNode.id]
        children = []
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        if isConditionTrue:
            children = [loopNode.condition, loopNode.nodeBlock]
        else:
            children = [loopNode.condition, loopNode.nodeBlock]
        return children

    def visit_forloop(self, forLoop: ForLoop):
        expression = self.expressions[forLoop.id]
        children = [forLoop.nodeInit, forLoop.condition, forLoop.nodeAfter]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        children.append(forLoop.nodeBlock)
        return children

    def visit_assigment(self, assigment: AssignmentStatement):
        return assigment.returnChildren()

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        return binaryOperator.returnChildren()

    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        return variableDeclaration.returnChildren()

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        return unaryOperator.returnChildren()

    def visit_statement(self, statementNode: StatementNode):
        return statementNode.returnChildren()

    def visit_variable(self, variableNode: VariableNode):
        return variableNode.returnChildren()

    def visit_functioncall(self, functioncall: FunctionCall):
        return functioncall.returnChildren()

    def visit_ifnode(self, ifNode: IfNode):
        children = [ifNode.condition]
        expression = self.expressions[ifNode.id]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        children.append(ifNode.nodeThen)
        if ifNode.nodeElse is not None:
            children.append(ifNode.nodeElse)
        return children

    def visit_literal(self, literalNode: LiteralNode):
        return []

    def visit_sequence(self, sequence: SequenceNode):
        return sequence.returnChildren()

    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        return functionDecl.returnChildren()

    def visit_unknown(self, unknownNode: UnknownNode):
        return []

    def resolve_expression(self, node):
        expression = self.expressions[node.id]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        if isConditionTrue:
            return str(1)
        else:
            return str(0)
