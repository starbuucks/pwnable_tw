# Death Note

`heap`

## Code analysis

가장 큰 문제 : minus indexing이 가능함 -> got overwrite 가능(add)

read_input 함수는 null로 끝나지 않을 수 있음

is_printable은 중간에 null 넣으면 우회가능

```shell
gdb-peda$ vmmap
Start      End        Perm	Name
0x08048000 0x08049000 r-xp	/home/starbuucks/pwnable_tw/Death Note/death_note
0x08049000 0x0804a000 r-xp	/home/starbuucks/pwnable_tw/Death Note/death_note
0x0804a000 0x0804b000 rwxp	/home/starbuucks/pwnable_tw/Death Note/death_note
0xf7d73000 0xf7d74000 rwxp	mapped
0xf7d74000 0xf7f21000 r-xp	/lib32/libc-2.23.so
0xf7f21000 0xf7f22000 ---p	/lib32/libc-2.23.so
0xf7f22000 0xf7f24000 r-xp	/lib32/libc-2.23.so
0xf7f24000 0xf7f25000 rwxp	/lib32/libc-2.23.so
0xf7f25000 0xf7f28000 rwxp	mapped
0xf7f40000 0xf7f41000 rwxp	mapped
0xf7f41000 0xf7f44000 r--p	[vvar]
0xf7f44000 0xf7f46000 r-xp	[vdso]
0xf7f46000 0xf7f69000 r-xp	/lib32/ld-2.23.so
0xf7f69000 0xf7f6a000 r-xp	/lib32/ld-2.23.so
0xf7f6a000 0xf7f6b000 rwxp	/lib32/ld-2.23.so
0xffeb3000 0xffed4000 rwxp	[stack]
```

rwx 권한 있는 영역도 많다.

이거 그냥 shellcode를 got로 올려서 실행하면 안되나?

단, printable한지 검사하기 때문에 0x20 ~ 0x7e 범위 내의 ascii code로만 shellcode를 작성해야 됨.

null로 우회하면 strdup를 통한 복사가 안 이뤄지기 때문에 정면돌파 할 수 밖에 없음.