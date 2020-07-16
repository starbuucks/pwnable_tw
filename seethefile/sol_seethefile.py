#pwnable.tw
#seethefile

from pwn import *

debug = True

def exploit():
    pass

if debug:
    s = process('./seethefile')
    pause()
else:
    s = remote('chall.pwnable.tw', 10200)

exploit()
s.interactive()
s.close()
