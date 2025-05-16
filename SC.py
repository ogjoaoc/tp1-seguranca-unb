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

def get_xor(a, b):
    result = ""
    for i in range(len(a)):
        result += str(int(a[i]) ^ int(b[i]))
    return result

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

def rodada_feistel(L, R, K, round):
    EP = [4,  1,  2,  3,  2,  3,  4,  1]
    extend_R = ""
    for i in EP:
        extend_R += R[i-1]

    # XOR com a subchave K
    xored = get_xor(extend_R, K)
    
    # Passa pelas S-Boxes e aplica P4
    s0s1 = s_boxes(xored[:4], xored[4:])
    perm_s0s1 = perm4(s0s1)

    # XOR do resultado com L
    new_L = ""
    for i in range(4):
        a = int(L[i])
        b = int(perm_s0s1[i])
        c = a ^ b
        new_L += str(c)

    # Troca as metades apenas se for a 1ª rodada
    if round == 1:
        L, R = R , new_L
    else:
        L = new_L # Na 2ª rodada, mantém as metades (sem troca)
    
    return L+R

def sdes_encrypt(bloco_de_dados, chave):
    # Gerar as subchaves
    K1, K2 = generate_keys(chave)

    # Aplica o IP
    bits = ip(bloco_de_dados)

    # Realiza as Rodadas de Feistel
    bits = rodada_feistel(bits[:4], bits[4:], K1, 1)
    bits = rodada_feistel(bits[:4], bits[4:], K2, 2)

    # Aplica o IP inverso
    cypher_text = ip_inverse(bits)

    return cypher_text

def sdes_decrypt(bloco_de_dados_cifrado, chave):
    # Gerar as subchaves
    K2, K1 = generate_keys(chave)

    # Aplica o IP
    bits = ip(bloco_de_dados_cifrado)

    # Realiza as Rodadas de Feistel
    bits = rodada_feistel(bits[:4], bits[4:], K1, 1)
    bits = rodada_feistel(bits[:4], bits[4:], K2, 2)

    # Aplica o IP inverso
    decypher_text = ip_inverse(bits)

    return decypher_text

def ecb_encrypt(mensagem, chave):
    blocks = mensagem.split()
    cypher_blocks = []

    for bits in blocks:
        cypher_blocks.append(sdes_encrypt(bits, chave))

    result = " ".join(cypher_blocks)
    return result

def cbc_encrypt(mensagem, chave, vi):
    blocks = mensagem.split()
    cypher_blocks = []
    for bits in blocks:
        xored = get_xor(bits, vi)
        vi = sdes_encrypt(xored,chave)
        cypher_blocks.append(vi)
    
    result = " ".join(cypher_blocks)
    return result

bloco_de_dados = "11010111"
chave = "1010000010"
mensagem = "11010111 01101100 10111010 11110000"
vetor_inicialização = "01010101"

print("Parte 1 --------------")
print(f"Bloco de dados = {bloco_de_dados}\nChave = {chave}")

cypher_text = sdes_encrypt(bloco_de_dados, chave)
print(f"Bloco de dados cifrado = {cypher_text}")

decypher_text = sdes_decrypt(cypher_text, chave)
print(f"Bloco de dados decifrado = {decypher_text}")

print("\nParte 2 --------------")
print(f"Mensagem = {mensagem}")

cypher_mensage = ecb_encrypt(mensagem, chave)
print(f"Mensagem cifrada por ECB = {cypher_mensage}")