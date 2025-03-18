def rc4(key,data):
    S=list(range(256)) #initialize the state array S with values from 0 to 255.
    
    j=0 # j will be used for swapping values in S
    
    key_length=len(key) #length of the key to cycle through its bytes
    
    for i in range(256): #loop 256 to scramble S based on the key
        
        j=(j+S[i]+key[i%key_length])%256 #updating j by adding S[i] and the byte of key.
        # and key[i%key_length] cycle through the key.
        S[i],S[j]=S[j],S[i] #swaping the value of j and i
        
    i=0
    j=0
    #initializing i and j to 0 to generate the keystream
    result=bytearray()
    
    for byte in data:
        i=(i+1)%256 #wrapping around using modulo 256 
        j=(j+S[i])%256 #updating j based on the current state value.
        
        S[i],S[j]=S[j],S[i] #swaping the value
        k=S[(S[i]+S[j])%256] #the keystream byte is selected using the new values of S[i] and S[j]
        
        result.append(byte^k) #XORing them
        
    return bytes(result)

plaintext="Hi my name is Tushig Erdenebulgan and I am from Mongolia".encode()
key="This is Tushig is secret".encode()

encrypt=rc4(key,plaintext)
decrypt=rc4(key,encrypt)

print("This is encryption: ", encrypt)
print("This is decryption: ", decrypt)
        
        
        
    