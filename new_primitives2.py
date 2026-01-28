# from new_types import *


# def section() -> t_section:
#     """zero-arg node that 'starts' a section"""
#     return t_section("SECTION")


# def put_label(addr: t_func_addres) -> t_put_label:
#     """place a label at address"""
#     return t_put_label(f"LABEL {addr}")


# def func_jmp(addr: t_func_addres) -> t_func_jmp:
#     """jump to address"""
#     return t_func_jmp(f"JMP {addr}")


# def func_dw(addr: t_func_addres) -> t_func_dw:
#     """define word at address"""
#     return t_func_dw(f"DW {addr}")


# def func_opcode_two_operands_word(
#     a: t_func_opcode_operand_WORD, b: t_func_opcode_operand_WORD
# ) -> t_func_opcode_two_operands:
#     """word-sized opcode with two operands"""
#     return t_func_opcode_two_operands(f"OPW {a}, {b}")


# def func_opcode_two_operands_byte(
#     a: t_func_opcode_operand_BYTE, b: t_func_opcode_operand_BYTE
# ) -> t_func_opcode_two_operands:
#     """byte-sized opcode with two operands"""
#     return t_func_opcode_two_operands(f"OPB {a}, {b}")


# def func_opcode_openrand() -> t_func_opcode_openrand:
#     """placeholder OPENRAND opcode"""
#     return t_func_opcode_openrand("OPENRAND")


# def func_call(addr: t_func_addres) -> t_func_call:
#     """call function at address"""
#     return t_func_call(f"CALL {addr}")


# def random_generator_lcg() -> t_random_generator_lcg:
#     """linear congruential generator token"""
#     return t_random_generator_lcg("RND_LCG")


# def random_generator_xor_shift() -> t_random_generator_xor_shift:
#     """xor-shift generator token"""
#     return t_random_generator_xor_shift("RND_XOR")


# # ---- Terminals ----

# def T_ADDR_0() -> t_func_addres:
#     """address literal 0x0000"""
#     return t_func_addres("0x0000")


# def T_ADDR_1() -> t_func_addres:
#     """address literal 0x0010"""
#     return t_func_addres("0x0010")


# def T_WORD_1() -> t_func_opcode_operand_WORD:
#     """word literal 1"""
#     return t_func_opcode_operand_WORD("1")


# def T_WORD_2() -> t_func_opcode_operand_WORD:
#     """word literal 2"""
#     return t_func_opcode_operand_WORD("2")


# def T_BYTE_1() -> t_func_opcode_operand_BYTE:
#     """byte literal 1"""
#     return t_func_opcode_operand_BYTE("1")


# def T_BYTE_2() -> t_func_opcode_operand_BYTE:
#     """byte literal 2"""
#     return t_func_opcode_operand_BYTE("2")


# # ====== Export the sets Eckity expects ======
# FUNCTION_SET2 = [
#     section,
#     put_label,
#     func_jmp,
#     func_dw,
#     func_opcode_two_operands_word,
#     func_opcode_two_operands_byte,
#     func_opcode_openrand,
#     func_call,
#     random_generator_lcg,
#     random_generator_xor_shift,
#     # T_ADDR_0,
#     # T_ADDR_1,
#     # T_WORD_1,
#     # T_WORD_2,   
#     # T_BYTE_1,
#     # T_BYTE_2,
# ]




# new 


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
