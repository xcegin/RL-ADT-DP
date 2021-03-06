from ADT.IfNode import IfNode
from ADT.LiteralNode import LiteralNode
from ADT.Loops.DoLoop import DoLoop
from ADT.Loops.ForLoop import ForLoop
from ADT.Loops.WhileLoop import WhileLoop
from ADT.Operators.BinaryArithmeticOperator import BinaryArithmeticOperator
from ADT.Operators.BinaryBitwiseOperator import BinaryBitwiseOperator
from ADT.Operators.BinaryLogicalOperator import BinaryLogicalOperator
from ADT.Operators.ComparisonOperator import ComparisonOperator
from ADT.Operators.UnaryArithmeticOperator import UnaryArithmeticOperator
from ADT.Operators.UnaryLogicalOperator import UnaryLogicalOperator
from ADT.Operators.UnaryVariableOperator import UnaryVariableOperator
from ADT.SequenceNode import SequenceNode
from ADT.Statements.AssigmentStatement import AssignmentStatement
from ADT.Statements.BreakStatement import BreakStatement
from ADT.Statements.FunctionCall import FunctionCall
from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
from ADT.Statements.ReturnStatement import ReturnStatement
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.UnknowNode import UnknownNode
from ADT.Variables.ArraySubscriptVariable import ArraySubscriptVariable
from ADT.Variables.FieldReferenceVariable import FieldReferenceVariable
from ADT.Variables.OperatorVariable import OperatorVariable
from ADT.Variables.SimpleVariable import SimpleVariable
from ADT.Variables.TypeDefinition import TypeDefinition


class ResolverUtil:
    def __init__(self):
        self.variableDeclarations = {}
        self.variableNameDecl = {}
        self.mainFuncName = None

    def tryResolveVariableDeclarationStatement(self, node):
        if "VariableDeclaration" in node:
            variableDeclaration = node["VariableDeclaration"]
            if variableDeclaration is None:
                return None
            if "$id" in variableDeclaration:
                numOfRef = variableDeclaration["$id"]
                if numOfRef in self.variableDeclarations:
                    return self.variableDeclarations[numOfRef]
                else:
                    return None
            else:
                return None
        else:
            return None

    def resolveVarDecl(self, node):
        variableDeclaration = self.tryResolveVariableDeclarationStatement(node)
        if variableDeclaration is None:
            variableDeclaration = self.variableNameDecl[node["VariableName"]]
        else:
            self.variableNameDecl[node["VariableName"]] = variableDeclaration
        return variableDeclaration


def resolveType(type):
    startIndex = type.find('[')
    if startIndex > -1:
        endIndex = type.find(']')
        type = type[startIndex:endIndex]
        type = type.replace("[", "")
        type = type.replace("]", "")

    givenType = type.split(',')[0]
    return givenType.split('.')[-1]


def resolveNodeViaType(type, node, resolver_util):
    type = resolveType(type)
    if type == "VariableDeclarationStatement":
        variableDeclarationStatement = VariableDeclarationStatement(node["$id"], node["VariableType"],
                                                                    node["InitialValue"])
        resolver_util.variableDeclarations[node["$id"]] = variableDeclarationStatement
        variableDeclarationStatement.variable = resolveNodeViaType(node["Variable"]["$type"], node["Variable"],
                                                                   resolver_util)
        return resolver_util.variableDeclarations[node["$id"]]
    # ADT Nodes
    elif type == "IfNode":
        return IfNode(node["$id"], node["Condition"], node["NodeThen"], resolver_util, node["NodeElse"])
    elif type == "LiteralNode":
        return LiteralNode(node["$id"], node["Value"], node["Kind"])
    elif type == "SequenceNode" or type == "IAdtNode":
        return SequenceNode("sequenceNode", node, resolver_util)
    # Statement Nodes
    elif type == "AssignmentStatement":
        return AssignmentStatement(node["$id"], node["Variable"], node["Value"], resolver_util)
    elif type == "BreakStatement":
        return BreakStatement(node["$id"])
    elif type == "FunctionCall":
        if node["Name"] == resolver_util.mainFuncName:
            return FunctionCall(node["$id"], node["Name"], node["Arguments"], None, resolver_util)
        return FunctionCall(node["$id"], node["Name"], node["Arguments"], node["FunctionDeclaration"], resolver_util)
    elif type == "FunctionDeclarationStatement":
        return FunctionDeclarationStatement(node["$id"], node["ReturnType"], node["Name"],
                                            node["Arguments"], node["Body"], resolver_util)
    elif type == "ReturnStatement":
        return ReturnStatement(node["$id"], node["Value"], resolver_util)
    # Variable Nodes
    elif type == "ArraySubscriptVariable":
        variableDeclaration = resolver_util.resolveVarDecl(node)
        return ArraySubscriptVariable(node["$id"], node["VariableName"], node["Array"], node["Subscript"],
                                      resolver_util,
                                      variableDeclaration)
    elif type == "FieldReferenceVariable":
        variableDeclaration = resolver_util.resolveVarDecl(node)
        return FieldReferenceVariable(node["$id"], node["VariableName"], node["Variable"], node["Dereference"],
                                      node["Field"], resolver_util,
                                      variableDeclaration)
    elif type == "OperatorVariable":
        variableDeclaration = resolver_util.resolveVarDecl(node)
        return OperatorVariable(node["$id"], node["VariableName"], node["Operator"], resolver_util, variableDeclaration)
    elif type == "SimpleVariable":
        variableDeclaration = resolver_util.resolveVarDecl(node)
        return SimpleVariable(node["$id"],
                              node["VariableName"], node["IsReference"], node["IsDefinition"], node["IsDeclaration"],
                              resolver_util,
                              variableDeclaration)
    elif type == "TypeDefinition":
        return TypeDefinition(node["$id"], node["TypeName"], node["PointerDimension"], node["ArrayDimension"],
                              node["ArrayDimensionSize"],
                              node["Modifiers"], node["TypeNode"])
    # Loop Nodes
    elif type == "DoLoop":
        return DoLoop(node["$id"], node["Condition"], node["NodeBlock"], resolver_util)
    elif type == "ForLoop":
        return ForLoop(node["$id"], node["NodeInit"], node["Condition"], node["NodeAfter"], node["NodeBlock"],
                       resolver_util)
    elif type == "WhileLoop":
        return WhileLoop(node["$id"], node["Condition"], node["NodeBlock"], resolver_util)
    # Operator nodes
    elif type == "BinaryArithmeticOperator":
        return BinaryArithmeticOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"],
                                        resolver_util)
    elif type == "BinaryBitwiseOperator":
        return BinaryBitwiseOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"],
                                     resolver_util)
    elif type == "BinaryLogicalOperator":
        return BinaryLogicalOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"],
                                     resolver_util)
    elif type == "ComparisonOperator":
        return ComparisonOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"],
                                  resolver_util)
    elif type == "UnaryArithmeticOperator":
        return UnaryArithmeticOperator(node["$id"], node["Operation"], node["Operand"], resolver_util)
    elif type == "UnaryBitwiseOperator":
        return UnaryArithmeticOperator(node["$id"], node["Operation"], node["Operand"], resolver_util)
    elif type == "UnaryLogicalOperator":
        return UnaryLogicalOperator(node["$id"], node["Operation"], node["Operand"], resolver_util)
    elif type == "UnaryVariableOperator":
        return UnaryVariableOperator(node["$id"], node["Operation"], node["Operand"], resolver_util)
    else:
        return UnknownNode(node["$id"])


def getNumOfReasonableNodes(node):
    if node['node'] == "VariableDeclarationStatement":
        return getNumFromChildren(node['children']) + 1
    # ADT Nodes
    elif node['node'] == "IfNode":
        return getNumFromChildren(node['children']) + 2
    elif node['node'] == "SequenceNode":
        return getNumFromChildren(node['children'])
    elif node['node'] == "LiteralNode":
        return getNumFromChildren(node['children']) + 1
    # Statement Nodes
    elif node['node'] == "AssignmentStatement":
        return getNumFromChildren(node['children']) + 2
    elif node['node'] == "BreakStatement":
        return getNumFromChildren(node['children'])
    elif node['node'] == "FunctionCall":
        return getNumFromChildren(node['children']) + 2
    elif node['node'] == "FunctionCallRecursion":
        return getNumFromChildren(node['children']) + 4
    elif node['node'] == "FunctionDeclarationStatement":
        return getNumFromChildren(node['children']) + 1
    elif node['node'] == "ReturnStatement":
        return getNumFromChildren(node['children']) + 1
    # Variable Nodes
    elif "Variable" in node['node']:
        return getNumFromChildren(node['children']) + 1
    elif "TypeDefinition" in node['node']:
        return getNumFromChildren(node['children']) + 1
    # Loop Nodes
    elif "Loop" in node['node']:
        return getNumFromChildren(node['children']) + 4
    # Operator nodes
    elif "Operator" in node['node']:
        return getNumFromChildren(node['children']) + 3
    else:
        return getNumFromChildren(node['children'])


def getNumFromChildren(children):
    num = 0
    for child in children:
        tmp = getNumOfReasonableNodes(child)
        if tmp is None:
            continue
        num += tmp
    return num
