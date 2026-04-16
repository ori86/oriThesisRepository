from evo_types import *


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






def mov_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"mov {dst}, {src}")

def mov_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"mov {dst}, {imm}")

def mov_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"mov {dst}, {mem}")

def mov_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"mov {mem}, {src}")





def add_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"add {dst}, {src}")

def add_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"add {dst}, {imm}")



def sub_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"sub {dst}, {src}")

def sub_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sub {dst}, {imm}")

def sub_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"sub {dst}, {mem}")

def sub_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"sub word  {mem}, {src}")

def sub_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"sub word  {mem}, {imm}")




def xor_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"xor {dst}, {src}")

def xor_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"xor {dst}, {imm}")





def cmp_rr(a: t_reg, b: t_reg) -> t_stmt:
    return t_stmt(f"cmp {a}, {b}")

def cmp_ri(a: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"cmp {a}, {imm}")

def cmp_rm(a: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"cmp {a}, word {mem}")

def cmp_mr(mem: t_mem, reg: t_reg) -> t_stmt:
    return t_stmt(f"cmp word {mem}, {reg}")

def cmp_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"cmp word {mem}, {imm}")



def inc_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"inc {dst}")

def dec_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"dec {dst}")



def inc_m(dst: t_mem) -> t_stmt:
    return t_stmt(f"inc word {dst}")

def dec_m(dst: t_mem) -> t_stmt:
    return t_stmt(f"dec word {dst}")





def stosw() -> t_stmt:
    return t_stmt("stosw")

def stosb() -> t_stmt:
    return t_stmt("stosb")



def idr(x: t_reg) -> t_reg:
    return x
def idm(x: t_mem) -> t_mem:
    return x
def idi(x: t_imm) -> t_imm:
    return x
def ids(x:t_stmt) -> t_stmt:
    return x



def seq_stmt(a: t_stmt, b: t_stmt) -> t_stmt:
    a = str(a).strip()
    b = str(b).strip()
    if not a: return t_stmt(b)
    if not b: return t_stmt(a)
    return t_stmt(a + "\n" + b)

def prog2(a: t_stmt, b: t_stmt) -> t_stmt:
    return t_stmt("\n".join([str(a).strip(), str(b).strip()]))

def prog3(a: t_stmt, b: t_stmt, c: t_stmt) -> t_stmt:
    return t_stmt("\n".join([str(a).strip(), str(b).strip(), str(c).strip()]))

def prog4(a: t_stmt, b: t_stmt, c: t_stmt, d: t_stmt) -> t_stmt:
    return t_stmt("\n".join([str(a).strip(), str(b).strip(), str(c).strip(), str(d).strip()]))

def prog5(a: t_stmt, b: t_stmt, c: t_stmt, d: t_stmt , e:t_stmt) -> t_stmt:
    return t_stmt("\n".join([str(a).strip(), str(b).strip(), str(c).strip(), str(d).strip(), str(e).strip()]))




def push_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"push {dst}")


def pop_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"pop {dst}")







FUNCTION_SET2 = [


    stosb, stosw, 

    push_r, pop_r, 
    
    prog2, prog3, prog4, prog5,

    mov_rr,mov_ri,mov_rm,mov_mr,
    add_rr,add_ri,
    xor_rr,xor_ri,
    inc_r,dec_r,

    inc_m,dec_m,

    sub_rr, sub_ri, sub_rm, sub_mr, sub_mi,
    cmp_rr, cmp_ri, cmp_rm, cmp_mr, cmp_mi,

    idr,idm,idi,ids,


]

