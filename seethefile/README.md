# seethefile

>Can you see anything?
>
>Get a shell for me.
>
>nc chall.pwnable.tw 10200
>
>[seethefile](https://pwnable.tw/static/chall/seethefile)
>
>[libc.so](https://pwnable.tw/static/libc/libc_32.so.6)

## given file
```shell
$ file seethefile 
seethefile: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.32, BuildID[sha1]=04e6f2f8c85fca448d351ef752ff295581c2650d, not stripped

$ checksec seethefile
[*] '/home/starbuucks/pwnable_tw/seethefile/seethefile'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)

```

## code analysis
1. main()
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  char nptr[32]; // [esp+Ch] [ebp-2Ch] BYREF
  unsigned int v5; // [esp+2Ch] [ebp-Ch]

  v5 = __readgsdword(0x14u);
  init();
  welcome();
  while ( 1 )
  {
    menu();
    __isoc99_scanf("%s", nptr);                 // stack overflow!
    switch ( atoi(nptr) )
    {
      case 1:
        openfile();
        break;
      case 2:
        readfile();
        break;
      case 3:
        writefile();
        break;
      case 4:
        closefile();
        break;
      case 5:
        printf("Leave your name :");
        __isoc99_scanf("%s", name);             // overflow! (bss)
        printf("Thank you %s ,see you next time\n", name);// fsb!!
        if ( fp )
          fclose(fp);
        exit(0);
        return result;
      default:
        puts("Invaild choice");
        exit(0);
        return result;
    }
  }
}
```

in the main function, we can make overflow or trigger _format string bug_ 

2. 