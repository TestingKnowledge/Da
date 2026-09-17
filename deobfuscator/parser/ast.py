class Node: pass

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

class Assignment(Node):
    def __init__(self, is_local, targets, values):
        self.is_local = is_local
        self.targets = targets
        self.values = values

class Literal(Node):
    def __init__(self, value, type_):
        self.value = value
        self.type = type_ # 'NUMBER', 'STRING', 'BOOLEAN'

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class FunctionCall(Node):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class UnknownNode(Node):
    def __init__(self, raw_tokens):
        self.raw = raw_tokens

