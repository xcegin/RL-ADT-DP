from ADT.ADTNode import ADTNode
from ADT.ResolverUtil import resolveType, resolveNodeViaType


class SequenceNode(ADTNode):
    CDTNameAsBlock = "c.CASTCompoundStatement"
    CDTNameAsExpression = "c.CASTExpressionList"

    def __init__(self, nodes):
        self.nodes = []
        for node in nodes["$values"]:
            self.nodes.append(resolveNodeViaType(node["$type"], node))
