alphabet="abcdefghijklmnopqrstuvwxyz"
letter_to_index=dict(zip(alphabet,range(len(alphabet))))
index_to_letter=dict(zip(range(len(alphabet)),alphabet))

def encrypt_vigenere(text,key):
    result=""
    split_message=[]
    for i in range(0,len(text),len(key)):
        piece= text[i:i+len(key)]
        split_message.append(piece)
    for each in split_message:
        i=0
        for letter in each:
            number=(letter_to_index[letter]+letter_to_index[key[i]])%len(alphabet)
            result+=index_to_letter[number]
            i+=1
    return result
    
    
def decrypt_vigenere(cipher,key):
    result=""
    split_message=[]
    for i in range(0,len(cipher),len(key)):
        piece= cipher[i:i+len(key)]
        split_message.append(piece)
    for each in split_message:
        i=0
        for letter in each:
            number=(letter_to_index[letter]-letter_to_index[key[i]])%len(alphabet)
            result+=index_to_letter[number]
            i+=1
    return result
    
    
key="tushig"
text="egshighuurhun"
print(encrypt_vigenere(text,key))
cipher=encrypt_vigenere(text,key)
print(decrypt_vigenere(cipher,key))
print("key",key)