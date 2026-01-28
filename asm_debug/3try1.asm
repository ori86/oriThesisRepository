bits 16
org 0
start:
push cs
pop ds
push cs
pop es
cld
xor di, di
mov dx, si
jmp start
times 510-($-$$) db 0x90
