class NodeTree(object):
    def __init__(self):
        self.children = []
        self.tokenType = None
        self.tokenValue = None
        self.parent = None
        self.isTerminal = False


def createNode(_tokenType, _tokenValue, _isTerminal):
    node = NodeTree()
    node.tokenValue = _tokenValue
    node.tokenType = _tokenType
    node.isTerminal = _isTerminal
    return node


def addNode(_parentNode, _node):
    _node.parent = _parentNode
    _parentNode.childen.append(_node)
