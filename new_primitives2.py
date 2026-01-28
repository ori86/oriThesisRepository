from new_types import *


# -------- Program composition --------

def seq(a: t_section, b: t_section) -> t_section:
    """Concatenate two code blocks (multi-line strings)."""
    a = str(a).strip()
    b = str(b).strip()
    if not a:
        return t_section(b)
    if not b:
        return t_section(a)
    return t_section(a + "\n" + b)


# -------- Safe basic instructions --------

def nop() -> t_section:
    return t_section("nop")


def stosb() -> t_section:
    # writes AL to [ES:DI], increments DI
    return t_section("stosb")


def stosw() -> t_section:
    # writes AX to [ES:DI], increments DI by 2
    return t_section("stosw")


# -------- Two-operand instructions (WORD-ish) --------

def mov(dst: t_func_opcode_operand_WORD, src: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"mov {dst}, {src}")


def add(dst: t_func_opcode_operand_WORD, src: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"add {dst}, {src}")


def sub(dst: t_func_opcode_operand_WORD, src: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"sub {dst}, {src}")


def xor(dst: t_func_opcode_operand_WORD, src: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"xor {dst}, {src}")


def cmp(dst: t_func_opcode_operand_WORD, src: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"cmp {dst}, {src}")


# -------- One-operand instructions --------

def inc(dst: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"inc {dst}")


def dec(dst: t_func_opcode_operand_WORD) -> t_section:
    return t_section(f"dec {dst}")

def movb(dst: t_func_opcode_operand_BYTE, src: t_func_opcode_operand_BYTE) -> t_section:
    return t_section(f"mov {dst}, {src}")

def idw(x: t_func_opcode_operand_WORD) -> t_func_opcode_operand_WORD:
    return x


# Export to Eckity
FUNCTION_SET2 = [
    seq,
    nop,
    stosb,
    stosw,
    mov,
    add,
    sub,
    xor,
    cmp,
    inc,
    dec,
    idw,
    #movb,
]
