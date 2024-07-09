import struct


def to_32bit_blocks(values):
    while len(values) % 4 != 0:
        values.append(0)
    blocks = []
    for i in range(0, len(values), 4):
        block = struct.unpack('>I', bytes(values[i:i + 4]))[0]
        blocks.append(block)
    return blocks


def from_32bit_blocks(blocks):
    values = []
    for block in blocks:
        bytes_block = struct.pack('>I', block)
        values.extend(bytes_block)
    return values


def ror32(value, shift):
    shift &= 31
    return ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF


def rol32(value, shift):
    shift &= 31
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def xor32(value1, value2):
    return (value1 ^ value2) & 0xFFFFFFFF


def reg_encrypt(block, key):
    for i in range(0, 3):
        # block = ror32(block, 1)
        block = xor32(block, key)
    return block


def reg_decrypt(block, key):
    for i in range(0, 3):
        block = xor32(block, key)
        # block = rol32(block, 1)
    return block


def encrypt(key, blocks):
    key_value = key
    result = []
    for block in blocks:
        encrypted_block = reg_encrypt(block, key_value)
        result.append(encrypted_block)
        key_value = block
    return result


def decrypt(key, blocks):
    key_value = key
    result = []
    for block in blocks:
        decrypted_block = reg_decrypt(block, key_value)
        result.append(decrypted_block)
        key_value = decrypted_block
    return result


key = 0xABAD1DEA
secret = 'NTRLGC{DataFlow_Rul3z!}'
# reverse secret
secret = secret[::-1]

print(secret)
blocks = to_32bit_blocks(list(map(ord, secret)))
print(blocks)
encrypted_blocks = encrypt(key, blocks)
print(encrypted_blocks)
for i in encrypted_blocks:
    print('0x{0:08X}'.format(i))
decrypted_blocks = decrypt(key, encrypted_blocks)
print(decrypted_blocks)
result = from_32bit_blocks(decrypted_blocks)
print("Result: " + ''.join(map(chr, result)).rstrip('\x00')[::-1])
