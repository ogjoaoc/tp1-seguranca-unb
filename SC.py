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

def circular_shift():
    pass

def generate_keys():
    pass

def s_boxes():
    pass

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