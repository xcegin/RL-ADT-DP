from ADT.ADTNode import ADTNode


class SequenceNode(ADTNode):
    CDTNameAsBlock = "c.CASTCompoundStatement"
    CDTNameAsExpression = "c.CASTExpressionList"

    def __init__(self, nodes):
        self.nodes = []
        for node in nodes["$values"]:
            from ADT.ResolverUtil import resolveNodeViaType
            self.nodes.append(resolveNodeViaType(node["$type"], node))
