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
	pass

def main():
	if debug:
		s = process('./death_note')
		pause()
	else:
		s = remote('chall.pwnable.tw', 10201)

	exploit()
	s.interactive()
	s.close()

if __name__ == '__main__':
	main()