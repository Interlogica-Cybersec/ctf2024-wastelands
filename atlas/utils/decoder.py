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
        print("Usage: python script.py <file_contenente_le_chiavi> <stringa_AES_ECB_256_in_HEX>")
        return

    keys_file = sys.argv[1]
    ciphertext_hex = sys.argv[2]

    try:
        with open(keys_file, 'r') as f:
            keys = f.readlines()
    except FileNotFoundError:
        print("File delle chiavi non trovato.")
        return

    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
    except ValueError:
        print("Stringa di testo cifrata non valida.")
        return

    for key in keys:
        key = key.strip()  # Rimuove spaziature o newline aggiuntivi
        try:
            plaintext = decrypt_aes_ecb(key.encode('utf-8'), ciphertext)
            print(f"Trovata chiave corretta: {key}")
            print("Plaintext:", plaintext.decode('utf-8'))
            return
        except Exception:
            pass  # Se la decrittazione fallisce, passa alla prossima chiave

    print("Nessuna chiave valida trovata.")

if __name__ == "__main__":
    main()
