import time
from ..parser.ast import *
from ..safety.resource_limits import VMLimits

class SymbolicEvaluator:
    def __init__(self, limits: VMLimits):
        self.env = {}
        self.limits = limits
        self.steps = 0
        self.partial = False

    def evaluate(self, node, depth=0):
        self.steps += 1
        self.limits.check_limits(self.steps, depth)

        if isinstance(node, Block):
            new_stmts = []
            for stmt in node.statements:
                eval_stmt = self.evaluate(stmt, depth + 1)
                if eval_stmt: new_stmts.append(eval_stmt)
            return Block(new_stmts)

        elif isinstance(node, Assignment):
            eval_vals = [self.evaluate(v, depth + 1) for v in node.values]
            # Track constants in environment for deterministic evaluation
            for i, target in enumerate(node.targets):
                if i < len(eval_vals) and isinstance(eval_vals[i], Literal):
                    self.env[target.name] = eval_vals[i]
                else:
                    self.env[target.name] = None # Mark as unknown/symbolic
            return Assignment(node.is_local, node.targets, eval_vals)

        elif isinstance(node, Identifier):
            # Resolve proven constants, otherwise return symbolic Identifier
            if node.name in self.env and self.env[node.name] is not None:
                return self.env[node.name]
            return node

        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left, depth + 1)
            right = self.evaluate(node.right, depth + 1)
            
            # Constant Folding & String Reconstitution
            if isinstance(left, Literal) and isinstance(right, Literal):
                try:
                    if node.op == '..':
                        val = f'"{left.value.strip("\"\'")} {right.value.strip("\"\'")}"'.replace(" ", "")
                        return Literal(val, 'STRING')
                    elif node.op == '+':
                        return Literal(left.value + right.value, 'NUMBER')
                    elif node.op == '-':
                        return Literal(left.value - right.value, 'NUMBER')
                    elif node.op == '*':
                        return Literal(left.value * right.value, 'NUMBER')
                except Exception:
                    self.partial = True
            
            return BinaryOp(left, node.op, right)

        elif isinstance(node, FunctionCall):
            self.partial = True # Symbolic fallback for external functions
            eval_args = [self.evaluate(arg, depth + 1) for arg in node.args]
            return FunctionCall(node.func, eval_args)

        elif isinstance(node, Literal):
            return node

        self.partial = True
        return node

