from evo_types import *
import threading as _threading
import datetime as _dt
import random as _random

# Thread-local label counter — reset once per tree before assembly generation.
_label_local = _threading.local()


def reset_labels() -> None:
    _label_local.counter = 0


def _new_label() -> str:
    if not hasattr(_label_local, "counter"):
        _label_local.counter = 0
    lb = f"_l{_label_local.counter}"
    _label_local.counter += 1
    return lb



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
# Memory address constructors
# Return t_mem so any instruction accepting t_mem can use them.
# ---------------------------

def mem_bx_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[bx+{imm}]")


def mem_si_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[si+{imm}]")


def mem_di_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[di+{imm}]")


def mem_bp_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[bp+{imm}]")


def mem_bxsi_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[bx+si+{imm}]")


def mem_bxdi_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[bx+di+{imm}]")


def mem_bpsi_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[bp+si+{imm}]")


def mem_bpdi_disp(imm: t_imm) -> t_mem:
    return t_mem(f"[bp+di+{imm}]")


# ---------------------------
# Carry arithmetic (adc / sbb)
# ---------------------------

def adc_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"adc {dst}, {src}")


def adc_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"adc {dst}, {imm}")


def adc_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"adc {dst}, word {mem}")


def sbb_rr(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(f"sbb {dst}, {src}")


def sbb_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sbb {dst}, {imm}")


def sbb_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"sbb {dst}, word {mem}")


# ---------------------------
# Arithmetic shifts and rotate-through-carry
# ---------------------------

def sar_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sar {dst}, {imm}")


def sal_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sal {dst}, {imm}")


def sar_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sar {dst}, {imm}")


def sal_hi(dst: t_half_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"sal {dst}, {imm}")


def rcl_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"rcl {dst}, {imm}")


def rcr_ri(dst: t_reg, imm: t_imm) -> t_stmt:
    return t_stmt(f"rcr {dst}, {imm}")


# ---------------------------
# Shift / rotate by CL
# Pair with mov cl, imm to get flexible shift amounts at runtime.
# ---------------------------

def shl_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"shl {dst}, cl")


def shr_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"shr {dst}, cl")


def sar_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"sar {dst}, cl")


def rol_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"rol {dst}, cl")


def ror_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"ror {dst}, cl")


def rcl_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"rcl {dst}, cl")


def rcr_rc(dst: t_reg) -> t_stmt:
    return t_stmt(f"rcr {dst}, cl")


# ---------------------------
# Memory-destination arithmetic / logic
# Currently missing: add/xor/or/and [mem], src
# ---------------------------

def add_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"add word {mem}, {src}")


def add_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"add word {mem}, {imm}")


def xor_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"xor word {mem}, {src}")


def xor_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"xor word {mem}, {imm}")


def or_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"or word {mem}, {src}")


def or_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"or word {mem}, {imm}")


def and_mr(mem: t_mem, src: t_reg) -> t_stmt:
    return t_stmt(f"and word {mem}, {src}")


def and_mi(mem: t_mem, imm: t_imm) -> t_stmt:
    return t_stmt(f"and word {mem}, {imm}")


# ---------------------------
# Multiply
# mul/imul write dx:ax implicitly — useful for offset calculations.
# ---------------------------

def mul_r(src: t_reg) -> t_stmt:
    return t_stmt(f"mul {src}")


def imul_r(src: t_reg) -> t_stmt:
    return t_stmt(f"imul {src}")


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


def copy_neg(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(_join_lines(
        f"mov {dst}, {src}",
        f"neg {dst}"
    ))


def copy_not(dst: t_reg, src: t_reg) -> t_stmt:
    return t_stmt(_join_lines(
        f"mov {dst}, {src}",
        f"not {dst}"
    ))


def with_flags_saved(body: t_stmt) -> t_stmt:
    return t_stmt(_join_lines("pushf", body, "popf"))


def with_saved_s(r: t_reg, body: t_stmt) -> t_stmt:
    """Push r, execute body, pop r — t_stmt variant of with_saved."""
    return t_stmt(_join_lines(f"push {r}", body, f"pop {r}"))


def with_saved2_s(r1: t_reg, r2: t_reg, body: t_stmt) -> t_stmt:
    """Push r1 and r2, execute body, pop both — t_stmt variant of with_saved2."""
    return t_stmt(_join_lines(f"push {r1}", f"push {r2}", body, f"pop {r2}", f"pop {r1}"))


# Step-write: write register to [ptr], advance ptr — classic imp/writer pattern.

def write_step_si(val: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"mov [si], {val}", f"add si, {step}"))


def write_step_di(val: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"mov [di], {val}", f"add di, {step}"))


def write_step_bx(val: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"mov [bx], {val}", f"add bx, {step}"))


# Step-read: load from [ptr] into register, advance ptr — scanner pattern.

def read_step_si(dst: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"mov {dst}, [si]", f"add si, {step}"))


def read_step_di(dst: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"mov {dst}, [di]", f"add di, {step}"))


# Step-xor: XOR [ptr] with register, advance ptr — XOR-bomber pattern.

def xor_step_si(val: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"xor word [si], {val}", f"add si, {step}"))


def xor_step_di(val: t_reg, step: t_imm) -> t_stmt:
    return t_stmt(_join_lines(f"xor word [di], {val}", f"add di, {step}"))


# ---------------------------
# Control flow — labels and jumps
# reset_labels() must be called before each tree is assembled.
# ---------------------------

def loop_back(body: t_stmt, jmp: t_jmp) -> t_stmt:
    """Backward-jump loop: label: [body]; jmp label"""
    lb = _new_label()
    return t_stmt(_join_lines(f"{lb}:", body, f"{jmp} {lb}"))


def if_skip(jmp: t_jmp, body: t_stmt) -> t_stmt:
    """Forward jump: if condition taken, skip body"""
    lb = _new_label()
    return t_stmt(_join_lines(f"{jmp} {lb}", body, f"{lb}:"))


def loop_cx(body: t_stmt) -> t_stmt:
    """CX-counted loop using the loop instruction (decrements CX, jumps if non-zero)"""
    lb = _new_label()
    return t_stmt(_join_lines(f"{lb}:", body, f"loop {lb}"))


def subroutine(caller: t_stmt, jmp: t_jmp, callee: t_stmt) -> t_stmt:
    """Loop that calls a subroutine: lb_loop: [caller]; call lb_func; jmp lb_loop; lb_func: [callee]; ret"""
    lb_loop = _new_label()
    lb_func = _new_label()
    return t_stmt(_join_lines(
        f"{lb_loop}:",
        caller,
        f"call {lb_func}",
        f"{jmp} {lb_loop}",
        f"{lb_func}:",
        callee,
        "ret"
    ))


# ---------------------------
# General displaced addressing
# More composable than the 8 specific mem_*_disp functions.
# Works on any t_mem terminal including indexed ones like [bx+si].
# ---------------------------

def mem_disp(addr: t_mem, imm: t_imm) -> t_mem:
    """[reg] + imm → [reg+imm];  [bx+si] + 4 → [bx+si+4]"""
    return t_mem(str(addr)[:-1] + f"+{imm}]")


# ---------------------------
# Data word — embed literal bytes in the code stream
# ---------------------------

def dw(imm: t_imm) -> t_stmt:
    return t_stmt(f"dw {imm}")


# ---------------------------
# Unconditional jumps to register / memory
# ---------------------------

def jmp_r(reg: t_reg) -> t_stmt:
    return t_stmt(f"jmp {reg}")


def jmp_m(mem: t_mem) -> t_stmt:
    return t_stmt(f"jmp {mem}")


# ---------------------------
# Extended REP prefix combinations
# The 4 hardcoded rep_* above cover stos/movs.
# These cover lods, scas, cmps with all prefix variants.
# ---------------------------

def rep_lodsw() -> t_stmt:
    return t_stmt("rep lodsw")


def rep_lodsb() -> t_stmt:
    return t_stmt("rep lodsb")


def rep_scasw() -> t_stmt:
    return t_stmt("rep scasw")


def rep_scasb() -> t_stmt:
    return t_stmt("rep scasb")


def repe_cmpsw() -> t_stmt:
    return t_stmt("repe cmpsw")


def repe_cmpsb() -> t_stmt:
    return t_stmt("repe cmpsb")


def repne_cmpsw() -> t_stmt:
    return t_stmt("repne cmpsw")


def repne_cmpsb() -> t_stmt:
    return t_stmt("repne cmpsb")


def repe_scasw() -> t_stmt:
    return t_stmt("repe scasw")


def repe_scasb() -> t_stmt:
    return t_stmt("repe scasb")


def repne_scasw() -> t_stmt:
    return t_stmt("repne scasw")


def repne_scasb() -> t_stmt:
    return t_stmt("repne scasb")


# ---------------------------
# Pointer loads — LES / LDS
# ---------------------------

def les_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"les {dst}, {mem}")


def lds_rm(dst: t_reg, mem: t_mem) -> t_stmt:
    return t_stmt(f"lds {dst}, {mem}")


# ---------------------------
# Random number generator macros
# Ported from the reference grammar's lcg / xor-shift patterns.
# ---------------------------

def lcg_init(reg: t_reg) -> t_stmt:
    """Seed AX with a time-based value, then apply one LCG step into AX."""
    seed = hex(int(_dt.datetime.now().timestamp()) & 0xFFFF)
    return t_stmt(_join_lines(
        f"mov ax, {seed}",
        f"mov {reg}, 0x5D45",
        f"mul {reg}",
        f"add ax, 0xB27F"
    ))


def xor_shift(reg1: t_reg, reg2: t_reg) -> t_stmt:
    """XOR-shift PRNG: seed reg1 and reg2 with random constants, then mix."""
    v1 = hex(_random.randint(1, 65535))
    v2 = hex(_random.randint(1, 65535))
    return t_stmt(_join_lines(
        f"mov {reg1}, {v1}",
        f"mov {reg2}, {v2}",
        f"xor {reg1}, {reg2}",
        f"shl {reg1}, 7",
        f"shr {reg2}, 5",
        f"xor {reg1}, {reg2}"
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


def idj(x: t_jmp) -> t_jmp:
    return x


FUNCTION_SET2 = [
    # statement sequence builders (return t_stmt, 2-5 t_stmt children)
    seq_stmt, prog2, prog3, prog4, prog5,

    # control flow — return t_stmt so they're reachable from the t_stmt root
    loop_back, if_skip, loop_cx, subroutine,

    # push/pop wrappers (t_stmt version — preserve a register around a body)
    with_saved_s, with_saved2_s, with_flags_saved,

    # data movement
    mov_rr, mov_ri, mov_rm, mov_mr, mov_mi, lea_rm,
    mov_hh, mov_hi, mov_hm, mov_mh,
    les_rm, lds_rm,

    # arithmetic
    add_rr, add_ri, add_rm,
    sub_rr, sub_ri, sub_rm, sub_mr, sub_mi,
    add_hh, add_hi, sub_hh, sub_hi,

    # carry arithmetic
    adc_rr, adc_ri, adc_rm,
    sbb_rr, sbb_ri, sbb_rm,

    # logic
    xor_rr, xor_ri, and_rr, and_ri, or_rr, or_ri, test_rr, test_ri,
    xor_hh, xor_hi, and_hh, and_hi, or_hh, or_hi,

    # memory-destination arithmetic / logic
    add_mr, add_mi,
    xor_mr, xor_mi,
    or_mr, or_mi,
    and_mr, and_mi,

    # compare
    cmp_rr, cmp_ri, cmp_rm, cmp_mr, cmp_mi,
    cmp_hh, cmp_hi,

    # unary
    inc_r, dec_r, inc_h, dec_h, inc_m, dec_m,
    not_r, neg_r, not_m, neg_m,

    # multiply
    mul_r, imul_r,

    # shifts and rotates
    shl_ri, shr_ri, rol_ri, ror_ri, shl_hi, shr_hi,
    sar_ri, sal_ri, sar_hi, sal_hi, rcl_ri, rcr_ri,
    shl_rc, shr_rc, sar_rc, rol_rc, ror_rc, rcl_rc, rcr_rc,

    # stack and exchange
    push_r, pop_r, push_m, pop_m, xchg_rr,

    # unconditional jumps to register / memory
    jmp_r, jmp_m,

    # data word embedding
    dw,

    # memory address constructors (general and specific displaced/indexed)
    mem_disp,
    mem_bx_disp, mem_si_disp, mem_di_disp, mem_bp_disp,
    mem_bxsi_disp, mem_bxdi_disp, mem_bpsi_disp, mem_bpdi_disp,

    # macro-like building blocks
    zero_r, zero_h, clear_mem,
    copy_add, copy_xor, twiddle_pair,
    load_add_store, load_xor_store, compare_bump,
    copy_neg, copy_not,
    write_step_si, write_step_di, write_step_bx,
    read_step_si, read_step_di,
    xor_step_si, xor_step_di,

    # random number generator macros
    lcg_init, xor_shift,

    # identities — allow crossover/mutation to insert type-compatible stubs
    idr, idh, idm, idi, ids, idj,
]