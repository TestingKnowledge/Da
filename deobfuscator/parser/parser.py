from .ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None, expected_value=None):
        tok = self.peek()
        if tok and (expected_type is None or tok.type == expected_type) and (expected_value is None or tok.value == expected_value):
            self.pos += 1
            return tok
        return None

    def parse(self):
        stmts = []
        while self.peek():
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
            else:
                self.pos += 1 # Skip unparseable to allow partial recovery
        return Block(stmts)

    def parse_statement(self):
        if self.consume('KEYWORD', 'local'):
            return self.parse_assignment(is_local=True)
        # Attempt standard assignment
        saved = self.pos
        ident = self.consume('IDENT')
        if ident and self.consume('OP', '='):
            self.pos = saved # backtrack
            return self.parse_assignment(is_local=False)
        self.pos = saved
        
        # Fallback to expression/function call
        expr = self.parse_expression()
        if isinstance(expr, FunctionCall):
            return expr
        return None

    def parse_assignment(self, is_local):
        targets = []
        while True:
            t = self.consume('IDENT')
            if not t: break
            targets.append(Identifier(t.value))
            if not self.consume('PUNC', ','): break
            
        values = []
        if self.consume('OP', '='):
            while True:
                val = self.parse_expression()
                if not val: break
                values.append(val)
                if not self.consume('PUNC', ','): break
                
        return Assignment(is_local, targets, values)

    def parse_expression(self):
        left = self.parse_primary()
        if not left: return None
        
        while True:
            op = self.consume('OP')
            if op:
                right = self.parse_primary()
                if right:
                    left = BinaryOp(left, op.value, right)
                else:
                    break
            else:
                break
        return left

    def parse_primary(self):
        tok = self.peek()
        if not tok: return None
        
        if tok.type == 'NUMBER':
            self.pos += 1
            return Literal(float(tok.value) if '.' in tok.value else int(tok.value), 'NUMBER')
        elif tok.type == 'STRING':
            self.pos += 1
            return Literal(tok.value, 'STRING') # keeping quotes for simplicity
        elif tok.type == 'IDENT':
            self.pos += 1
            ident = Identifier(tok.value)
            if self.consume('PUNC', '('):
                args = []
                while not self.consume('PUNC', ')'):
                    arg = self.parse_expression()
                    if arg: args.append(arg)
                    self.consume('PUNC', ',')
                return FunctionCall(ident, args)
            return ident
        return None

