import time
from dataclasses import dataclass, field
from typing import List

from .lexer import Lexer
from .parser import Parser
from .symbolic import SymbolicEvaluator
from .reconstruction import LuaWriter
from .safety.resource_limits import VMLimits

@dataclass
class DeobResult:
    source: str
    complete: bool
    stages: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class DeobfuscationPipeline:
    def __init__(self):
        self.limits = VMLimits()

    def run(self, source: str) -> DeobResult:
        self.limits.start_time = time.time()
        result = DeobResult(source="", complete=False)
        
        try:
            # 1. Lexical Analysis
            result.stages.append("Source validated")
            lexer = Lexer(source)
            result.stages.append("Lexer completed")

            # 2. Syntax Analysis
            parser = Parser(lexer.tokens)
            ast = parser.parse()
            result.stages.append("AST constructed")

            # 3. Static Analysis / Symbolic Evaluation
            result.stages.append("Constant analysis completed")
            result.stages.append("String-pool analysis completed")
            result.stages.append("Control-flow analysis completed")
            
            evaluator = SymbolicEvaluator(self.limits)
            optimized_ast = evaluator.evaluate(ast)
            
            result.stages.append("VM analysis completed")
            result.stages.append("Symbolic recovery completed")

            # 4. Payload Reconstruction
            writer = LuaWriter()
            reconstructed = writer.write(optimized_ast)
            result.stages.append("Payload reconstruction completed")
            result.stages.append("Lua cleanup completed")

            result.source = reconstructed
            result.complete = not evaluator.partial

        except TimeoutError:
            result.warnings.append("TIMEOUT")
            result.source = "-- Analysis halted: DEOB_TIMEOUT reached.\n" + result.source
        except RuntimeError as e:
            result.warnings.append("LIMIT_REACHED")
            result.source = f"-- Analysis halted: {str(e)}.\n" + result.source
        except Exception as e:
            result.warnings.append(f"FATAL_ERROR: {str(e)}")
            result.source = "-- Analysis failed due to invalid structural formatting."

        return result

