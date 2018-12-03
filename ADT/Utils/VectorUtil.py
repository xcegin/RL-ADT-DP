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
    if isinstance(node, DoLoop) or node is isinstance(node, WhileLoop):
        return 21
    elif isinstance(node, BinaryArithmeticOperator):
        return 1
    elif isinstance(node, BinaryBitwiseOperator):
        return 2
    elif isinstance(node, BinaryLogicalOperator):
        return 3
    elif isinstance(node, UnaryArithmeticOperator):
        return 4
    elif isinstance(node, ComparisonOperator):
        return 5
    elif isinstance(node, UnaryBitwiseOperator):
        return 6
    elif isinstance(node, UnaryLogicalOperator):
        return 7
    elif isinstance(node, UnaryVariableOperator):
        return 8
    elif isinstance(node, AssignmentStatement):
        return 9
    elif isinstance(node, BreakStatement):
        return 10
    elif isinstance(node, FunctionCall):
        return 11
    elif isinstance(node, FunctionDeclarationStatement):
        return 12
    elif isinstance(node, ReturnStatement):
        return 13
    elif isinstance(node, VariableDeclarationStatement):
        return 14
    elif isinstance(node, ArraySubscriptVariable):
        return 15
    elif isinstance(node, FieldReferenceVariable):
        return 16
    elif isinstance(node, SimpleVariable):
        return 17
    elif isinstance(node, OperatorVariable):
        return 18
    elif isinstance(node, IfNode):
        return 19
    elif isinstance(node, LiteralNode):
        return 20
    else:
        return 0


def typeOfVectorData(node):
    from ADT.Variables.VariableNode import VariableNode
    from ADT.LiteralNode import LiteralNode
    from ADT.Statements.FunctionCall import FunctionCall
    from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
    from ADT.Operators.BinaryArithmeticOperator import BinaryArithmeticOperator
    from ADT.Operators.BinaryBitwiseOperator import BinaryBitwiseOperator
    from ADT.Operators.BinaryLogicalOperator import BinaryLogicalOperator
    from ADT.Operators.UnaryArithmeticOperator import UnaryArithmeticOperator
    from ADT.Operators.ComparisonOperator import ComparisonOperator
    from ADT.Operators.UnaryBitwiseOpeartor import UnaryBitwiseOperator
    from ADT.Operators.UnaryLogicalOperator import UnaryLogicalOperator
    from ADT.Operators.UnaryVariableOperator import UnaryVariableOperator
    if isinstance(node, VariableNode):
        return 6
    elif isinstance(node, LiteralNode):
        return 1
    elif isinstance(node, BinaryArithmeticOperator):
        return 8
    elif isinstance(node, BinaryBitwiseOperator):
        return 2
    elif isinstance(node, BinaryLogicalOperator):
        return 9
    elif isinstance(node, FunctionCall):
        return 4
    elif isinstance(node, VariableDeclarationStatement):
        return 5
    elif node is None:
        return 0
    elif isinstance(node, UnaryArithmeticOperator):
        return 3
    elif isinstance(node, ComparisonOperator):
        return 10
    elif isinstance(node, UnaryBitwiseOperator):
        return 11
    elif isinstance(node, UnaryLogicalOperator):
        return 12
    elif isinstance(node, UnaryVariableOperator):
        return 13
    else:
        return 7


def vectorizationTypeUtil(type):
    if type == "t_int":
        return 1
    elif type == "t_char16_t":
        return 2
    elif type == "t_char":
        return 2
    elif type == "t_char32_t":
        return 2
    elif type == "t_bool":
        return 3
    elif type == "t_wchar_t":
        return 2
    elif type == "t_int128":
        return 1
    elif type == "t_float128" or type == "t_double":
        return 4
    elif type == "t_float":
        return 4
    elif type == "t_decimal128":
        return 4
    elif type == "t_decimal32":
        return 4
    elif type == "t_decimal64":
        return 4
    else:
        return 5


def vectorizationTypeLiteral(type):
    if type == "lk_nullptr":
        return 6
    elif type == "lk_char_constant":
        return 1
    elif type == "lk_string_literal":
        return 2
    elif type == "lk_false" or type == "lk_true":
        return 3
    elif type == "lk_this":
        return 4
    elif type == "lk_float_constant":
        return 5
    else:
        return 0


def resolve_argument_involvement(argument, visitor):
    highest = 0
    for currArg in visitor.currentArgumentVectorDependency:
        if currArg is None:
            continue
        elif argument == currArg:
            highest = 2 if highest < 2 else highest
        elif IsInfluencedByCurrentArgVector(argument, visitor, currArg):
            highest = 1 if highest < 1 else highest
    return highest


def IsInfluencedByCurrentArgVector(argument, visitor, currArg):
    dataDependencyDict = visitor.context.dataDependencies
    if currArg in dataDependencyDict[argument]:
        return True
    for arg in dataDependencyDict[currArg]:
        if arg in dataDependencyDict[argument]:
            return True
    return False
