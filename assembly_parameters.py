import datetime
import random


statement_terminals  = [
    # plain no-operand instructions
    "nop", "stosw", "lodsw", "movsw", "cmpsw", "scasw", "pushf", "popf",
    "lahf", "stosb", "lodsb", "movsb", "cmpsb", "scasb", "xlat", "xlatb",
    "cwd", "cbw", "cmc", "clc", "stc", "cli", "sti", "cld", "std",
    # rep/repe/repne prefixed string instructions
    "rep stosb", "rep stosw", "rep movsb", "rep movsw",
    "rep lodsw", "rep lodsb",
    "rep scasw", "rep scasb",
    "repe cmpsw", "repe cmpsb",
    "repne cmpsw", "repne cmpsb",
    "repe scasw", "repe scasb",
    "repne scasw", "repne scasb",
]
opcodes_special = ["wait\nwait\nwait\nwait", "wait\nwait", "int 0x86", "int 0x87"]  # "nrg"=wait wait
opcodes_repeats = ["rep", "repe", "repz", "repne", "repnz"]
opcodes_jump = ["jmp", "jcxz", "je", "jne", "jp", "jnp", "jo", "jno", "jc", "jnc", "ja", "jna", "js", "jns", "jl",
                "jnl", "jle", "jnle", "loopnz", "loopne", "loopz", "loope", "loop"]
opcodes_double = ["cmp", "mov", "add", "sub", "and", "or", "xor", "adc", "sbb", "test"]
opcodes_single = ["div", "mul", "inc", "dec", "not", "neg"]
opcodes_function = ["call", "call near", "call far"]
opcodes_pointers = ["lea", "les", "lds"]
opcode_ret = ["ret", "retn", "retf", "iret"]
opcode_push = ["push"]
opcode_pop = ["pop"]
opcodes_double_no_cost = ["xchg"]
opcodes_shift = ["sal", "sar", "shl", "shr", "rol", "ror", "rcl", "rcr"]

# not supported: jecxz, imul, idiv, push const, repnz and repnz with s/l/m
general_registers = ["ax", "bx", "cx", "dx", "si", "di", "bp", "sp"]
general_half_registers = ["ah", "al", "bh", "bl", "ch", "cl", "dh", "dl"]
addressing_registers = ["[bx]", "[si]", "[di]", "[bp]",
                        "[bx+si]", "[bx+di]", "[bp+si]", "[bp+di]"]
pop_registers = general_registers + ["WORD " + add_reg for add_reg in addressing_registers] + ["ds", "es"]  #+, "ss"]
push_registers = pop_registers + ["cs", "ss"]
labels = []
consts = (
    [str(2*i) for i in range(0, 133)] +
    [str(-2*i) for i in range(1, 11)] +   # -2, -4, ..., -20 for backward bombing
    ["65535", "0xCCCC"]
)




from evo_types import *

TAG_TO_TYPE = {
    "reg": t_reg,
    "half_reg": t_half_reg,
    "mem": t_mem,
    "imm": t_imm,
    "statement": t_stmt,
    "section": t_section,
    "jmp": t_jmp,
}


def create_terminals(terminal_tuples):
    ret = {value : TAG_TO_TYPE[tag] for value, tag in terminal_tuples if tag in TAG_TO_TYPE}
    return ret


terminal_set = create_terminals(
    [(reg, "reg") for reg in general_registers] +
    [(h_reg, "half_reg") for h_reg in general_half_registers] +
    [(addr, "mem") for addr in addressing_registers] +
    [(c, "imm") for c in consts] +
    [(s, "statement") for s in statement_terminals] +
    [(j, "jmp") for j in opcodes_jump]
)



