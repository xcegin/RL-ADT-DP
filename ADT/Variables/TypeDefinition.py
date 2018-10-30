from ADT.ADTNode import ADTNode


class TypeDefinition(ADTNode):

    def accept(self, visitor):
        pass

    def __init__(self, typeName, pointerDimension, arrayDimension, arrayDimensionSize, modifiers, typeNode):
        self.typeName = typeName
        self.pointerDimension = pointerDimension
        self.arrayDimension = arrayDimension
        self.arrayDimensionSize = arrayDimensionSize
        self.modifiers = modifiers
        self.typeNode = typeNode
