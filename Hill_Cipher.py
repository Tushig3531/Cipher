def mod_inverse(a,module):
    a=a%module
    for i in range(1,module):
        if (a*i)%module==1:
            return i
    raise ValueError("not inversable")

def get_submatrix(matrix,i,j):
    return [row[:j]+row[j+1:] for index,row in enumerate(matrix) if index!=i]

def determinant(matrix, module):
    n=len(matrix)
    if n==1:
        return matrix[0][0]%module
    if n==2:
        return (matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0])%module
    det=0
    for j in range(n):
        sign=1 if j%2==0 else -1
        sub=get_submatrix(matrix,0,j)
        det+=sign*matrix[0][j]*determinant(sub,module)
        det%=module
    return det%module
def matrix_co_factor(matrix,module):
    n=len(matrix)
    cofactor=[]
    for i in range(n):
        co_factor_row=[]
        for j in range(n):
            sub=get_submatrix(matrix,i,j)
            sign=1 if (i+j)%2==0 else -1
            cof=sign*determinant(sub,module)
            co_factor_row.append(cof%module)
        cofactor.append(co_factor_row)
    return cofactor

def transpose(matrix):
    n=len(matrix)
    return [[matrix[j][i] for j in range(n)] for i in range(n)]

def matrix_mod_inv(matrix,module):
    det=determinant(matrix,module)
    det_inv=mod_inverse(det,module)
    cofactor=matrix_co_factor(matrix,module)
    adjust=transpose(cofactor)
    
    n=len(matrix)
    inv_matrix=[]
    for i in range(n):
        row=[]
        for j in range(n):
            row.append((adjust[i][j]*det_inv)%module)
        inv_matrix.append(row)
    return inv_matrix


def text_to_number(text):
    result = []
    for ch in text.upper():
        if ch.isalpha():
            result.append(ord(ch) - ord("A"))
    return result

def number_to_text(numbers):
    result = ""
    for num in numbers:
        result += chr(num + ord("A"))
    return result

def matrix_vector_mult(matrix, vector, mod):
    result=[]
    for row in matrix:
        total=0
        for a, b in zip(row,vector):
            total+=a*b
        result.append(total%mod)
    return result

def encrypt(plaintext, key_matrix):
    mod=26 
    n = len(key_matrix) 
    nums = text_to_number(plaintext)
    if len(nums)%n!=0:
        padding_length=n-(len(nums)%n)
        nums.extend([0]*padding_length)
    
    ciphertext_numbers=[]
    for i in range(0,len(nums),n):
        block=nums[i:i+n]
        encrypted_block=matrix_vector_mult(key_matrix, block, mod)
        ciphertext_numbers.extend(encrypted_block)
    
    return number_to_text(ciphertext_numbers)

def decrypt(ciphertext, key_matrix):
    """
    Decrypt the ciphertext using the Hill cipher with the given key matrix.
    """
    mod=26
    n=len(key_matrix)
    nums=text_to_number(ciphertext)
    inv_matrix=matrix_mod_inv(key_matrix,mod)
    
    plaintext_numbers=[]
    for i in range(0,len(nums),n):
        block=nums[i:i+n]
        decrypted_block=matrix_vector_mult(inv_matrix,block,mod)
        plaintext_numbers.extend(decrypted_block)
    
    return number_to_text(plaintext_numbers)
        




if __name__ == "__main__":
    key_matrix = [
        [17,17,5,21,3],
        [4,9,15,10,8],
        [12,24,1,8,14]
    ]
    module = 26 
    plaintext="Tushig"
    try:
        inv_matrix = matrix_mod_inv(key_matrix, module)
        print("Original matrix:")
        for row in key_matrix:
            print(row)
        print("Inverse matrix modulo:", module)
        for row in inv_matrix:
            print(row)
    except ValueError as e:
        print("Error:", e)
        
    print("Plaintext: ", plaintext)
    
    ciphertext=encrypt(plaintext, key_matrix)
    print("Ciphertext:", ciphertext)

    decrypted_text=decrypt(ciphertext, key_matrix)
    print("Decrypted: ", decrypted_text)
            
            
            
            
            
            
            
            
