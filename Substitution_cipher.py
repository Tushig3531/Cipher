import random
import string

useg=list(string.ascii_uppercase+string.ascii_lowercase+string.punctuation+string.digits+string.whitespace+" ")

def generating_key(useg):
    holison_useg=useg.copy()
    random.shuffle(holison_useg)
    return holison_useg

def encrypt(text,key,useg):
            encrypted=[key[useg.index(c)] for c in text]
            return "".join(encrypted)
def decrypt(text,key,useg): 
            decrypted=[useg[key.index(c)] for c in text]
            return "".join(decrypted)
generated_key=generating_key(useg)

message="Sainuu namaig Tushig gedeg bi 21 nastai"
encrypted_text=encrypt(message,generated_key,useg)
decrypted_text=decrypt(encrypted_text,generated_key,useg)
print(encrypted_text)
print(decrypted_text)
