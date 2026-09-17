import os

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
MAX_UPLOAD_BYTES = int(os.environ.get("MAX_UPLOAD_BYTES", 2 * 1024 * 1024)) # 2 MB
MAX_VM_STEPS = int(os.environ.get("MAX_VM_STEPS", 100000))
MAX_VM_STATES = int(os.environ.get("MAX_VM_STATES", 10000))
MAX_VM_STACK_DEPTH = int(os.environ.get("MAX_VM_STACK_DEPTH", 512))
MAX_VM_REGISTERS = int(os.environ.get("MAX_VM_REGISTERS", 256))
MAX_VM_MEMORY_ENTRIES = int(os.environ.get("MAX_VM_MEMORY_ENTRIES", 50000))
DEOB_TIMEOUT = int(os.environ.get("DEOB_TIMEOUT", 30)) # Seconds
 
