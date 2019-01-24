from ADT.ADTNode import ADTNode


class TypeDefinition(ADTNode):

    def accept(self, visitor):
        return visitor.visit_typeDefinition(self)

    def __init__(self, id, typeName, pointerDimension, arrayDimension, arrayDimensionSize, modifiers, typeNode):
        super().__init__(id)
        self.typeName = typeName
        self.pointerDimension = pointerDimension
        self.arrayDimension = arrayDimension
        self.arrayDimensionSize = arrayDimensionSize
        self.modifiers = modifiers
        self.typeNode = typeNode
