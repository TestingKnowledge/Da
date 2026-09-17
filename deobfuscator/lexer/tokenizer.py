import re
import time

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

class Lexer:
    RULES = [
        # FIXED: Safe, non-backtracking rules, plus support for Lua long strings [=[ ]=]
        ('COMMENT', r'--\[(=*)\[.*?\]\1\]|--[^\n]*'),
        ('LONGSTRING', r'\[(=*)\[.*?\]\1\]'),
        ('STRING', r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),
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
        self.start_time = time.time()
        self.tokenize()

    def tokenize(self):
        rules = [(name, re.compile(pattern, re.DOTALL)) for name, pattern in self.RULES]
        pos = 0
        line = 1
        while pos < len(self.source):
            # Hard failsafe: if lexing a massive obfuscated file takes > 10 seconds, abort safely
            if time.time() - self.start_time > 10:
                raise TimeoutError("Lexer timed out. The file is too large or complex.")

            match = None
            for name, regex in rules:
                match = regex.match(self.source, pos)
                if match:
                    val = match.group(0)
                    
                    # Treat LONGSTRING as a standard STRING for the parser
                    token_type = 'STRING' if name == 'LONGSTRING' else name

                    if token_type not in ['SPACE', 'COMMENT', 'MISMATCH']:
                        self.tokens.append(Token(token_type, val, line))
                        
                    line += val.count('\n')
                    pos = match.end(0)
                    break
            if not match:
                pos += 1 # Fallback safeguard
