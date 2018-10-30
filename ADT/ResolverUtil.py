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

def resolveType(type):
    startIndex = type.find('[')
    if startIndex > -1:
        endIndex = type.find(']')
        type = type[startIndex:endIndex]
        type = type.replace("[", "")
        type = type.replace("]", "")

    givenType = type.split(',')[0]
    return givenType.split('.')[-1]


def resolveNodeViaType(type, node):
    type = resolveType(type)
    if type == "VariableDeclarationStatement":
        variableDeclarationStatement = VariableDeclarationStatement(node["VariableType"],node["InitialValue"])
        variableDeclarations[node["$id"]] = variableDeclarationStatement
        variableDeclarationStatement.variable = resolveNodeViaType(node["Variable"]["$type"], node["Variable"])
        return variableDeclarations[node["$id"]]
    # ADT Nodes
    elif type == "IfNode":
        return IfNode(node["Condition"], node["NodeThen"], node["NodeElse"])
    elif type == "LiteralNode":
        return LiteralNode(node["Value"], node["Kind"])
    elif type == "SequenceNode" or type == "IAdtNode":
        return SequenceNode(node)
    # Statement Nodes
    elif type == "AssignmentStatement":
        return AssignmentStatement(node["Variable"], node["Value"])
    elif type == "BreakStatement":
        return BreakStatement()
    elif type == "FunctionCall":
        return FunctionCall(node["Name"], node["Arguments"])
    elif type == "FunctionDeclarationStatement":
        return FunctionDeclarationStatement(node["ReturnTypeModifiers"], node["ReturnType"], node["Name"],
                                            node["Arguments"])
    elif type == "ReturnStatement":
        return ReturnStatement(node["Value"])
    # Variable Nodes
    elif type == "ArraySubscriptVariable":
        variableDeclaration = tryResolveVariableDeclarationStatement(node)
        return ArraySubscriptVariable(node["VariableName"], node["Array"], node["Subscript"], variableDeclaration)
    elif type == "FieldReferenceVariable":
        variableDeclaration = tryResolveVariableDeclarationStatement(node)
        return FieldReferenceVariable(node["VariableName"], node["Variable"], node["Dereference"], node["Field"],
                                      variableDeclaration)
    elif type == "OperatorVariable":
        variableDeclaration = tryResolveVariableDeclarationStatement(node)
        return OperatorVariable(node["VariableName"], node["Operator"], variableDeclaration)
    elif type == "SimpleVariable":
        variableDeclaration = tryResolveVariableDeclarationStatement(node)
        return SimpleVariable(node["VariableName"], node["IsReference"], node["IsDefinition"], node["IsDeclaration"],
                              variableDeclaration)
    elif type == "TypeDefinition":
        return TypeDefinition(node["TypeName"], node["PointerDimension"], node["ArrayDimension"],
                              node["ArrayDimensionSize"],
                              node["Modifiers"], node["TypeNode"])
    # Loop Nodes
    elif type == "DoLoop":
        return DoLoop(node["Condition"], node["NodeBlock"])
    elif type == "ForLoop":
        return ForLoop(node["NodeInit"], node["Condition"], node["NodeAfter"], node["NodeBlock"])
    elif type == "WhileLoop":
        return WhileLoop(node["Condition"], node["NodeBlock"])
    # Operator nodes
    elif type == "BinaryArithmeticOperator":
        return BinaryArithmeticOperator(node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "BinaryArithmeticOperator":
        return BinaryBitwiseOperator(node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "BinaryLogicalOperator":
        return BinaryLogicalOperator(node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "ComparisonOperator":
        return ComparisonOperator(node["Operation"], node["LeftOperand"], node["RightOperand"])
    elif type == "UnaryArithmeticOperator":
        return UnaryArithmeticOperator(node["Operation"], node["Operand"])
    elif type == "UnaryBitwiseOperator":
        return UnaryArithmeticOperator(node["Operation"], node["Operand"])
    elif type == "UnaryLogicalOperator":
        return UnaryLogicalOperator(node["Operation"], node["Operand"])
    elif type == "UnaryVariableOperator":
        return UnaryVariableOperator(node["Operation"], node["Operand"])
    else:
        return UnknownNode()

def tryResolveVariableDeclarationStatement(node):
    if "VariableDeclaration" in node:
        variableDeclaration = node["VariableDeclaration"]
        if "$ref" in variableDeclaration:
            numOfRef = variableDeclaration["$ref"]
            if numOfRef in variableDeclarations:
                return variableDeclarations[numOfRef]
            else:
                return None
        else:
            return None
    else:
        return None