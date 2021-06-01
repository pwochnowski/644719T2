CC         := gcc
CFLAGS     := -fno-stack-protector -no-pie -Q -v -m32 -O0
INTEL_ASM  := -masm=intel

all: clean build

build:
	$(CC) $(INTEL_ASM) $(CFLAGS) -o format_prac format_prac.c 

clean:
	rm -f format_prac


