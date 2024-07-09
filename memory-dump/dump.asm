jmp .up
.down:
pop eax
push 0xD68C67D9
call eax
push 0x1154286C
call eax
push 0x1B1A1E19
call eax
push 0x161B2D02
call eax
push 0x1A372608
call eax
push 0x2917094C
call eax
mov eax, 4
mov ebx, 1
mov ecx, esp
mov edx, 0x18
int 0x80
mov eax, 1
dec ebx
int 0x80
.up: call .down
xor [esp+4], ebx
mov ebx, [esp+4]
ret