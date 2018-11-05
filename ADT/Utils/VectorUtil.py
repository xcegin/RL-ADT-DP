

#TODO think more of the grouping values
def typeOfVector(node):
    from ADT.Operators.BinaryArithmeticOperator import BinaryArithmeticOperator
    from ADT.Loops.DoLoop import DoLoop
    from ADT.Loops.WhileLoop import WhileLoop
    from ADT.Operators.BinaryBitwiseOperator import BinaryBitwiseOperator
    from ADT.Operators.BinaryLogicalOperator import BinaryLogicalOperator
    from ADT.Operators.UnaryArithmeticOperator import UnaryArithmeticOperator
    from ADT.Operators.ComparisonOperator import ComparisonOperator
    from ADT.Operators.UnaryBitwiseOpeartor import UnaryBitwiseOperator
    from ADT.Operators.UnaryLogicalOperator import UnaryLogicalOperator
    from ADT.Operators.UnaryVariableOperator import UnaryVariableOperator
    from ADT.Statements.AssigmentStatement import AssignmentStatement
    from ADT.Statements.BreakStatement import BreakStatement
    from ADT.Statements.FunctionCall import FunctionCall
    from ADT.Statements.FunctionDeclarationStatement import FunctionDeclarationStatement
    from ADT.Statements.ReturnStatement import ReturnStatement
    from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
    from ADT.Variables.ArraySubscriptVariable import ArraySubscriptVariable
    from ADT.Variables.FieldReferenceVariable import FieldReferenceVariable
    from ADT.Variables.SimpleVariable import SimpleVariable
    from ADT.Variables.OperatorVariable import OperatorVariable
    from ADT.IfNode import IfNode
    from ADT.LiteralNode import LiteralNode
    if node is DoLoop or node is WhileLoop:
        return 0
    elif node is BinaryArithmeticOperator:
        return 1
    elif node is BinaryBitwiseOperator:
        return 2
    elif node is BinaryLogicalOperator:
        return 3
    elif node is UnaryArithmeticOperator:
        return 4
    elif node is ComparisonOperator:
        return 5
    elif node is UnaryBitwiseOperator:
        return 6
    elif node is UnaryLogicalOperator:
        return 7
    elif node is UnaryVariableOperator:
        return 8
    elif node is AssignmentStatement:
        return 9
    elif node is BreakStatement:
        return 10
    elif node is FunctionCall:
        return 11
    elif node is FunctionDeclarationStatement:
        return 12
    elif node is ReturnStatement:
        return 13
    elif node is VariableDeclarationStatement:
        return 14
    elif node is ArraySubscriptVariable:
        return 15
    elif node is FieldReferenceVariable:
        return 16
    elif node is SimpleVariable:
        return 17
    elif node is OperatorVariable:
        return 18
    elif node is IfNode:
        return 19
    elif node is LiteralNode:
        return 20
    else:
        return 21

def typeOfVectorData(node):
    from ADT.Variables.VariableNode import VariableNode
    from ADT.LiteralNode import LiteralNode
    from ADT.Operators.BinaryOperator import BinaryOperator
    from ADT.Operators.UnaryOperator import UnaryOperator
    from ADT.Statements.FunctionCall import FunctionCall
    if node is VariableNode:
        return 0
    elif node is LiteralNode:
        return 1
    elif node is BinaryOperator:
        return 2
    elif node is UnaryOperator:
        return 3
    elif node is FunctionCall:
        return 4
    else:
        return 5


def vectorizationTypeUtil(type):
    if type == "t_int":
        return 0
    elif type == "t_char16_t":
        return 20
    elif type == "t_char":
        return 21
    elif type == "t_char32_t":
        return 22
    elif type == "t_bool":
        return 50
    elif type == "t_wchar_t":
        return 23
    elif type == "t_int128":
        return 1
    elif type == "t_float128" or type == "t_double":
        return 100
    elif type == "t_float":
        return 101
    elif type == "t_decimal128":
        return 102
    elif type == "t_decimal32":
        return 103
    elif type == "t_decimal64":
        return 104
    else:
        return 105

def resolve_argument_involvement(argument, visitor):
    if visitor.currentArgumentVectorDependency == None:
        return 0
    if argument == visitor.currentArgumentVectorDependency:
        return 2
    elif IsInfluencedByCurrentArgVector(argument, visitor):
        return 1
    else:
        return 0

def IsInfluencedByCurrentArgVector(argument, visitor):
    dataDependencyDict = visitor.context.dataDependencies
    if argument in dataDependencyDict:
        return True
    for arg in dataDependencyDict[visitor.currentArgumentVectorDependency]:
        if visitor.currentArgumentVectorDependency in visitor.currentArgumentVectorDependency[arg]:
            return True
    return False
