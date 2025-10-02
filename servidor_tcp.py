# servidor_tcp.py

import socket
import random

# Função que simula a conversão de moeda
def calcular_conversao(valor_reais_str, moeda_desejada):
    """
    Realiza a conversão de BRL para a moeda desejada.
    Usa taxas de câmbio aleatórias para simulação.
    """
    try:
        valor_reais = float(valor_reais_str)
    except ValueError:
        return "Erro: O valor informado não é um número válido."

    moeda_desejada = moeda_desejada.strip().lower()

    # Taxas de câmbio aleatórias para simulação
    taxas = {
        'dolar': random.uniform(4.8, 5.2),
        'euro': random.uniform(5.2, 5.6),
        'libra': random.uniform(6.0, 6.5)
    }

    if moeda_desejada in taxas:
        taxa = taxas[moeda_desejada]
        valor_convertido = valor_reais / taxa
        # Formata a resposta
        return (f"R$ {valor_reais:.2f} equivalem a "
                f"{moeda_desejada.upper()} {valor_convertido:.2f}. "
                f"(Cotação: {taxa:.2f})")
    else:
        return f"Erro: Moeda '{moeda_desejada}' não suportada. Tente dolar, euro ou libra."

# --- Configuração do Servidor ---
HOST = '127.0.0.1'  # Endereço IP do servidor (localhost)
PORT = 65432        # Porta que o servidor irá escutar

# socket.AF_INET especifica que usaremos IPv4
# socket.SOCK_STREAM especifica que usaremos o protocolo TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Vincula o socket ao endereço e porta especificados
    s.bind((HOST, PORT))
    
    # Coloca o socket em modo de escuta, aguardando conexões
    s.listen()
    print(f"Servidor TCP ouvindo em {HOST}:{PORT}")

    # O servidor fica em um loop infinito para aceitar múltiplas conexões
    while True:
        # Aceita uma nova conexão. `accept()` é bloqueante.
        # Retorna um novo objeto de socket (`conn`) para a comunicação
        # e o endereço (`addr`) do cliente.
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            
            # Loop para receber dados do cliente
            while True:
                # Recebe até 1024 bytes de dados
                data = conn.recv(1024)
                if not data:
                    # Se não receber dados, o cliente fechou a conexão
                    break
                
                # Decodifica os bytes recebidos para string
                mensagem_cliente = data.decode('utf-8')
                print(f"Cliente enviou: {mensagem_cliente}")

                try:
                    # Espera-se que a mensagem seja no formato "valor,moeda"
                    valor_str, moeda = mensagem_cliente.split(',')
                    
                    # Calcula o resultado da conversão
                    resposta = calcular_conversao(valor_str, moeda)
                
                except ValueError:
                    resposta = "Erro: Formato da mensagem inválido. Use 'valor,moeda'."

                # Envia a resposta de volta para o cliente, codificando para bytes
                conn.sendall(resposta.encode('utf-8'))
            
            print(f"Conexão com {addr} foi fechada.")