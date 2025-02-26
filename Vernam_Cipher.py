def vernam(text,key,Flag):
    result=""
    if len(key)!=len(text):
        return f"Invalid length"
    for i in range(len(text)):
        character=text[i]
        if Flag:
            result+=chr((ord(character)-97+ord(key[i])-97)%26+97)
        else:
            result+=chr((ord(character)-ord(key[i])+26)%26+97)
    return result

key="miniinerboltushig!"
text="tushigerdenebulgan"
cipher=vernam(text,key,True)
print("Cipher: ",vernam(text,key,True))
print("Plaintext:", vernam(cipher,key,False))