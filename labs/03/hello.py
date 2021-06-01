from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
# gdb.attach(p)

payload = """
    call a
    a:
    int3
    pop ecx;
    mov eax, 0x4;
    mov ebx, 0x1;
    add ecx, 0x16;
    mov edx, 0x8;
    int 0x80;
"""


compiled = asm(payload)
print(compiled)
print(len(compiled))
p = process("./runner")
gdb.attach(p)
p.sendline(compiled + "ABCDEFG")
p.interactive()



