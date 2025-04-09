def initialize(key, IV, register_length=10):
    lfsr=[]
    for bit in key:
        number=int(bit)
        lfsr.append(number)
    nlfsr=[]
    for bit in IV:
        number=int(bit)
        nlfsr.append(number)
        
    while len(lfsr)<register_length:
        lfsr.append(0)
    while len(nlfsr)<register_length:
        nlfsr.append(0)
        
    return lfsr,nlfsr
        
def lfsr_feedback(lfsr):
    feedback=lfsr[0]^lfsr[3]^lfsr[5]
    return feedback

def nlfsr_feedback(nlfsr):
    feedback=nlfsr[0]^(nlfsr[1]&nlfsr[2])^nlfsr[4]
    return feedback

def combine_keystream_bit(lfsr,nlfsr):
    combined=(lfsr[2]^nlfsr[2])^(lfsr[4]&nlfsr[4])
    return combined&1

def update_register(lfsr,nlfsr):
    new_bit_lfsr=lfsr_feedback(lfsr)
    new_bit_nlfsr=nlfsr_feedback(nlfsr)
    lfsr=[new_bit_lfsr]+lfsr[:-1]
    nlfsr=[new_bit_nlfsr]+nlfsr[:-1]
    return lfsr,nlfsr

def encrypt(plaintext,key,IV):
    lfsr,nlfsr=initialize(key,IV,register_length=10)
    ciphertext=""
    keystream=[]
    for bit in plaintext:
        keystream_bit=combine_keystream_bit(lfsr,nlfsr)
        keystream.append(keystream_bit)
        cipher_bit=int(bit)^keystream_bit
        ciphertext+=str(cipher_bit)
        lfsr,nlfsr=update_register(lfsr,nlfsr)
    return ciphertext,keystream

def decrypt(ciphertext,key,IV):
    return encrypt(ciphertext,key,IV)[0]

def binary_to_text(binary_str):
    binary_str=binary_str.replace(" ","")
    text=""
    for i in range(0,len(binary_str),8):
        byte=binary_str[i:i+8]
        ascii_code=int(byte,2)
        text+=chr(ascii_code)
    return text


plaintext="Tushig Erdenebulgan"
binary_plaintext=""


for character in plaintext:
    ascii_value=ord(character)
    binary_character=format(ascii_value,'08b')
    binary_plaintext+=binary_character+" "
    
binary_plaintext=binary_plaintext.strip()
binary_plaintext_no_spaces=binary_plaintext.replace(" ", "")
key="1100101010"
IV="1011010011"



print(plaintext)
print(binary_plaintext)
ciphertext,keystream=encrypt(binary_plaintext_no_spaces,key,IV)
recovered_plaintext = decrypt(ciphertext,key,IV)
recovered_plaintext_text=binary_to_text(recovered_plaintext)

    
print("Plaintext:",plaintext)
print("Binary Plaintext:",binary_plaintext)
print("Keystream:", ''.join(map(str,keystream)))
print("Ciphertext:",ciphertext)
print("Recovered:",recovered_plaintext)
print("Decrypt:",recovered_plaintext_text)



    
    
    
        
    