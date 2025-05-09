def perm10(bits):
    P10 = [3,  5,  2,  7,  4,  10,  1,  9,  8,  6]
    result = ""
    for i in P10:
        result += bits[i-1]
    
    return result

def perm8(bits):
    P8 = [6,  3,  7,  4,  8,  5,  10,  9]
    result = ""
    for i in P8:
        result += bits[i-1]

    return result

def perm4(bits):
    P4 = [2,  4,  3,  1]
    result = ""
    for i in P4:
        result += bits[i-1]
    
    return result

def ip(bits):
    IP = [2,  6,  3,  1,  4,  8,  5,  7]
    result = ""
    for i in IP:
        result += bits[i-1]
    
    return result

def ip_inverse(bits):
    IP_R = [4,  1,  3,  5,  7,  2,  8,  6]
    result = ""
    for i in IP_R:
        result += bits[i-1]
    
    return result

def circular_shift(bits):
    left = bits[:5]
    right = bits[5:]

    left = left[1:] + left[0]
    right = right[1:] + right[0]

    return left + right

def generate_keys(chave):
    K = perm10(chave)
    K = circular_shift(K)
    K1 = perm8(K)
    K = circular_shift(circular_shift(K))
    K2 = perm8(K)
    return K1, K2

def s_boxes(l4, r4):
    # S-Box S0
    S0 = [[1, 0, 3, 2],  # linha 0
          [3, 2, 1, 0],  # linha 1
          [0, 2, 1, 3],  # linha 2
          [3, 1, 3, 2]]   # linha 3

    # S-Box S1
    S1 = [[0, 1, 2, 3],  # linha 0
          [2, 0, 1, 3],  # linha 1
          [3, 0, 1, 0],  # linha 2
          [2, 1, 0, 3]]   # linha 3
    
    row_l = int(l4[0] + l4[3], 2)
    col_l = int(l4[1] + l4[2], 2)
    val_l = S0[row_l][col_l]

    row_r = int(r4[0] + r4[3], 2)
    col_r = int(r4[1] + r4[2], 2)
    val_r = S1[row_r][col_r]

    s0_out = format(val_l, '02b')
    s1_out = format(val_r, '02b')

    return s0_out + s1_out

def rodada_feistel():
    pass

def sdes_encrypt():
    pass

def sdes_decrypt():
    pass

def ecb_encrypt():
    pass

def cbc_encrypt():
    pass

bloco_de_dados = "11010111"
chave = "1010000010"