from ADT.ADTNode import ADTNode


class SequenceNode(ADTNode):

    def accept(self, visitor):
        return visitor.visit_sequence(self)

    CDTNameAsBlock = "c.CASTCompoundStatement"
    CDTNameAsExpression = "c.CASTExpressionList"

    def __init__(self, id, nodes):
        super().__init__(id)
        self.nodes = []
        if "Nodes" in nodes:
            from ADT.Utils.ResolverUtil import resolveNodeViaType
            self.nodes.append(resolveNodeViaType(nodes["Nodes"]["$type"], nodes["Nodes"]))
        if "$values" in nodes:
            for node in nodes["$values"]:
                from ADT.Utils.ResolverUtil import resolveNodeViaType
                self.nodes.append(resolveNodeViaType(node["$type"], node))
