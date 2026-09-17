from ..parser.ast import *

class LuaWriter:
    def __init__(self):
        self.output = []

    def write(self, node):
        if isinstance(node, Block):
            for stmt in node.statements:
                self.output.append(self.visit(stmt))
            return "\n".join(filter(None, self.output))
        return self.visit(node)

    def visit(self, node):
        if isinstance(node, Assignment):
            prefix = "local " if node.is_local else ""
            targets = ", ".join(t.name for t in node.targets)
            if node.values:
                vals = ", ".join(self.visit(v) for v in node.values)
                return f"{prefix}{targets} = {vals}"
            return f"{prefix}{targets}"
            
        elif isinstance(node, Literal):
            return str(node.value)
            
        elif isinstance(node, Identifier):
            return node.name
            
        elif isinstance(node, BinaryOp):
            return f"{self.visit(node.left)} {node.op} {self.visit(node.right)}"
            
        elif isinstance(node, FunctionCall):
            func_name = self.visit(node.func)
            args = ", ".join(self.visit(a) for a in node.args)
            return f"{func_name}({args})"
            
        return "-- [UNRESOLVED NODE]"
