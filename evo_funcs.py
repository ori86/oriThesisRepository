from evo_types import *



def _join_lines(*parts) -> str:
    lines = []
    for part in parts:
        s = str(part).strip()
        if s:
            lines.append(s)
    return "\n".join(lines)


# ---------------------------
# Program composition
# ---------------------------

def seq(a: t_section, b: t_section) -> t_section:
    return t_section(_join_lines(a, b))


def seq3(a: t_section, b: t_section, c: t_section) -> t_section:
    return t_section(_join_lines(a, b, c))


def seq4(a: t_section, b: t_section, c: t_section, d: t_section) -> t_section:
    return t_section(_join_lines(a, b, c, d))


def as_section(x: t_stmt) -> t_section:
    return t_section(str(x).strip())


def seq_stmt(a: t_stmt, b: t_stmt) -> t_stmt:
    return t_stmt(_join_lines(a, b))


def prog2(a: t_stmt, b: t_stmt) -> t_stmt:
    return t_stmt(_join_lines(a, b))


def prog3(a: t_stmt, b: t_stmt, c: t_stmt) -> t_stmt:
    return t_stmt(_join_lines(a, b, c))


def prog4(a: t_stmt, b: t_stmt, c: t_stmt, d: t_stmt) -> t_stmt:
    return t_stmt(_join_lines(a, b, c, d))


def prog5(a: t_stmt, b: t_stmt, c: t_stmt, d: t_stmt, e: t_stmt) -> t_stmt:
    return t_stmt(_join_lines(a, b, c, d, e))


def surround(before: t_stmt, body: t_section, after: t_stmt) -> t_section:
    return t_section(_join_lines(before, body, after))


def with_saved(r: t_reg, body: t_section) -> t_section:
    return t_section(_join_lines(f"push {r}", body, f"pop {r}"))


def with_saved2(r1: t_reg, r2: t_reg, body: t_section) -> t_section:
    return t_section(_join_lines(
        f"push {r1}",
        f"push {r2}",
        body,
        f"pop {r2}",
        f"pop {r1}"
    ))

# ---------------------------
# Safe no-operand instructions
# ---------------------------

def nop() -> t_stmt:
    return t_stmt("nop")


def cld() -> t_stmt:
    return t_stmt("cld")


def std() -> t_stmt:
    return t_stmt("std")


def clc() -> t_stmt:
    return t_stmt("clc")


def stc() -> t_stmt:
    return t_stmt("stc")


def cmc() -> t_stmt:
    return t_stmt("cmc")


def pushf() -> t_stmt:
    return t_stmt("pushf")


def popf() -> t_stmt:
    return t_stmt("popf")


def lahf() -> t_stmt:
    return t_stmt("lahf")


def cbw() -> t_stmt:
    return t_stmt("cbw")


def cwd() -> t_stmt:
    return t_stmt("cwd")


def stosw() -> t_stmt:
    return t_stmt("stosw")


def stosb() -> t_stmt:
    return t_stmt("stosb")


def lodsw() -> t_stmt:
    return t_stmt("lodsw")


def lodsb() -> t_stmt:
    return t_stmt("lodsb")


def movsw() -> t_stmt:
    return t_stmt("movsw")


def movsb() -> t_stmt:
    return t_stmt("movsb")


def cmpsw() -> t_stmt:
    return t_stmt("cmpsw")


def cmpsb() -> t_stmt:
    return t_stmt("cmpsb")


def scasw() -> t_stmt:
    return t_stmt("scasw")


def scasb() -> t_stmt:
    return t_stmt("scasb")


def xlat() -> t_stmt:
    return t_stmt("xlat")


def xlatb() -> t_stmt:
    return t_stmt("xlatb")


def rep_stosb() -> t_stmt:
    return t_stmt("rep stosb")


def rep_stosw() -> t_stmt:
    return t_stmt("rep stosw")


def rep_movsb() -> t_stmt:
    return t_stmt("rep movsb")


def rep_movsw() -> t_stmt:
    return t_stmt("rep movsw")


# ---------------------------
# 16-bit data movement
# ---------------------------

def mov_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"mov {dst}, {src}")


def mov_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"mov {dst}, {imm}")


def mov_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"mov {dst}, {mem}")


def mov_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"mov {mem}, {src}")


def mov_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"mov word {mem}, {imm}")


def lea_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"lea {dst}, {mem}")


# ---------------------------
# 8-bit data movement
# ---------------------------

def mov_hh(dst: t_half_reg, src: t_half_reg) -> t_stmt:
    return t_stmt(f"mov {dst}, {src}")


def mov_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"mov {dst}, {imm}")


def mov_hm(dst: t_half_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"mov {dst}, byte {mem}")


def mov_mh(mem: t_mem, src: t_half_reg) -> t_stmt:
    return t_stmt(f"mov byte {mem}, {src}")


# ---------------------------
# Arithmetic - 16 bit
# ---------------------------

def add_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"add {dst}, {src}")


def add_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"add {dst}, {imm}")


def add_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"add {dst}, {mem}")


def sub_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"sub {dst}, {src}")


def sub_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sub {dst}, {imm}")


def sub_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"sub {dst}, {mem}")


def sub_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"sub word {mem}, {src}")


def sub_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"sub word {mem}, {imm}")


# ---------------------------
# Arithmetic - 8 bit
# ---------------------------

def add_hh(dst: t_half_reg, src: t_half_reg) -> t_stmt:
    return t_stmt(f"add {dst}, {src}")


def add_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"add {dst}, {imm}")


def sub_hh(dst: t_half_reg, src: t_half_reg) -> t_stmt:
    return t_stmt(f"sub {dst}, {src}")


def sub_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sub {dst}, {imm}")


# ---------------------------
# Bitwise logic - 16 bit
# ---------------------------

def xor_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"xor {dst}, {src}")


def xor_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"xor {dst}, {imm}")


def and_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"and {dst}, {src}")


def and_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"and {dst}, {imm}")


def or_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"or {dst}, {src}")


def or_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"or {dst}, {imm}")


def test_rr(a: t_reg, b: t_reg) -> t_stmt:
    return t_stmt(f"test {a}, {b}")


def test_ri(a: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"test {a}, {imm}")


# ---------------------------
# Bitwise logic - 8 bit
# ---------------------------

def xor_hh(dst: t_half_reg, src: t_half_reg) -> t_stmt:
    return t_stmt(f"xor {dst}, {src}")


def xor_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"xor {dst}, {imm}")


def and_hh(dst: t_half_reg, src: t_half_reg) -> t_stmt:
    return t_stmt(f"and {dst}, {src}")


def and_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"and {dst}, {imm}")


def or_hh(dst: t_half_reg, src: t_half_reg) -> t_stmt:
    return t_stmt(f"or {dst}, {src}")


def or_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"or {dst}, {imm}")


# ---------------------------
# Compare
# ---------------------------

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


def cmp_hh(a: t_half_reg, b: t_half_reg) -> t_stmt:
    return t_stmt(f"cmp {a}, {b}")


def cmp_hi(a: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"cmp {a}, {imm}")


# ---------------------------
# Unary ops
# ---------------------------

def inc_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"inc {dst}")


def dec_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"dec {dst}")


def inc_h(dst: t_half_reg) -> t_stmt:
    return t_stmt(f"inc {dst}")


def dec_h(dst: t_half_reg) -> t_stmt:
    return t_stmt(f"dec {dst}")


def inc_m(dst: t_mem) -> t_stmt:
    return t_stmt(f"inc word {dst}")


def dec_m(dst: t_mem) -> t_stmt:
    return t_stmt(f"dec word {dst}")


def not_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"not {dst}")


def neg_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"neg {dst}")


def not_m(dst: t_mem) -> t_stmt:
    return t_stmt(f"not word {dst}")


def neg_m(dst: t_mem) -> t_stmt:
    return t_stmt(f"neg word {dst}")


# ---------------------------
# Shifts and rotates
# ---------------------------

def shl_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"shl {dst}, {imm}")


def shr_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"shr {dst}, {imm}")


def rol_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"rol {dst}, {imm}")


def ror_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"ror {dst}, {imm}")


def shl_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"shl {dst}, {imm}")


def shr_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"shr {dst}, {imm}")


# ---------------------------
# Stack ops
# ---------------------------

def push_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"push {dst}")


def pop_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"pop {dst}")


def push_m(mem: t_mem) -> t_stmt:
    return t_stmt(f"push word {mem}")


def pop_m(mem: t_mem) -> t_stmt:
    return t_stmt(f"pop word {mem}")


# ---------------------------
# Exchange
# ---------------------------

def xchg_rr(a: t_reg, b: t_reg) -> t_stmt:
    return t_stmt(f"xchg {a}, {b}")


# ---------------------------
# Macro-like building blocks
# These are the main source of richer individuals.
# ---------------------------

def zero_r(dst: t_reg) -> t_stmt:
    return t_stmt(f"xor {dst}, {dst}")


def zero_h(dst: t_half_reg) -> t_stmt:
    return t_stmt(f"xor {dst}, {dst}")


def clear_mem(mem: t_mem) -> t_stmt:
    return t_stmt(f"mov word {mem}, 0")


def copy_add(dst: t_reg, src: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(_join_lines(
        f"mov {dst}, {src}",
        f"add {dst}, {imm}"
    ))


def copy_xor(dst: t_reg, src: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(_join_lines(
        f"mov {dst}, {src}",
        f"xor {dst}, {imm}"
    ))


def twiddle_pair(a: t_reg, b: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(_join_lines(
        f"xor {a}, {b}",
        f"add {b}, {imm}",
        f"sub {a}, {imm}"
    ))


def load_add_store(tmp: t_reg, mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(_join_lines(
        f"mov {tmp}, {mem}",
        f"add {tmp}, {imm}",
        f"mov {mem}, {tmp}"
    ))


def load_xor_store(tmp: t_reg, mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(_join_lines(
        f"mov {tmp}, {mem}",
        f"xor {tmp}, {imm}",
        f"mov {mem}, {tmp}"
    ))


def compare_bump(a: t_reg, b: t_reg) -> t_stmt:
    return t_stmt(_join_lines(
        f"cmp {a}, {b}",
        f"inc {a}",
        f"dec {b}"
    ))


# ---------------------------
# Identity helpers
# Useful for mutation/recombination in typed GP
# ---------------------------

def idr(x: t_reg) -> t_reg:
    return x


def idh(x: t_half_reg) -> t_half_reg:
    return x


def idm(x: t_mem) -> t_mem:
    return x


def idi(x: t_imm) -> t_imm:
    return x


def ids(x: t_stmt) -> t_stmt:
    return x


FUNCTION_SET2 = [
    # section builders
    seq, seq3, seq4, as_section, surround, with_saved, with_saved2,

    # statement builders
    seq_stmt, prog2, prog3, prog4, prog5,

    # no-operand
    nop, cld, std, clc, stc, cmc, pushf, popf, lahf, cbw, cwd,
    stosw, stosb, lodsw, lodsb, movsw, movsb, cmpsw, cmpsb,
    scasw, scasb, xlat, xlatb,
    rep_stosb, rep_stosw, rep_movsb, rep_movsw,

    # data movement
    mov_rr, mov_ri, mov_rm, mov_mr, mov_mi, lea_rm,
    mov_hh, mov_hi, mov_hm, mov_mh,

    # arithmetic
    add_rr, add_ri, add_rm,
    sub_rr, sub_ri, sub_rm, sub_mr, sub_mi,
    add_hh, add_hi, sub_hh, sub_hi,

    # logic
    xor_rr, xor_ri, and_rr, and_ri, or_rr, or_ri, test_rr, test_ri,
    xor_hh, xor_hi, and_hh, and_hi, or_hh, or_hi,

    # compare
    cmp_rr, cmp_ri, cmp_rm, cmp_mr, cmp_mi,
    cmp_hh, cmp_hi,

    # unary
    inc_r, dec_r, inc_h, dec_h, inc_m, dec_m,
    not_r, neg_r, not_m, neg_m,

    # shifts
    shl_ri, shr_ri, rol_ri, ror_ri, shl_hi, shr_hi,

    # stack and exchange
    push_r, pop_r, push_m, pop_m, xchg_rr,

    # macro-like building blocks
    zero_r, zero_h, clear_mem,
    copy_add, copy_xor, twiddle_pair,
    load_add_store, load_xor_store, compare_bump,

    # identities
    idr, idh, idm, idi, ids,
]