import random
from math import gcd

def generate_superincreasing_sequence(n,start=2,factor=10):
    sequence=[]
    total=0
    for _ in range(n):
        next_val=random.randint(total+1,total+factor)
        sequence.append(next_val)
        total+=next_val
    return sequence

def modular_inverse(a,m):
    def egcd(a,b):
        if a==0:
            return (b,0,1)
        else:
            g,y,x=egcd(b%a,a)
            return (g,x-(b//a)*y,y)
    g,x,_=egcd(a,m)
    if g!=1:
        raise Exception('Modular inverse does not exist')
    return x%m

def generate_key(n):
    private_key=generate_superincreasing_sequence(n)
    total=sum(private_key)
    q=random.randint(total+1,total+100) 
    r=random.randint(2,q-1)
    while gcd(r,q)!=1:
        r=random.randint(2,q-1)
    public_key=[(r*w)%q for w in private_key]
    return public_key,private_key,q,r    

def encrypt(message,public_key):
    if len(message)!=len(public_key):
        raise ValueError("Message length must equal the public key length")
    ciphertext=sum(int(bit)*publickey for bit,publickey in zip(message,public_key))
    return ciphertext

def decrypt(ciphertext,private_key,q,r):
    r_inv=modular_inverse(r,q)
    cipher=(ciphertext*r_inv)%q
    n=len(private_key)
    message=[0]*n
    for i in reversed(range(n)):
        if private_key[i]<=cipher:
            message[i]=1
            cipher-=private_key[i]
    return ''.join(map(str,message))

def main():
    n = 8 
    public_key,private_key,q,r = generate_key(n)
    print("Public Key:",public_key)
    print("Private Key (superincreasing sequence):",private_key)
    print("Modulus q:",q)
    print("Multiplier r:",r)

    message = "10110010"
    print("Original message:", message)

    ciphertext = encrypt(message, public_key)
    print("Ciphertext:", ciphertext)
    
    decrypted_message = decrypt(ciphertext, private_key, q, r)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()
        
