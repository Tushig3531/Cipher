
def round_left(round, shift, bit=32):
    left=(round*(2**shift))%(2**bit) 
    right=round//(2**(bit-shift)) #extracting the bits that fall off on the left
    rotated=left | right
    return rotated%(2**bit)

def round_function(r,subkey):
    rotated=round_left(r,1,32)
    result=rotated^subkey
    return result%(2**32)


def generate_subkey(masterkey, rounds=16):
    subkeys=[]
    for i in range(rounds):
        subkey=round_left(masterkey,i,32)
        subkeys.append(subkey)
    return subkeys

def encryption_block(block,subkeys):
    L=block//(2**32)
    R=block%(2**32)
    
    for subkey in subkeys:
        L,R=R,L^round_function(R,subkey)
    return (L*(2**32))+R

def decryption_block(block,subkeys):
    L=block//(2**32)
    R=block%(2**32)
    
    for subkey in reversed(subkeys):
        L,R=R^round_function(L,subkey),L
    return (L*(2**32))+R

def pad(data):
    pad_len=8-(len(data)%8)
    return data+bytes([pad_len])*pad_len

def unpad(data):
    pad_len=data[-1]
    if pad_len<1 or pad_len>8:
        raise ValueError("Hhhe you failed on padding")
    return data[:-pad_len]

def encrypt(plaintext,masterkey,rounds=16):
    subkey=generate_subkey(masterkey,rounds)
    padded=pad(plaintext)
    ciphertext=b''
    
    for i in range(0,len(padded),8):
        block=int.from_bytes(padded[i:i+8], byteorder="big")
        
        encrypt_block=encryption_block(block,subkey)
        ciphertext+=encrypt_block.to_bytes(8,byteorder="big")
    return ciphertext
        
def decrypt(ciphertext,masterkey,rounds=16):
    subkey=generate_subkey(masterkey,rounds)
    plaintext=b''
    
    for i in range(0,len(ciphertext),8):
        block=int.from_bytes(ciphertext[i:i+8],byteorder="big")
        decrypt_block=decryption_block(block,subkey)
        plaintext+=decrypt_block.to_bytes(8,byteorder="big")
    return unpad(plaintext)
    
    
if __name__=="__main__":
    masterkey=0x0F1571C5
    rounds=16
    message = b"Hello, my name is Tushig Erdenebulgan"
    print("Original Message:")
    print(message)

    ciphertext = encrypt(message, masterkey, rounds)
    print("\nCiphertext (in hexadecimal):")
    print(ciphertext.hex())

    decrypted_message = decrypt(ciphertext, masterkey, rounds)
    print("\nDecrypted Message:")
    print(decrypted_message) 
    
    
    
    
    