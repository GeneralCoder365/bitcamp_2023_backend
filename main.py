import aes256 as encryptor
import falcon
from github import Github, UnknownObjectException
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def make_encr_sk_pk():
    sk = get_random_bytes(32)
    salt = get_random_bytes(16)
    
    pk = AES.new(sk, AES.MODE_CBC, salt)
    
    return [sk, pk]


def encrypt(pk, file_ext: str, message: bytes) -> bytes:
    # key = encryptor.encrypt_file(input_file, output_file)
    
    # key = get_random_bytes(32)
    # iv = get_random_bytes(16)
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    
    

    # with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
    #     f_out.write(iv)

    #     while True:
    #         chunk = f_in.read(64 * 1024)
    #         if not chunk:
    #             break
    #         encrypted_chunk = cipher.encrypt(pad(chunk, 16))
    #         f_out.write(encrypted_chunk)
    
    output_file_contents = bytes()
    # while True:
    #     chunk = message.read(64 * 1024)
    for i in range(0, len(message), 64 * 1024):
        chunk = message[i:i+64*1024]
        if not chunk:
            break
        encrypted_chunk = pk.encrypt(pad(chunk, 16))
        output_file_contents += encrypted_chunk
    
    
    
    result = bytes(file_ext, 'utf-8') + bytes("Ω", 'utf-8') + key
    # print(result)
    # print(bytes('Ω', 'utf-8'))
    # print(result.find(bytes('Ω', 'utf-8')))
    return [result, output_file_contents]


def decrypt(input_file, key_ext_bytes: bytes):
    key_ext = key_ext_bytes.split(bytes('Ω', 'utf-8'))
    
    output_file_ext = key_ext[0].decode('utf-8')
    key = key_ext[1]
    
    
    file_rel_path = "/".join((input_file.split('/')[:-1])) + "/" # path to file
    file_details = ((input_file.split('/'))[-1]).split('.') # file name with extension split by .
    file_ext = file_details[-1] # file extension
    file_name = ".".join(file_details[:-1]) # file name without extension
    
    output_file = file_rel_path + file_name + "_decrypted" + "." + output_file_ext
    if (output_file[0] == "/"):
        output_file = (output_file.split("/"))[1]
    
    # print(file_rel_path, file_name, file_ext, output_file)
    
    return encryptor.decrypt_file(input_file, output_file, key)


def encrypt_github(username, filename):
    GITHUB_API_TOKEN = "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"
    
    github_object = Github(GITHUB_API_TOKEN)
    repository = github_object.get_user().get_repo("qsafe_storage")
    
    
    try:
        contents = repository.get_contents(username + "/" + filename)
        
        message = bytes(contents.decoded_content)
        
        encrypted_details = encrypt(filename.split(".")[-1], message)
        
        public_key = encrypted_details[0]
        output_file_contents = encrypted_details[1]
        
        
        # if output file already exists, delete it
        filename = (filename.split('/')[-1]).split('.')
        filename = ".".join(filename[:-1])
        try:
            repository.delete_file(username + "/" + filename + ".bin", "deleting ofile", contents.sha)
        except UnknownObjectException:
            pass
        
        try:
            output_file = repository.create_file(username + "/" + filename + ".bin", "encrypting ofile", output_file_contents)
            return public_key
        except UnknownObjectException:
            pass
    
    except UnknownObjectException:
        pass
            

encrypt_github("qsafe_storage", "test.txt")



def decrypt_github(username, filename, public_key):
    GITHUB_API_TOKEN = "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"
    
    github_object = Github(GITHUB_API_TOKEN)
    repository = github_object.get_user().get_repo("qsafe_storage")
    
    
    try:
        contents = repository.get_contents(username + "/" + filename)
        
        message = bytes(contents.decoded_content)
        
        encrypted_details = encrypt(filename.split(".")[-1], message)
        
        public_key = encrypted_details[0]
        output_file_contents = encrypted_details[1]
        
        
        # if output file already exists, delete it
        filename = (filename.split('/')[-1]).split('.')
        filename = ".".join(filename[:-1])
        try:
            repository.delete_file(username + "/" + filename + ".bin", "deleting ofile", contents.sha)
        except UnknownObjectException:
            pass
        
        try:
            output_file = repository.create_file(username + "/" + filename + ".bin", "encrypting ofile", output_file_contents)
            return public_key
        except UnknownObjectException:
            pass
    
    except UnknownObjectException:
        pass





#! NEED TO WRITE WAY TO CLEAN UP CACHED FILES ON USER SYSTEMS
# def clean(file_path):
#     file_rel_path = "/".join((file_path.split('/')[:-1])) + "/" # path to file
#     file_details = ((file_path.split('/'))[-1]).split('.') # file name with extension split by .
#     file_ext = file_details[-1] # file extension
#     file_name = ".".join(file_details[:-1]) # file name without extension
    
#     input_file = file_path



# key_ext_bytes = encrypt('fuck.txt')
# decrypt('fuck.bin', key_ext_bytes)
# decrypt('Booker_Commercial_Medium.bin', key_ext_bytes)



def get_verification_sk_pk():
    sk = falcon.SecretKey(512)
    pk = falcon.PublicKey(sk)
    
    return [sk, pk]

def get_signature(sk, message: str="nosleepfml"):
    message = bytes(message, 'utf-8')
    
    return sk.sign(message)


# verify only works if the sig was generated with the real person's sk
# so, only checks against a known message and the known sig of that message
# to see if pk is derived from the valid sk
def verify(sig, pk, message: str="nosleepfml"):
    message = bytes(message, 'utf-8')
    
    return pk.verify(message, sig)