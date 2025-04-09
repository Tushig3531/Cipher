lfsr_state=0
fsm_state=0

def init_state(key,iv):
    global lfsr_state,fsm_state
    initial_value=(key^iv)&0xFFFF
    lfsr_state=initial_value
    fsm_state=(initial_value>>3)&0xffff
    
def lfsr():
    global lfsr_state
    t1=(lfsr_state>>15)&1
    t2=(lfsr_state>>13)&1
    t3=(lfsr_state>>12)&1
    t4=(lfsr_state>>10)&1
    new_bit=t1^t2^t3^t4
    
    lfsr_state=((lfsr_state<<1)&0xffff)|new_bit
    
    return (lfsr_state>>15)&1

def fsm(input_bit):
    global fsm_state
    rotated=((fsm_state>>3)|(fsm_state<<(16-3)))&0xffff
    fsm_state=((fsm_state+input_bit)^rotated)&0xffff
    return fsm_state

def generate_keystream():
    byte_value=0
    for _ in range(8):
        lfsr_bit=lfsr()
        fms_value=fsm(lfsr_bit)
        keystream=lfsr_bit^(fms_value&1)
        byte_value=(byte_value<<1)|keystream
    return byte_value

def encrypt(plaintext,key,iv):
    init_state(key,iv)
    ciphertext=""
    for character in plaintext:
        plaintext_byte=ord(character)
        keystream_byte=generate_keystream()
        cipher_byte=plaintext_byte^keystream_byte
        ciphertext+="{:02x}".format(cipher_byte)
    return ciphertext

def decrypt(ciphertext,key,iv):
    init_state(key,iv)
    plaintext=""
    for i in range(0,len(ciphertext),2):
        cipher_byte=int(ciphertext[i:i+2],16)
        keystream_byte=generate_keystream()
        plaintext_byte=cipher_byte^keystream_byte
        plaintext+=chr(plaintext_byte)
    return plaintext

key=0x1234
iv=0xABCD
plaintext="Tushig Erdenebulgan" 
print("Plaintext:",plaintext)
ciphertext=encrypt(plaintext,key,iv)
decrypted_plaintext=decrypt(ciphertext,key,iv)
print("Encrypted:",ciphertext)
print("Decrypted:",decrypted_plaintext)       