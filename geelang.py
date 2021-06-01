from pwn import *

run="""
INT x 5
PRINT x
END
"""

program = './geelang-compiler'
elf = ELF(program)

global p


p = process(program)
