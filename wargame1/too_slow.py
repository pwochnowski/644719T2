from pwn import *

# p = process("shared/wargame1/too-slow")
p = remote("plzpwn.me",1001)
p.recvline()
for i in range(10):
    n1 = p.recvuntil(" ")[:-1]
    p.recv(2)
    n2 = p.recvuntil(" ")[:-1]
    log.info("adding " + n1 + " + " + n2)
    p.recv()
    p.sendline(str(int(n1) + int(n2)))
    log.info(p.recvline())
log.info(p.recv())
p.interactive()
# p.sendline("c")
log.info(p.recv())
