def majority(x,y,z):
    return (x&y)|(x&z)|(y&z) #Given three bits x,y and z, define majority(x,y,z) to be the majority vote function, that is, if the majority of x,y, and z are 0, the function reutnrs 0; otherwiste it returns 1. Since there are an odd numbers of bits, there cannot be a tie, so this function is well defined. 

def clock_register(register,taps): #register and the list of tap positions
    feedback_bit=0
    for tap in taps:
        feedback_bit ^=register[tap] #XOR-ing the tap in the list of position which is in register, and XOR-ing
    register=[feedback_bit]+register[::-1] #after that process register needs to shift and inserted the first feedback bit and the last bit
    return register

def new_bits(register, bits):
    for bit in bits:
        register=clock_register(register,[])
        register[0]=bit
    return register

def tushig_keystream(key,frame,n_bits):
    x=[0]*19
    y=[0]*22
    z=[0]*23
    
    tap_round_x=[13,16,17,18]
    tap_round_y=[20,21]
    tap_round_z=[7,20,21,22]
    
    key_bits=[int(bit) for bit in key]
    for tushig in key_bits:
        x=clock_register(x,[])
        y=clock_register(y,[])
        z=clock_register(z,[])
        
        x[0]^=tushig
        y[0]^=tushig
        z[0]^=tushig
        
    frame_bits=[int(bit) for bit in frame]
    for tushig in frame_bits:
        x=clock_register(x,[])
        y=clock_register(y,[])
        z=clock_register(z,[])

        x[0]^=tushig
        y[0]^=tushig
        z[0]^=tushig
        
    for _ in range(100):
        m=majority(x[8],y[10],z[10])
        if x[8]==m:
            x=clock_register(x,tap_round_x)
        if y[10]==m:
            y=clock_register(y,tap_round_y)
        if z[10]==m:
            z=clock_register(z,tap_round_z)
            
    keystream=[]
    for _ in range(n_bits):
        m=majority(x[8],y[10],z[10])
        if x[8]==m:
            x=clock_register(x,tap_round_x)
        if y[10]==m:
            y=clock_register(y,tap_round_y)
        if z[10]==m:
            z=clock_register(z,tap_round_z)
        keystream_bit=x[-1]^y[-1]^z[-1]
        keystream.append(keystream_bit)
        
    return keystream

def xor(bits1,bits2):
    return [b1^b2 for b1, b2 in zip(bits1,bits2)]

def text_to_bits(text):
    
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bits_to_text(bits):
    chars=[]
    
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        byte_str = ''.join(str(bit) for bit in byte)
        chars.append(chr(int(byte_str, 2)))
    return ''.join(chars)

plaintext="Hi, my name is Tushig, currently I am studying in Luther College and majoring Computer Science. And I love Information Security"
plaintext_bits = text_to_bits(plaintext)
print("Plaintext bits:", plaintext_bits)

key = "1100101010110010101010110010101011001010101010101010101010101010"  # 64-bit key
frame = "1010101010101010101010"  # 22-bit frame number
ks = tushig_keystream(key,frame,len(plaintext_bits))  # Generate 64 keystream bits using the key and frame.
print("Keystream:", ks)

cipher_bits=xor(plaintext_bits,ks)
ciphertext = bits_to_text(cipher_bits)
print("Ciphertext:", ciphertext)

ciphertext_bits = text_to_bits(ciphertext)
decrypt_bits=xor(ciphertext_bits,ks)
decrypted_text=bits_to_text(decrypt_bits)
print("Decrypted:", decrypted_text)
                
    
