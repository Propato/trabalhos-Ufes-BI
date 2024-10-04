import random
import requests

# Abrindo e lendo o arquivo CSV
INVESTIMENTOS_FIXA = []
with open('renda_fixa.txt', 'r', encoding='utf-8') as renda_fixa_arquivo:
    for linha in renda_fixa_arquivo:
        INVESTIMENTOS_FIXA.append(linha.strip())

INVESTIMENTOS_VAR = []

url = "https://brapi.dev/api/quote/list"
response = requests.get(url)
# Verifica se a resposta foi bem-sucedida
if response.status_code == 200:
    data_all = response.json()
    
    if 'stocks' in data_all:
        for data in data_all['stocks']:
            INVESTIMENTOS_VAR.append((data['stock'], data['type']))
else:
    print(f"Erro na requisição. Status code: {response.status_code}")

CLIENTE_ID = 0
CLIENTES_PERFIS = ['CONSERVADOR', 'MODERADO', 'ARROJADO', 'AGRESSIVO']
# OPS = ['DEPOSITO', 'SAQUE', 'COMPRA', 'VENDA', 'DIVIDENDOS']
PERFIL = {
    # PERFIL: NUMERO DE [DEPOSITO (sem saque), SAQUE (deposito dps saque), COMPRA (sem venda), VENDA (compra dps venda), DIVIDENDO] POR INVESTIMENTO
    'CONSERVADOR': [16, 12, 0, 0, 0],
    'MODERADO': [13, 7, 7, 3, 0],

    'ARROJADO': [7, 3, 13, 7, 1],
    'AGRESSIVO': [0, 0, 16, 12, 2]
}

with open('FILL_CLIENTES.sql', 'w', encoding="utf-8") as arquivo_clientes:
    arquivo_clientes.write("USE CTVM;\n")
    with open('FILL_OPS.sql', 'w', encoding="utf-8") as arquivo_ops:
        arquivo_ops.write("USE CTVM;\n")
        with open('clientes.txt', 'r') as arquivo_nomes:

            for linha in arquivo_nomes:
                linha = linha.strip()
                nomes = linha.split()

                arquivo_clientes.write("\n")

                for nome in nomes:
                    arquivo_ops.write("\n")

                    CLIENTE_ID += 1
                    perfil = random.choice(CLIENTES_PERFIS)
                    arquivo_clientes.write(f"INSERT INTO CLIENTES(CPF, NOME, PERFIL) VALUES ('{CLIENTE_ID*12345}', '{nome}', '{perfil}');\n")

                    for op in range(0, PERFIL[perfil][0]): # DEPOSITOS SEM SAQUES
                        VALOR = round(random.uniform(10, 100), 2)
                        INV = random.choice(INVESTIMENTOS_FIXA)

                        DATA_DIA = random.randint(1, 28)
                        DATA_MES = random.randint(1, 12)
                        DATA_ANO  = 2021 + random.randint(1, 3)

                        arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 1, {VALOR}, {VALOR}, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")
                    
                    for op in range(0, PERFIL[perfil][1]): # DEPOSITOS COM SAQUES
                        VALOR = round(random.uniform(10, 100), 2)
                        VALOR_INICIAL = VALOR
                        INV = random.choice(INVESTIMENTOS_FIXA)

                        DATA_DIA = random.randint(1, 28)
                        DATA_MES = random.randint(1, 11)
                        DATA_ANO  = 2021 + random.randint(1, 3)

                        arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 1, {VALOR}, {VALOR_INICIAL}, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")
                        
                        VALOR = round(VALOR * random.uniform(1.1, 1.5), 2)
                        DATA_MES += 1
                        arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 2, {VALOR}, {VALOR_INICIAL}, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")
                    
                    for op in range(0, PERFIL[perfil][2]): # COMPRA SEM VENDA
                        VALOR = round(random.uniform(10, 100), 2)
                        INV = random.choice(INVESTIMENTOS_VAR)[0]

                        DATA_DIA = random.randint(1, 28)
                        DATA_MES = random.randint(1, 12)
                        DATA_ANO  = 2021 + random.randint(1, 3)

                        arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 3, {VALOR}, {VALOR}, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")

                        if op == 0:
                            for rend in range(0, PERFIL[perfil][4]): # RENDIMENTOS
                                VALOR = round(random.uniform(100, 150), 2)
                                DATA_ANO += 1
                                arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 5, {VALOR}, 0, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")
                    
                    for op in range(0, PERFIL[perfil][3]): # COMPRA COM VENDA
                        VALOR = round(random.uniform(10, 100), 2)
                        INV = random.choice(INVESTIMENTOS_VAR)[0]
                        VALOR_INICIAL = VALOR

                        DATA_DIA = random.randint(1, 28)
                        DATA_MES = random.randint(1, 11)
                        DATA_ANO  = 2021 + random.randint(1, 3)

                        arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 3, {VALOR}, {VALOR_INICIAL}, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")
                        
                        VALOR = round(VALOR * random.uniform(1.1, 1.5), 2)
                        DATA_MES += 1
                        arquivo_ops.write(f"INSERT INTO OPERACOES(COD_INV, CLIENTE_ID, OP, VALOR, VALOR_INICIAL, DATA_OP) VALUES ('{INV}', {CLIENTE_ID}, 4, {VALOR}, {VALOR_INICIAL}, '{DATA_ANO}-{DATA_MES}-{DATA_DIA}');\n")

print("Fim!!!\n")