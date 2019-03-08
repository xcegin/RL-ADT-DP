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


class SampleVisitorEnvWithConv(ABCVisitor):

    def __init__(self, Context, mainFuncName):
        super().__init__(Context)
        self.mainFuncName = mainFuncName

    def reset(self):
        self.context = enviromentWalkerContext()

    def get_name(self, node):
        if isinstance(node, BinaryOperator) or isinstance(node, UnaryOperator):
            return type(node).__name__ + str(node.operation)
        elif isinstance(node, FunctionCall) and node.name == self.mainFuncName:
            return type(node).__name__ + 'Recursion'
        else:
            return type(node).__name__

    def visit_loop(self, loopNode: LoopNode):
        children = []
        children.append(self.resolveParent(loopNode, loopNode.condition.accept(self)))
        # expression = self.expressions[loopNode.id]
        # if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
        #     isConditionTrue = self.rowExpressionValues[expression["Token"]]
        # else:
        #     conditionSolver = ConditionSolverVisitor(expression,
        #                                              self.rowExpressionValues,
        #                                              self.expressions)
        #     isConditionTrue = conditionSolver.retrieveValueOfCondition()
        children.append(self.resolveParent(loopNode, loopNode.nodeBlock.accept(self)))
        return {
            'node': self.get_name(loopNode),
            'parent': None,
            'children': children
        }

    def visit_forloop(self, forLoop: ForLoop):
        children = []
        children.append(self.resolveParent(forLoop, forLoop.nodeInit.accept(self)))
        children.append(self.resolveParent(forLoop, forLoop.condition.accept(self)))
        children.append(self.resolveParent(forLoop, forLoop.nodeAfter.accept(self)))
        # expression = self.expressions[forLoop.id]
        # if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
        #     isConditionTrue = self.rowExpressionValues[expression["Token"]]
        # else:
        #     conditionSolver = ConditionSolverVisitor(expression,
        #                                              self.rowExpressionValues,
        #                                              self.expressions)
        #     isConditionTrue = conditionSolver.retrieveValueOfCondition()
        children.append(self.resolveParent(forLoop, forLoop.nodeBlock.accept(self)))
        return {
            'node': self.get_name(forLoop),
            'parent': None,
            'children': children
        }

    def visit_assigment(self, assigment: AssignmentStatement):
        children = [self.resolveParent(assigment, assigment.variable.accept(self)),
                    self.resolveParent(assigment, assigment.value.accept(self))]
        return {
            'node': self.get_name(assigment),
            'parent': None,
            'children': children
        }

    def visit_binaryoperator(self, binaryOperator: BinaryOperator):
        children = [self.resolveParent(binaryOperator, binaryOperator.rightOperand.accept(self)),
                    self.resolveParent(binaryOperator, binaryOperator.leftOperand.accept(self))]
        return {
            'node': self.get_name(binaryOperator),
            'parent': None,
            'children': children
        }

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

    def visit_unaryoperator(self, unaryOperator: UnaryOperator):
        children = [self.resolveParent(unaryOperator, unaryOperator.operand.accept(self))]
        return {
            'node': self.get_name(unaryOperator),
            'parent': None,
            'children': children
        }

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

    def visit_ifnode(self, ifNode: IfNode):
        children = [self.resolveParent(ifNode, ifNode.condition.accept(self))]
        # expression = self.expressions[ifNode.id]
        # if getTypeOfExpression(expression["$type"]) != Utils.COMPOSITE_EXPRESSION:
        #     isConditionTrue = self.rowExpressionValues[expression["Token"]]
        # else:
        #     conditionSolver = ConditionSolverVisitor(expression,
        #                                              self.rowExpressionValues,
        #                                              self.expressions)
        #     isConditionTrue = conditionSolver.retrieveValueOfCondition()
        children.append(self.resolveParent(ifNode, ifNode.nodeThen.accept(self)))
        if ifNode.nodeElse is not None:
            children.append(self.resolveParent(ifNode, ifNode.nodeElse.accept(self)))
        return {
                    'node': self.get_name(ifNode),
                    'parent': None,
                    'children': children
                }

    def visit_literal(self, literalNode: LiteralNode):
        return {
                    'node': self.get_name(literalNode),
                    'parent': None,
                    'children': []
                }

    def visit_sequence(self, sequence: SequenceNode):
        children = []
        for node in sequence.nodes:
            children.append(self.resolveParent(sequence, node.accept(self)))
        return {
                    'node': self.get_name(sequence),
                    'parent': None,
                    'children': children
                }

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

    def visit_typeDefinition(self, typeDef: TypeDefinition):
        return {
            'node': self.get_name(typeDef),
            'parent': None,
            'children': []
        }

    def visit_unknown(self, unknownNode: UnknownNode):
        return {
                    'node': self.get_name(unknownNode),
                    'parent': None,
                    'children': []
                }

    def resolveParent(self, parent, child):
        child['parent'] = self.get_name(parent)
        return child
