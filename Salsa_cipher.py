import struct #this will help us to pack and unpack 32-bit words

def rotate_left(value,shift):
    return ((value<<shift)& 0xffffffff)|(value>>(32-shift)) 
    #value<<shift --> shifts left
    #0xffffffff --> it identifies that this will only work with 32 bit
    # | --> when it completes
    #value>>(32-shift) --> bring the overflow to the right
    # Salsa cipher uses a rotation to mix the data, but Python doesn't have the rotating feature, so implementing it manually
    
def quarterround(a,b,c,d):
    b^=rotate_left((a+d)&0xffffffff,7)
    c^=rotate_left((b+a)&0xffffffff,9)
    d^=rotate_left((c+b)&0xffffffff,13)
    a^=rotate_left((d+c)&0xffffffff,18)
    return a,b,c,d
    #It mixes four 32-bit words using addition modulo 2^32, XOR, and bit rotation
    
def evenround(y):
    z=[0]*16
    z[0],z[1],z[2],z[3]=quarterround(y[0],y[1],y[2],y[3])
    z[5],z[6],z[7],z[4]=quarterround(y[5],y[6],y[7],y[4])
    z[10],z[11],z[8],z[9]=quarterround(y[10],y[11],y[8],y[9])
    z[15],z[12],z[13],z[14]=quarterround(y[15],y[12],y[13],y[14])
    return z

def oddround(x):
    y=[0]*16
    y[0],y[4],y[8],y[12]=quarterround(x[0],x[4],x[8],x[12])
    y[5],y[9],y[13],y[1]=quarterround(x[5],x[9],x[13],x[1])
    y[10],y[14],y[2],y[6]=quarterround(x[10],x[14],x[2],x[6])
    y[15],y[3],y[7],y[11]=quarterround(x[15],x[3],x[7],x[11])
    return y

def doubleround(x):
    return evenround(oddround(x))

def salsa20_hash(state):
    x=state.copy()
    for _ in range(10):
        x=doubleround(x)
    result=[]
    for i in range(16):
        summed=x[i]+state[i]
        masked=summed&0xffffffff
        result.append(masked)
    return result
    # implements the core Salsa20 hash that transforms the input state
    # this function is used to generate the keystream block for encryption
    
    # makes the copy of the input state
    # then it applies 10 double rounds
    # then it adds the original state to the result to produce the final block
    
def salsa20_block(key,nonce,counter):
    constants=[0x61707865, 0x3320646e, 0x79622d32, 0x6b206574] 
    #0x61707865 --> expa
    #0x3320646e --> nd 3
    #0x79622d32 --> 2-by
    #0x6b206574 --> te k
    key_words=list(struct.unpack('<8I',key))
    nonce_words=list(struct.unpack('<2I',nonce))
    counter_words=[counter&0xffffffff,(counter>>32)&0xffffffff]
    state=[0]*16
    state[0]=constants[0]
    state[1:5]=key_words[0:4]
    state[5]=constants[1]
    state[6:7]=nonce_words
    state[7:9]=counter_words
    state[10]=constants[2]
    state[11:15]=key_words[4:8]
    state[15]=constants[3]
    return salsa20_hash(state)

def salsa20_encrypt(key,nonce,plaintext):
    ciphertext=bytearray()
    block_count=(len(plaintext)+63)//64
    for counter in range(block_count):
        block=salsa20_block(key,nonce,counter)
        keystream=b''.join(struct.pack('<I',word) for word in block)
        block_bytes=plaintext[counter*64:(counter+1)*64]
        ciphertext.extend(bytes(a^b for a,b in zip(block_bytes,keystream)))
    return bytes(ciphertext)

key = b'0123456789abcdef0123456789abcdef'
nonce = b'12345678'
message = b"Hi my name is Tushig"
print("Original message:", message)
ciphertext = salsa20_encrypt(key,nonce,message)
print("Encrypted message:", ciphertext.hex())
decrypted = salsa20_encrypt(key,nonce,ciphertext)
print("Decrypted message:", decrypted)
    
    

