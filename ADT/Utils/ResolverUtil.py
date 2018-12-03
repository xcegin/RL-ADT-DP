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

variableDeclarations = {}
variableNameDecl = {}


def resolveType(type):
    startIndex = type.find('[')
    if startIndex > -1:
        endIndex = type.find(']')
        type = type[startIndex:endIndex]
        type = type.replace("[", "")
        type = type.replace("]", "")

    givenType = type.split(',')[0]
    return givenType.split('.')[-1]


def resetUtil():
    global variableDeclarations
    global variableNameDecl
    variableDeclarations = {}
    variableNameDecl = {}

def resolveNodeViaType(type, node):
    type = resolveType(type)
    if type == "VariableDeclarationStatement":
        variableDeclarationStatement = VariableDeclarationStatement(node["$id"], node["VariableType"],
                                                                    node["InitialValue"])
        variableDeclarations[node["$id"]] = variableDeclarationStatement
        variableDeclarationStatement.variable = resolveNodeViaType(node["Variable"]["$type"], node["Variable"])
        return variableDeclarations[node["$id"]]
    # ADT Nodes
    elif type == "IfNode":
        return IfNode(node["$id"], node["Condition"], node["NodeThen"], node["NodeElse"])
    elif type == "LiteralNode":
        return LiteralNode(node["$id"], node["Value"], node["Kind"])
    elif type == "SequenceNode" or type == "IAdtNode":
        return SequenceNode("sequenceNode", node)
    # Statement Nodes
    elif type == "AssignmentStatement":
        return AssignmentStatement(node["$id"], node["Variable"], node["Value"])
    elif type == "BreakStatement":
        return BreakStatement(node["$id"])
    elif type == "FunctionCall":
        return FunctionCall(node["$id"], node["Name"], node["Arguments"], node["FunctionDeclaration"])
    elif type == "FunctionDeclarationStatement":
        return FunctionDeclarationStatement(node["$id"], node["ReturnType"], node["Name"],
                                            node["Arguments"], node["Body"])
    elif type == "ReturnStatement":
        return ReturnStatement(node["$id"], node["Value"])
    # Variable Nodes
    elif type == "ArraySubscriptVariable":
        variableDeclaration = resolveVarDecl(node)
        return ArraySubscriptVariable(node["$id"], node["VariableName"], node["Array"], node["Subscript"],
                                      variableDeclaration)
    elif type == "FieldReferenceVariable":
        variableDeclaration = resolveVarDecl(node)
        return FieldReferenceVariable(node["$id"], node["VariableName"], node["Variable"], node["Dereference"],
                                      node["Field"],
                                      variableDeclaration)
    elif type == "OperatorVariable":
        variableDeclaration = resolveVarDecl(node)
        return OperatorVariable(node["$id"], node["VariableName"], node["Operator"], variableDeclaration)
    elif type == "SimpleVariable":
        variableDeclaration = resolveVarDecl(node)
        return SimpleVariable(node["$id"],
                              node["VariableName"], node["IsReference"], node["IsDefinition"], node["IsDeclaration"],
                              variableDeclaration)
    elif type == "TypeDefinition":
        return TypeDefinition(node["$id"], node["TypeName"], node["PointerDimension"], node["ArrayDimension"],
                              node["ArrayDimensionSize"],
                              node["Modifiers"], node["TypeNode"])
    # Loop Nodes
    elif type == "DoLoop":
        return DoLoop(node["$id"], node["Condition"], node["NodeBlock"])
    elif type == "ForLoop":
        return ForLoop(node["$id"], node["NodeInit"], node["Condition"], node["NodeAfter"], node["NodeBlock"])
    elif type == "WhileLoop":
        return WhileLoop(node["$id"], node["Condition"], node["NodeBlock"])
    # Operator nodes
    elif type == "BinaryArithmeticOperator":
        return BinaryArithmeticOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "BinaryArithmeticOperator":
        return BinaryBitwiseOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "BinaryLogicalOperator":
        return BinaryLogicalOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "ComparisonOperator":
        return ComparisonOperator(node["$id"], node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "UnaryArithmeticOperator":
        return UnaryArithmeticOperator(node["$id"], node["Operation"], node["Operand"])
    elif type == "UnaryBitwiseOperator":
        return UnaryArithmeticOperator(node["$id"], node["Operation"], node["Operand"])
    elif type == "UnaryLogicalOperator":
        return UnaryLogicalOperator(node["$id"], node["Operation"], node["Operand"])
    elif type == "UnaryVariableOperator":
        return UnaryVariableOperator(node["$id"], node["Operation"], node["Operand"])
    else:
        return UnknownNode(node["$id"])


def tryResolveVariableDeclarationStatement(node):
    if "VariableDeclaration" in node:
        variableDeclaration = node["VariableDeclaration"]
        if variableDeclaration is None:
            return None
        if "$id" in variableDeclaration:
            numOfRef = variableDeclaration["$id"]
            if numOfRef in variableDeclarations:
                return variableDeclarations[numOfRef]
            else:
                return None
        else:
            return None
    else:
        return None


def resolveVarDecl(node):
    variableDeclaration = tryResolveVariableDeclarationStatement(node)
    if variableDeclaration is None:
        variableDeclaration = variableNameDecl[node["VariableName"]]
    else:
        variableNameDecl[node["VariableName"]] = variableDeclaration
    return variableDeclaration