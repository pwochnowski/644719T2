intro
===========================

Flag: COMP6447{W3LCOME_M4T3S}

General overview of problems faced
-------------------------------------
Had to follow the instructions + use strings to find the hidden password


Script/Command used
------------------
```
from pwn import *

# p = process("shared/wargame1/intro")
p = remote("plzpwn.me",1000)
line = p.recvuntil(": {")
log.info(line)
address = p.recv(6)
num1 = int(address, 16)

line = p.recvline()
line = p.recvline()
log.info(line)
p.sendline(str(num1))
line = p.recvuntil("MINUS ")
print(line)
address = p.recvuntil("!")[:-1]
p.recv()
num2 = int(address, 16)
p.sendline(str(hex(num1 - num2)))
print(p.recvuntil("me "))
num = p.recv(6)
print(p.recvline())
p.sendline(p16(int(num,16)))
print(p.recvline())
print(p.recvline())
address = p.recvline()
print(address)
b1 = address[:3]
print(address[4:])
b2 = address[3:]
log.info("b2: " + b2[0])
dec = unpack(b1 + b2[0], "all", endian="little")
log.info(dec)
print(p.recv())
p.sendline(str(dec))
print(p.recv())
p.sendline(str(hex(int(dec))))
p.recvuntil("is ")
n1 = p.recvuntil(" ")[:-1]
print(n1)
p.recvuntil("+ ")
n2 = p.recvuntil("?")[:-1]
print(n2)
p.recv()
p.sendline(str(int(n1) + int(n2)))
log.info(p.recv())
p.sendline('password')
p.interactive()
log.info(p.recv())
```
Sorry for the mess

too-slow
=============

Flag: COMP6447{2_SL0W_4_Y0U}

General overview of problems faced
-------------------------------------
Had to follow the instructions


Script/Command used
------------------
```
from pwn import *

# p = process("shared/wargame1/too-slow")
p = remote("plzpwn.me",1001)
p.recvline()
for i in range(10):
    n1 = p.recvuntil(" ")[:-1]
    p.recv(2)
    n2 = p.recvuntil(" ")[:-1]
    log.info("adding " + n1 + " + " + n2)
    p.recv()
    p.sendline(str(int(n1) + int(n2)))
    log.info(p.recvline())
log.info(p.recv())
# p.sendline("cat flag")
log.info(p.recv())
```

