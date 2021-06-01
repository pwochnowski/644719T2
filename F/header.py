#!/usr/bin/env python
# UNSW COMP9447 18s2
# Exam Q1 - Pwnable
from pwn import *
import struct


# Exploit Variables
program = './alpha'
host = 'plzpwn.me'
port = 8001
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