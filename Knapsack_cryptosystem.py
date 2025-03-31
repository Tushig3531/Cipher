import random
from math import gcd

LARGE_N = 100



def generate_sik(size: int) -> tuple[int, ...]:
    sik=[]
    total=0
    
    for _ in range(size):
        val=random.randint(total+1,total+10)
        sik.append(val)
        total+=val
    return tuple(sik)




def calculate_n(sik: tuple) -> int:
    return sum(sik)+1




def calculate_m(n: int) -> int:
    for x in range(n-1,0,-1):
        if gcd(x,n)==1:
            return x
    raise ValueError("No coprime found")





def calculate_inverse(sik: tuple[int, ...], n: int = 0, m: int = 0) -> int:
    if n==0:
        n=calculate_n(sik)
    if m==0:
        m=calculate_m(n)
    def egcd(a,b):
        if a==0:
            return b,0,1
        g,x,y=egcd(b%a,a)
        return g,y-(b//a)*x,x
    g,x,_=egcd(m,n)
    if g!=1:
        raise ValueError("m and n are not coprime")
    return x%n  





def generate_gk(sik: tuple[int, ...], n: int = 0, m: int = 0) -> tuple[int, ...]:
    if n==0:
        n=calculate_n(sik)
    if m==0:
        m=calculate_m(n)
    return tuple((a*m)%n for a in sik)





def encrypt(plaintext: str, gk: tuple[int, ...]) -> int:
    int_val=0
    for c in plaintext:
        int_val=(int_val<<8)+ord(c)

    if int_val.bit_length()>len(gk):
        raise ValueError("Plaintext is longer than the knapsack capacity")

    bits = bin(int_val)[2:].zfill(len(gk))
    c = 0
    for i, bitchar in enumerate(bits):
        if bitchar=='1':
            c+=gk[i]
    return c
    
    


def decrypt(ciphertext: int, sik: tuple[int, ...], n: int = 0, m: int = 0) -> str:

    if n==0:
        n=calculate_n(sik)
    if m==0:
        m=calculate_m(n)

    inv_m=calculate_inverse(sik,n,m)
    c_prime=(ciphertext*inv_m)%n

    bits_reversed=[]
    remainder=c_prime
    for weight in reversed(sik):
        if weight<=remainder:
            bits_reversed.append('1')
            remainder-=weight
        else:
            bits_reversed.append('0')
    bits_reversed.reverse()

    # converting bits to integer
    bitstring = "".join(bits_reversed)
    dec_val = int(bitstring, 2)

    #converting integer to bytes
    recovered_bytes=[]
    while dec_val > 0:
        recovered_bytes.append(dec_val & 0xFF)
        dec_val >>= 8
    recovered_bytes.reverse()

    if not recovered_bytes:
        return ""

    plaintext = "".join(chr(b) for b in recovered_bytes)
    return plaintext.lstrip("\x00")
    
        


def main():

    size=8

    sik=generate_sik(size)
    print("Superincreasing knapsack (sik):")
    print(sik)

    n=calculate_n(sik)
    print("\nCalculated N:")
    print(n)

    m=calculate_m(n)
    print("\nCalculated M:")
    print(m)

    gk=generate_gk(sik,n,m)
    print("\nGeneral knapsack (gk):")
    print(gk)

    plaintext="10110010"
    print("\nPlaintext (binary):")
    print(plaintext)

    ciphertext=encrypt(plaintext,gk)
    print("\nCiphertext:")
    print(ciphertext)

    decrypted=decrypt(ciphertext,sik,n,m)
    print("\nDecrypted plaintext (binary):")
    print(decrypted)


if __name__ == "__main__":
    main()
