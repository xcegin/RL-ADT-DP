class Batcher:
    def __init__(self, batch):
        self.nodes, self.children = batch[0][1]
        self.nodes = self.nodes[0]
        self.children = self.children[0]
        self.done = False

    def give_next(self, num_of_next):
        tobereturned_nodes = self.nodes[:num_of_next]
        self.nodes = self.nodes[num_of_next:]
        tobereturned_children = self.children[:num_of_next]
        self.children = self.children[num_of_next:]
        if not self.nodes:
            self.done = True
        return [tobereturned_nodes], [tobereturned_children]

def gen_samples(tree, vectors, vector_lookup):
    """Creates a generator that returns a tree in BFS order with each node
    replaced by its vector embedding, and a child lookup table."""

    nodes = []
    children = []

    queue = [(tree, -1)]
    while queue:
        node, parent_ind = queue.pop(0)
        node_ind = len(nodes)
        # add children and the parent index to the queue
        queue.extend([(child, node_ind) for child in node['children']])
        # create a list to store this node's children indices
        children.append([])
        # add this child to its parent's child list
        if parent_ind > -1:
            children[parent_ind].append(node_ind)
        nodes.append(vectors[vector_lookup[node['node']]])

    yield (nodes, children)


def batch_samples(gen, batch_size):
    """Batch samples from a generator"""
    nodes, children = [], []
    samples = 0
    for n, c in gen:
        nodes.append(n)
        children.append(c)
        samples += 1
        if samples >= batch_size:
            yield _pad_batch(nodes, children)
            nodes, children = [], []
            samples = 0

    if nodes:
        yield _pad_batch(nodes, children)


def _pad_batch(nodes, children):
    if not nodes:
        return [], [], []
    max_nodes = max([len(x) for x in nodes])
    max_children = max([len(x) for x in children])
    feature_len = len(nodes[0][0])
    child_len = max([len(c) for n in children for c in n])

    nodes = [n + [[0] * feature_len] * (max_nodes - len(n)) for n in nodes]
    # pad batches so that every batch has the same number of nodes
    children = [n + ([[]] * (max_children - len(n))) for n in children]
    # pad every child sample so every node has the same number of children
    children = [[c + [0] * (child_len - len(c)) for c in sample] for sample in children]

    return nodes, children
