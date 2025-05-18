import os

# apenas para limpar o menu :D
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def cbc_decrypt(mensagem, chave, vi):
    blocks = mensagem.split()
    plain_blocks = []
    old_vi = vi
    for block in blocks:
        dec_block = sdes_decrypt(block, chave)
        plain = get_xor(dec_block, old_vi)
        plain_blocks.append(plain)
        old_vi = block

    return " ".join(plain_blocks)

def bits_list_to_hex(bits_list):
    ret = ""
    for b in bits_list:
        ret += format(int(b, 2), '02X') + ' '
    return ret

def show_menu():
    print("\n=== Simulador S-DES ===")
    print("1) Criptografar (ECB)")
    print("2) Descriptografar (ECB)")
    print("3) Criptografar (CBC)")
    print("4) Descriptografar (CBC)")
    print("5) Executar testes padrão")
    print("6) Sair")

def main():
    while True:
        show_menu()
        escolha = input("Escolha uma opção: ").strip()
        
        if escolha == '1':
            msg = input("Mensagem (bits separados por espaço): ")
            chave = input("Chave (10 bits): ")
            ct = ecb_encrypt(msg, chave)
            out_bin = ct
            out_hex    = bits_list_to_hex(ct.split())
            print(f"\nECB cifrado — BINÁRIO: {out_bin}")
            print(f"ECB cifrado —   HEXA: {out_hex}")
        
        elif escolha == '2':
            ct = input("Texto cifrado ECB: ")
            chave = input("Chave (10 bits): ")
            pt = ' '.join(sdes_decrypt(b, chave) for b in ct.split())
            out_bin = pt
            out_hex    = bits_list_to_hex(pt.split())
            print(f"\nECB decifrado — BINÁRIO: {out_bin}")
            print(f"ECB decifrado —   HEXA: {out_hex}")
        
        elif escolha == '3':
            msg = input("Mensagem (bits separados por espaço): ")
            chave = input("Chave (10 bits): ")
            vi = input("Vetor de inicialização (8 bits): ")
            ct = cbc_encrypt(msg, chave, vi)
            out_bin = ct
            out_hex    = bits_list_to_hex(ct.split())
            print(f"\nCBC cifrado — BINÁRIO: {out_bin}")
            print(f"CBC cifrado —   HEXA: {out_hex}")
            print(f"VI usado: {vi}")
        
        elif escolha == '4':
            ct = input("Texto cifrado CBC: ")
            chave = input("Chave (10 bits): ")
            vi = input("VI original (8 bits): ")
            pt = cbc_decrypt(ct, chave, vi)
            out_bin = pt
            out_hex    = bits_list_to_hex(pt.split())
            print(f"\nCBC decifrado — BINÁRIO: {out_bin}")
            print(f"CBC decifrado —   HEXA: {out_hex}")
        
        elif escolha == '5':
            run_default_tests()
        
        elif escolha == '6':
            print("\nSaindo...")
            break
        
        else:
            print("\nOpção inválida. Tente novamente.")
        
        input("\nPressione ENTER para continuar...")
        clear()


# testes padrões do trabalho
def run_default_tests():
    bloco_de_dados = "11010111"
    chave           = "1010000010"
    mensagem        = "11010111 01101100 10111010 11110000"
    vetor_inicialização = "01010101"

    print("=== Testes Padrões ===\n")
    print("Parte 1 --------------")
    print(f"Bloco de dados = {bloco_de_dados}\nChave = {chave}")

    cypher_text = sdes_encrypt(bloco_de_dados, chave)
    hex_ct      = bits_list_to_hex(cypher_text.split())
    print(f"Bloco de dados cifrado   — BINÁRIO: {cypher_text} | HEXA: {hex_ct}")

    decypher_text = sdes_decrypt(cypher_text, chave)
    hex_dec       = bits_list_to_hex(decypher_text.split())
    print(f"Bloco de dados decifrado — BINÁRIO: {decypher_text} | HEXA: {hex_dec}")

    print("\nParte 2 --------------")
    print(f"Mensagem = {mensagem}")

    cypher_message = ecb_encrypt(mensagem, chave)
    hex_msg        = bits_list_to_hex(cypher_message.split())
    print(f"Mensagem cifrada por ECB — BINÁRIO: {cypher_message} | HEXA: {hex_msg}")

    cypher_message = cbc_encrypt(mensagem, chave, vetor_inicialização)
    hex_msg        = bits_list_to_hex(cypher_message.split())
    print(f"Mensagem cifrada por CBC — BINÁRIO: {cypher_message} | HEXA: {hex_msg}")


if __name__ == "__main__":
    main()