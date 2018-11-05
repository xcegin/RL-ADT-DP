COMPOSITE_EXPRESSION = "CompositeLogicExpression"

def getTypeOfExpression(type):
    givenType = type.split(',')[0]
    return givenType.split('.')[-1]