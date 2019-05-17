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
from ADT.Statements.ReturnStatement import ReturnStatement
from ADT.Statements.StatementNode import StatementNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.UnknowNode import UnknownNode
from ADT.Variables.ArraySubscriptVariable import ArraySubscriptVariable
from ADT.Variables.FieldReferenceVariable import FieldReferenceVariable
from ADT.Variables.OperatorVariable import OperatorVariable
from ADT.Variables.TypeDefinition import TypeDefinition
from ADT.Variables.VariableNode import VariableNode
from ADT.Visitors.ABCVisitor import ABCVisitor
from ADT.Visitors.ConditionSolverVisitor import ConditionSolverVisitor
from Environment.Utils import getTypeOfExpression
from Environment import Utils
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext

class SampleVisitorEnv(ABCVisitor):

    def __init__(self, Context, rowExpressionValues, expressions):
        super().__init__(Context)
        self.rowExpressionValues = rowExpressionValues
        self.expressions = expressions
        self.global_expr = {}
        self.expr_id = {}

    def reset(self):
        self.context = enviromentWalkerContext()

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

    # Sample visitor loop node for the test case granularity
    def visit_loop(self, loopNode: LoopNode):
        children = []
        children.append(self.resolveParent(loopNode, loopNode.condition.accept(self)))
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
            children.append(self.resolveParent(loopNode, loopNode.nodeBlock.accept(self)))
            children = [loopNode.condition, loopNode.nodeBlock]
        elif isConditionTrue is None:
            children.append(self.resolveParent(loopNode, loopNode.nodeBlock.accept(self)))
        return {
            'node': self.get_name(loopNode),
            'parent': None,
            'children': children
        }

    # Sample visitor for loop node for the test case granularity
    def visit_forloop(self, forLoop: ForLoop):
        children = []
        children.append(self.resolveParent(forLoop, forLoop.condition.accept(self)))
        children.append(self.resolveParent(forLoop, forLoop.nodeInit.condition.accept(self)))
        expression = self.expressions[forLoop.id]
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
            children.append(self.resolveParent(forLoop, forLoop.nodeAfter.accept(self)))
            children.append(self.resolveParent(forLoop, forLoop.nodeBlock.accept(self)))
        return {
            'node': self.get_name(forLoop),
            'parent': None,
            'children': children
        }

    # Sample visitor assigment node for the test case granularity
    def visit_assigment(self, assigment: AssignmentStatement):
        children = [self.resolveParent(assigment, assigment.variable.accept(self)),
                    self.resolveParent(assigment, assigment.value.accept(self))]
        return {
            'node': self.get_name(assigment),
            'parent': None,
            'children': children
        }

    # Sample visitor binary operator node for the test case granularity
    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        children = [self.resolveParent(binaryOperator, binaryOperator.rightOperand.accept(self)),
                    self.resolveParent(binaryOperator, binaryOperator.leftOperand.accept(self))]
        return {
            'node': self.get_name(binaryOperator),
            'parent': None,
            'children': children
        }

    # Sample visitor variable declaration node for the test case granularity
    def visit_variabledeclaration(self, variableDeclaration: VariableDeclarationStatement):
        children = []
        children.append(self.resolveParent(variableDeclaration, variableDeclaration.variable.accept(self)))
        if variableDeclaration.initialValue is not None:
            children.append(self.resolveParent(variableDeclaration, variableDeclaration.initialValue.accept(self)))
        children.append(self.resolveParent(variableDeclaration, variableDeclaration.variableType.accept(self)))
        return {
            'node': self.get_name(variableDeclaration),
            'parent': None,
            'children': children
        }

    # Sample visitor unary operator node for the test case granularity
    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        children = [self.resolveParent(unaryOperator, unaryOperator.operand.accept(self))]
        return {
            'node': self.get_name(unaryOperator),
            'parent': None,
            'children': children
        }

    # Sample visitor statement node for the test case granularity
    def visit_statement(self, statementNode: StatementNode):
        if isinstance(statementNode, ReturnStatement):
            children = [self.resolveParent(statementNode, statementNode.value.accept(self))]
            return {
                'node': self.get_name(statementNode),
                'parent': None,
                'children': children
            }
        else:
            return {
                'node': self.get_name(statementNode),
                'parent': None,
                'children': []
            }

    # Sample visitor variable node for the test case granularity
    def visit_variable(self, variableNode: VariableNode):
        children = []
        if isinstance(variableNode, ArraySubscriptVariable):
            children.append(self.resolveParent(variableNode, variableNode.array.accept(self)))
            children.append(self.resolveParent(variableNode, variableNode.subscript.accept(self)))
            return {
                'node': self.get_name(variableNode),
                'parent': None,
                'children': children
            }
        elif isinstance(variableNode, FieldReferenceVariable):
            children.append(self.resolveParent(variableNode, variableNode.variable.accept(self)))
            return {
                'node': self.get_name(variableNode),
                'parent': None,
                'children': children
            }
        elif isinstance(variableNode, OperatorVariable):
            children += self.resolveParent(variableNode, variableNode.operator.accept(self))
            return {
                'node': self.get_name(variableNode),
                'parent': None,
                'children': children
            }
        else:
            return {
                'node': self.get_name(variableNode),
                'parent': None,
                'children': []
            }

    # Sample visitor function call node for the test case granularity
    def visit_functioncall(self, functioncall: FunctionCall):
        children = []
        for arguments in functioncall.arguments:
            children.append(self.resolveParent(functioncall, arguments.accept(self)))
        children.append(self.resolveParent(functioncall, functioncall.functionDeclaration.accept(self)))
        return {
            'node': self.get_name(functioncall),
            'parent': None,
            'children': children
        }

    # Sample visitor if node for the test case granularity
    def visit_ifnode(self, ifNode: IfNode):
        children = [self.resolveParent(ifNode, ifNode.condition.accept(self))]
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
            children.append(self.resolveParent(ifNode, ifNode.nodeThen.accept(self)))
        elif isConditionTrue is None:
            children.append(self.resolveParent(ifNode, ifNode.nodeThen.accept(self)))
            if ifNode.nodeElse is not None:
                children.append(self.resolveParent(ifNode, ifNode.nodeElse.accept(self)))
        else:
            if ifNode.nodeElse is not None:
                children.append(self.resolveParent(ifNode, ifNode.nodeElse.accept(self)))
        return {
            'node': self.get_name(ifNode),
            'parent': None,
            'children': children
        }

    # Sample visitor literal node for the test case granularity
    def visit_literal(self, literalNode: LiteralNode):
        return {
                    'node': self.get_name(literalNode),
                    'parent': None,
                    'children': []
                }

    # Sample visitor sequence node for the test case granularity
    def visit_sequence(self, sequence: SequenceNode):
        children = []
        for node in sequence.nodes:
            children.append(self.resolveParent(sequence, node.accept(self)))
        return {
                    'node': self.get_name(sequence),
                    'parent': None,
                    'children': children
                }

    # Sample visitor function declaration node for the test case granularity
    def visit_functiondeclaration(self, functionDecl: FunctionDeclarationStatement):
        children = [self.resolveParent(functionDecl, functionDecl.returnType.accept(self))]
        for arguments in functionDecl.arguments:
            children.append(self.resolveParent(functionDecl, arguments.accept(self)))
        children.append(self.resolveParent(functionDecl, functionDecl.body.accept(self)))
        return {
            'node': self.get_name(functionDecl),
            'parent': None,
            'children': children
        }

    # Sample visitor type definition node for the test case granularity
    def visit_typeDefinition(self, typeDef: TypeDefinition):
        return {
            'node': self.get_name(typeDef),
            'parent': None,
            'children': []
        }

    # Sample visitor loop unknown node for the test case granularity
    def visit_unknown(self, unknownNode: UnknownNode):
        return {
                    'node': self.get_name(unknownNode),
                    'parent': None,
                    'children': []
                }

    # Resolves the boolean value of the expression for given test case
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

    def resolveParent(self, parent, child):
        child['parent'] = self.get_name(parent)
        return child
