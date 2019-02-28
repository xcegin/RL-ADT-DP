NODE_LIST = [
    'DoLoop0','ForLoop0','WhileLoop0','DoLoop1','ForLoop1','WhileLoop1',
    'DoLoopNone','ForLoopNone','WhileLoopNone',
    'BinaryArithmeticOperator0','BinaryArithmeticOperator1','BinaryArithmeticOperator2',
    'BinaryArithmeticOperator3','BinaryArithmeticOperator4',
    'BinaryBitwiseOperator0', 'BinaryBitwiseOperator1', 'BinaryBitwiseOperator2', 'BinaryBitwiseOperator3',
    'BinaryBitwiseOperator4','BinaryLogicalOperator0','BinaryLogicalOperator1',
    'ComparisonOperator0','ComparisonOperator1','ComparisonOperator2','ComparisonOperator3','ComparisonOperator4','ComparisonOperator5',
    'UnaryArithmeticOperator0','UnaryArithmeticOperator1','UnaryArithmeticOperator2','UnaryArithmeticOperator3','UnaryArithmeticOperator4',
    'UnaryArithmeticOperator5','UnaryBitwiseOperator0','UnaryLogicalOperator0','UnaryVariableOperator0','UnaryVariableOperator1',
    'UnaryVariableOperator2','AssignmentStatement','BreakStatement','FunctionCall','FunctionCallRecursion','FunctionDeclarationStatement',
    'ReturnStatement','VariableDeclarationStatement','IfNode0','IfNode1','IfNodeNone','LiteralNode','SequenceNode','UnknownNode','ArraySubscriptVariable',
    'FieldReferenceVariable','SimpleVariable','TypeDefinition','VariableNode']

NODE_MAP = {x: i for (i, x) in enumerate(NODE_LIST)}