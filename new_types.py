

class t_section(str): pass

class t_func_opcode_two_operands(str): pass
class t_func_opcode_two_operands_WORD(str): pass
class t_func_opcode_two_operands_BYTE(str): pass

class t_func_opcode_openrand(str): pass

class t_func_opcode_operand_WORD(str): pass
class t_func_opcode_operand_BYTE(str): pass
class t_func_opcode_operand_cl(str): pass
class t_func_opcode_operand_1(str): pass

class t_func_call(str): pass
class t_func_opcode(str): pass
class t_put_label(str): pass
class t_func_forward_jmp(str): pass
class t_func_backwords_jmp(str): pass
class t_func_jmp(str): pass
class t_func_dw(str): pass
class t_func_addres(str): pass

class t_random_generator_lcg(str): pass
class t_random_generator_xor_shift(str): pass


type_tokens  = {
    "section": t_section,
    "func_opcode_two_operands": t_func_opcode_two_operands,
    "func_opcode_two_operands_WORD": t_func_opcode_two_operands_WORD,
    "func_opcode_two_operands_BYTE": t_func_opcode_two_operands_BYTE,
    "func_opcode_openrand": t_func_opcode_openrand,
    "func_opcode_operand_WORD": t_func_opcode_operand_WORD,
    "func_opcode_operand_BYTE": t_func_opcode_operand_BYTE,
    "func_call": t_func_call,
    "func_opcode": t_func_opcode,
    "put_label": t_put_label,
    "func_forward_jmp": t_func_forward_jmp,
    "func_backwords_jmp": t_func_backwords_jmp,
    "func_jmp": t_func_jmp,
    "func_dw": t_func_dw,
    "func_addres": t_func_addres,
    "func_opcode_operand_cl": t_func_opcode_operand_cl,
    "func_opcode_operand_1": t_func_opcode_operand_1,
    "random_generator_lcg": t_random_generator_lcg,
    "random_generator_xor_shift": t_random_generator_xor_shift,
}
