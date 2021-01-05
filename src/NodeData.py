class NodeData:
    """This class represents a node data of the graph with simple functions."""

    def __init__(self, key, pos=None):
        self.key = key
        self.pos = pos
        self.parent = 0
        self.tag = 0

    def __repr__(self) -> str:
        return f"|Key: {self.key}|"

    def __lt__(self, other):
        return self.tag < other.tag
