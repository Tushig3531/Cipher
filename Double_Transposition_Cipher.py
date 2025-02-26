def encrypt_cipher(text,key):
    row_key, column_key=key
    n_row=len(row_key)
    n_column=len(column_key)
    total_cell=n_row*n_column
    
    if len(text)<total_cell:
        text=text+"*"*(total_cell-len(text))
    elif len(text)>total_cell:
        text=text[:total_cell]
    matrix=[]
    index=0
    for _ in range(n_row):
        row=[]
        for _ in range(n_column):
            row.append(text[index])
            index=index+1
        matrix.append(row)
    shine_matrix=[]
    for r in row_key:
        new_row=[]
        for c in column_key:
            new_row.append(matrix[r][c])
        shine_matrix.append(new_row)
    ciphertext=""
    for row in shine_matrix:
        for char in row:
            ciphertext+=char
    return ciphertext.upper()

def decrypt_cipher(ciphertext, key):
    row_key, column_key=key
    n_row=len(row_key)
    n_column=len(column_key)
    total_cell=n_row*n_column
    
    if len(ciphertext)<total_cell:
        ciphertext=ciphertext+"*"*(total_cell-len(ciphertext))
    elif len(ciphertext)>total_cell:
        ciphertext=ciphertext[:total_cell]
        
    matrix=[]
    index=0
    for _ in range(n_row):
        row=[]
        for _ in range(n_column):
            row.append(ciphertext[index])
            index=index+1
        matrix.append(row)
        
    inverse_row=[0]*n_row
    for index, row in enumerate(row_key):
        inverse_row[row]=index
    inverse_column=[0]*n_column
    for j_index, column in enumerate(column_key):
        inverse_column[column]=j_index
    
    plaintext_matrix=[]
    for _ in range(n_row):
        plaintext_matrix.append([])
    for row in range(n_row):
        for column in range(n_column):
            plaintext_matrix[row].append(matrix[inverse_row[row]][inverse_column[column]])
    plaintext=""
    for r in plaintext_matrix:
        for character in r:
            plaintext+=character
    return plaintext.lower()
        

text="TushigErdenebulgan"
row_key=[5,3,1,0,2,4]
column_key=[1,0,2]
key=(row_key,column_key)
ciphertext="AGNNEEIHGUTSREDUBL"
print(encrypt_cipher(text,key))
print(decrypt_cipher(ciphertext,key))