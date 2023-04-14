import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def encrypt_file(input_file, output_file):
    key = get_random_bytes(32)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print(cipher)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(iv)

        while True:
            chunk = f_in.read(64 * 1024)
            if not chunk:
                break
            encrypted_chunk = cipher.encrypt(pad(chunk, 16))
            f_out.write(encrypted_chunk)

    return key

# def encrypt_file(input_file, output_file):
#     key = get_random_bytes(32)
#     iv = get_random_bytes(16)
#     cipher = AES.new(key, AES.MODE_CBC, iv)

#     with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
#         f_out.write(iv)

#         while True:
#             chunk = f_in.read(64 * 1024)
#             if not chunk:
#                 break
#             encrypted_chunk = cipher.encrypt(pad(chunk, 16))
#             f_out.write(encrypted_chunk)

#     return key

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        iv = f_in.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        while True:
            chunk = f_in.read(64 * 1024)
            if not chunk:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            if len(chunk) != 64 * 1024:
                decrypted_chunk = unpad(decrypted_chunk, 16)
            f_out.write(decrypted_chunk)

# Usage example:
key = encrypt_file('fuck.txt', 'fuck.bin')
# decrypt_file('example_encrypted.bin', 'example_decrypted.pdf', key)