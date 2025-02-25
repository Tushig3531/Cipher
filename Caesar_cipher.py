def Cipher(utga,key):
    result=[]
    possible_value="abcdefghijklmnopqrstuvwxyz"
    for i in utga:
        if i.lower() in possible_value:
            bair=possible_value.index(i.lower())
            hudulsun_bair=(bair+key)%26
            if i.isupper():
                result.append(possible_value[hudulsun_bair].upper())
            else:
                result.append(possible_value[hudulsun_bair].upper())
        else:
            result.append(i)
            
    return "".join(result)                
    
    
    
    
utga="Tushig"
key=4
encrypt=Cipher(utga,key)
decrypt=Cipher(encrypt,-key)
print(f"Plaintext: {utga}")
print(f"Encrypted: {encrypt}")
print(f"Decrypted: {decrypt.lower()}")