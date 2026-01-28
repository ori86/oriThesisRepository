from new_types import *


# --- helper decorator: attaches typed-GP metadata for Eckity ---
def primitive(ret_type, *arg_types):
    def deco(fn):
        # Provide both attribute names to be safe across Eckity versions
        fn.ret_type = ret_type
        fn.arg_types = list(arg_types)
        fn.return_type = ret_type
        fn.argument_types = list(arg_types)
        return fn
    return deco

# --- helper for constructing typed string tokens uniformly ---
def _mk(ret_type, text):
    return ret_type(text)

# ====== Example primitives (you can add more as needed) ======

@primitive(t_section)
def section():
    # zero-arg node that "starts" a section
    return _mk(t_section, "SECTION")

@primitive(t_put_label, t_func_addres)
def put_label(addr):
    # place a label at address
    return _mk(t_put_label, f"LABEL {addr}")

@primitive(t_func_jmp, t_func_addres)
def func_jmp(addr):
    return _mk(t_func_jmp, f"JMP {addr}")

@primitive(t_func_dw, t_func_addres)
def func_dw(addr):
    return _mk(t_func_dw, f"DW {addr}")

@primitive(t_func_opcode_two_operands, t_func_opcode_operand_WORD, t_func_opcode_operand_WORD)
def func_opcode_two_operands_word(a, b):
    # e.g., "OPW a, b"
    return _mk(t_func_opcode_two_operands, f"OPW {a}, {b}")

@primitive(t_func_opcode_two_operands, t_func_opcode_operand_BYTE, t_func_opcode_operand_BYTE)
def func_opcode_two_operands_byte(a, b):
    # e.g., "OPB a, b"
    return _mk(t_func_opcode_two_operands, f"OPB {a}, {b}")

@primitive(t_func_opcode_openrand)
def func_opcode_openrand():
    # placeholder
    return _mk(t_func_opcode_openrand, "OPENRAND")

@primitive(t_func_call, t_func_addres)
def func_call(addr):
    return _mk(t_func_call, f"CALL {addr}")

@primitive(t_random_generator_lcg, )
def random_generator_lcg():
    # you can wire a seed from context if needed
    return _mk(t_random_generator_lcg, "RND_LCG")

@primitive(t_random_generator_xor_shift, )
def random_generator_xor_shift():
    return _mk(t_random_generator_xor_shift, "RND_XOR")

# ====== Terminals (zero-arg, typed) ======

@primitive(t_func_addres)
def T_ADDR_0():
    return _mk(t_func_addres, "0x0000")

@primitive(t_func_addres)
def T_ADDR_1():
    return _mk(t_func_addres, "0x0010")

@primitive(t_func_opcode_operand_WORD)
def T_WORD_1():
    return _mk(t_func_opcode_operand_WORD, "1")

@primitive(t_func_opcode_operand_WORD)
def T_WORD_2():
    return _mk(t_func_opcode_operand_WORD, "2")

@primitive(t_func_opcode_operand_BYTE)
def T_BYTE_1():
    return _mk(t_func_opcode_operand_BYTE, "1")

@primitive(t_func_opcode_operand_BYTE)
def T_BYTE_2():
    return _mk(t_func_opcode_operand_BYTE, "2")

# ====== Export the sets Eckity expects ======
FUNCTION_SET = [
    section,
    put_label,
    func_jmp,
    func_dw,
    func_opcode_two_operands_word,
    func_opcode_two_operands_byte,
    func_opcode_openrand,
    func_call,
    random_generator_lcg,
    random_generator_xor_shift,
]


