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


class SampleVisitor(ABCVisitor):

    def __init__(self, Context, rowExpressionValues, expressions, mainFuncName):
        super().__init__(Context)
        self.rowExpressionValues = rowExpressionValues
        self.expressions = expressions
        self.mainFuncName = mainFuncName
        self.global_expr = {}
        self.expr_id = {}

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
            if children is None:
                children = []
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
            if node.id in self.expr_id:
                return self.expr_id[node.id]
            else:
                self.expr_id[node.id] = type(node).__name__ + self.resolve_expression(node)
                return self.expr_id[node.id]
        elif isinstance(node, FunctionCall) and node.name == self.mainFuncName:
            return type(node).__name__ + 'Recursion'
        else:
            return type(node).__name__

    def visit_loop(self, loopNode: LoopNode):
        expression = self.expressions[loopNode.id]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            expression = self.resolve_name_expr(expression, False)
            if not expression["Token"] in self.rowExpressionValues:
                isConditionTrue = None
            else:
                isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            expression = self.resolve_name_expr(expression, False)
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        if isConditionTrue:
            children = [loopNode.condition, loopNode.nodeBlock]
        elif isConditionTrue is None:
            children = [loopNode.condition, loopNode.nodeBlock]
        else:
            children = [loopNode.condition]
        return children

    def visit_forloop(self, forLoop: ForLoop):
        expression = self.expressions[forLoop.id]
        children = [forLoop.nodeInit, forLoop.condition]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            expression = self.resolve_name_expr(expression, False)
            if not expression["Token"] in self.rowExpressionValues:
                isConditionTrue = None
            else:
                isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            expression = self.resolve_name_expr(expression, False)
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        if isConditionTrue or isConditionTrue is None:
            children.append(forLoop.nodeAfter)
            children.append(forLoop.nodeBlock)
        #children.append(forLoop.nodeBlock)
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
            expression = self.resolve_name_expr(expression, False)
            if not expression["Token"] in self.rowExpressionValues:
                isConditionTrue = None
            else:
                isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            expression = self.resolve_name_expr(expression, False)
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        if isConditionTrue == True:
            children.append(ifNode.nodeThen)
        elif isConditionTrue is None:
            children.append(ifNode.nodeThen)
            children.append(ifNode.nodeElse)
        else:
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
        if node.id not in self.expressions:
            return 'None'
        expression = self.expressions[node.id]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            expression = self.resolve_name_expr(expression, True)
            if not expression["Token"] in self.rowExpressionValues:
                isConditionTrue = None
            else:
                isConditionTrue = self.rowExpressionValues[expression["Token"]]
        else:
            expression = self.resolve_name_expr(expression, True)
            conditionSolver = ConditionSolverVisitor(expression,
                                                     self.rowExpressionValues,
                                                     self.expressions)
            isConditionTrue = conditionSolver.retrieveValueOfCondition()
        if isConditionTrue:
            return str(1)
        elif isConditionTrue is None:
            return str(None)
        else:
            return str(0)

    def resolve_name_expr(self, expression, flag):
        tokenirino = expression["Token"]
        if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
            expression["Token"] = self.retrieve_new_token(tokenirino, flag)
            return expression
        else:
            tmpDict = {}
            tmpToken = tokenirino.replace("And", "~")
            tmpToken = tmpToken.replace("Or", "~")
            tokens = tmpToken.split("~")
            for token in tokens:
                if token[-1:] == ' ':
                    token = token[:-1]
                if token[0] == ' ':
                    token = token[1:]
                new_token = self.retrieve_new_token(token, flag)
                tmpDict[token] = new_token
            for key in tmpDict.keys():
                tokenirino = tokenirino.replace(key, tmpDict[key])
            expression["Token"] = tokenirino
            return expression

    def retrieve_new_token(self, token, flag):
        if token in self.global_expr:
            if flag:
                return token + str(self.global_expr[token])
            toBeToken = token + str(self.global_expr[token])
            self.global_expr += 1
            return toBeToken
        else:
            if flag:
                return token
            self.global_expr[token] = 0
            return token
