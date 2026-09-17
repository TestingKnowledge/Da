import re

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

class Lexer:
    # A restricted lexer focusing on standard/obfuscated Lua constants, identifiers, and ops
    RULES = [
        ('COMMENT', r'--\[\[.*?\]\]|--.*'),
        ('STRING', r'(["\'])(?:(?=(\\?))\2.)*?\1'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('KEYWORD', r'\b(local|if|then|else|end|while|do|for|function|return|and|or|not|true|false)\b'),
        ('IDENT', r'\b[a-zA-Z_]\w*\b'),
        ('OP', r'==|~=|\.\.|<=|>=|<|>|\+|-|\*|/|%|\^|=|#'),
        ('PUNC', r'[\[\]\{\}\(\)\.,;]'),
        ('SPACE', r'\s+'),
        ('MISMATCH', r'.')
    ]
    
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        rules = [(name, re.compile(pattern, re.DOTALL)) for name, pattern in self.RULES]
        pos = 0
        line = 1
        while pos < len(self.source):
            match = None
            for name, regex in rules:
                match = regex.match(self.source, pos)
                if match:
                    val = match.group(0)
                    
                    # FIXED: Safely ignore spaces, comments, and mismatched characters
                    if name not in ['SPACE', 'COMMENT', 'MISMATCH']:
                        self.tokens.append(Token(name, val, line))
                        
                    line += val.count('\n')
                    pos = match.end(0) # Now it properly moves forward!
                    break
            if not match:
                pos += 1 # Fallback safeguard
