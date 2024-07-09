## Memory Dump

The dump is an assembly code for the x86 architecture.
Let's analyze it

    jmp .up ; jumps to the .up label
    .down: ; defines the .down label
    pop eax ; pops the top value of the stack into the eax register. note: at this point the stack is not initialized
    push 0xD68C67D9 ; pushes a value into the top of the stack 
    call eax ; and then calls the address in eax, which is the xor operation
    push 0x1154286C ; same
    call eax
    push 0x1B1A1E19 ; same
    call eax
    push 0x161B2D02 ; same
    call eax
    push 0x1A372608 ; same
    call eax
    push 0x2917094C ; same
    call eax
    mov eax, 4 ; this is the write syscall
    mov ebx, 1 ; this is the file descriptor for stdout
    mov ecx, esp ; ecx points to the data to write
    mov edx, 0x18 ; edx is the number of bytes to write to stdout: 0x18, or 24 bytes. This will print the flag. 
    int 0x80 ; this interrupts to invoke the system call
    mov eax, 1 ; we set eax to 1
    dec ebx ; we decrease it to 0
    int 0x80 ; so we can exit
    .up: call .down ; defines the .up label, pushes the address of the next instruction onto the stack, sets the location at the .down label in the IP registry
    xor [esp+4], ebx ; we xor the value of the address pointed by esp+4 (we move up the stack. this is the latest value pushed to the stack) with the value of ebx
    mov ebx, [esp+4] ; moves the result of the xor operation into ebx
    ret ; returns to the address saved on the top of the stack (the caller)

This function performs a xor operation of the uppermost value of the stack with the value in ebx, saves the result on the top of the stack and on ebx.

    xor [esp+4], ebx
    mov ebx, [esp+4]
    ret

Note that its address is on eax for almost the entire duration of the program's execution because the `call .down` instruction (executed immediately because of the `jmp .up` instruction) sets the address of the next instruction (`xor [esp+4], ebx`) onto the top of the stack, but that address is removed from it and moved on the eax registry by the `pop eax` instruction, which is called right after the `jmp .up` instruction. For this reason the function is invoked every time `call eax` is executed. 

The simplified initial flow is therefore this:
    
    call .down ; saves the address of the "xor [esp+4], ebx" instruction on the stack
    pop eax ; removes that address from the stack right away and puts into the eax registry, so that the xoring function can be called with the "call eax" instruction
    ...

The program can be interpreted as this sequence of actions:

- prepares the address of the xoring function on eax
- calls the xoring function 6 times
- prints the stack on stdout
- exits
    
In other words, the program:

- takes a value from the top of the stack (not initialized)
- XORs it with 0xD68C67D9
- saves the result in the stack (flag chunk 6)
- XORs the result with 0x1154286C
- saves the result in the stack (flag chunk 5)
- XORs the result with 0x1B1A1E19
- saves the result in the stack (flag chunk 4)
- XORs the result with 0x161B2D02
- saves the result in the stack (flag chunk 3)
- XORs the result with 0x1A372608
- saves the result in the stack (flag chunk 2)
- XORs the result with 0x2917094C
- saves the result in the stack (flag chunk 1)
- prints the characters in the stack

We need to find the missing value that we must use to initialize the stack at the beginning of the program in order to print the flag.

What we know:
- the flag is in the NTRLGC{*} format
- this is assembly for x86, so values are represented in little-endian
- the stack elements composing the flag will be printed to stdout starting from the top down to the bottom
- the most recently inserted stack element will contain the start of the flag  

One possible way to reconstruct the initial value is to move through the algorithm backwards.
We know that since the first 4 characters of the flag are NTRL, the last stack element will contain one of the following possible values:

- b'LRTN' if the flag is 24 characters long
- b'RTN\x00' if the flag is 23 characters long
- b'TN\x00\x00' if the flag is 22 characters long
- b'N\x00\x00\x00' if the flag is 21 characters long

and so on. We expect it to not be shorter than 21 characters for simplicity, even though the same reasoning can be iterated for shorter values.
Note that the values are reversed because of the little-endian architecture.

Given this, we can be relatively sure that one of the 4 aforementioned cases will be the right one.

Now, for each case we can xor the first four bytes with each of the values that are pushed in the stack to reconstruct the value needed to correctly initialize the stack.

    initialization_value_1 = 0xD68C67D9 ^ 0x1154286C ^ 0x1B1A1E19 ^ 0x161B2D02 ^ 0x1A372608 ^ 0x2917094C ^ b'LRTN'
    initialization_value_2 = 0xD68C67D9 ^ 0x1154286C ^ 0x1B1A1E19 ^ 0x161B2D02 ^ 0x1A372608 ^ 0x2917094C ^ b'RTN\x00'
    initialization_value_3 = 0xD68C67D9 ^ 0x1154286C ^ 0x1B1A1E19 ^ 0x161B2D02 ^ 0x1A372608 ^ 0x2917094C ^ b'TN\x00\x00'
    initialization_value_4 = 0xD68C67D9 ^ 0x1154286C ^ 0x1B1A1E19 ^ 0x161B2D02 ^ 0x1A372608 ^ 0x2917094C ^ b'N\x00\x00\x00'

Now we just have to run the algorithm with each of the possible initialization values: one of those will give us the complete flag.

The following python algorithm will do everything for us:
    
```python
import struct

blocks = [
    0xD68C67D9, 0x1154286C,
    0x1B1A1E19, 0x161B2D02,
    0x1A372608, 0x2917094C,
]


def chars_to_int(chars) -> int:
    return struct.unpack('>I', chars.encode('utf-8'))[0]


def int_to_chars(integer_value) -> str:
    return struct.pack('>I', integer_value).decode('utf-8')


def check(initial_flag_chars: str):
    flag = ''
    key = chars_to_int(initial_flag_chars)
    for block in blocks[::-1]:
        key = block ^ key
    for block in blocks:
        key = block ^ key
        flag += int_to_chars(key)
    if 'CGLRTN' in flag:
        print(flag[::-1].replace('\x00', ''))


check('LRTN')
check('RTN\x00')
check('TN\x00\x00')
check('N\x00\x00\x00')
```

Another similar algorithm that reaches the same solution in a slightly different way is the following:

```python
import functools
import struct
from typing import List

blocks = [
    0xD68C67D9, 0x1154286C,
    0x1B1A1E19, 0x161B2D02,
    0x1A372608, 0x2917094C,
]


def chars_to_int(chars) -> int:
    return struct.unpack('>I', chars.encode())[0]


def int_to_chars(integer_value) -> str:
    return struct.pack('>I', integer_value).decode()


def check(candidates: List[str]):
    xored = functools.reduce(lambda a, b: a ^ b, blocks)
    for candidate in candidates:
        key = xored ^ chars_to_int(candidate)
        flag = ''
        for block in blocks:
            key ^= block
            flag += int_to_chars(key)
        if 'CGLRTN' in flag:
            print(f'initial value: {hex(xored ^ chars_to_int(candidate))}')
            return print(flag[::-1].replace('\x00', ''))


check(['LRTN', 'RTN\x00', 'TN\x00\x00', 'N\x00\x00\x00'])
```