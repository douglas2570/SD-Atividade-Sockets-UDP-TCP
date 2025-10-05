# servidor_tcp.py

import socket
import random

def calcular_conversao(valor_reais_str, moeda_desejada):
    try:
        valor_reais = float(valor_reais_str)
    except ValueError:
        return "Erro: O valor informado não é um número válido."

    moeda_desejada = moeda_desejada.strip().lower()

    taxas = {
        'dolar': random.uniform(4.8, 5.2),
        'euro': random.uniform(5.2, 5.6),
        'libra': random.uniform(6.0, 6.5)
    }

    if moeda_desejada in taxas:
        taxa = taxas[moeda_desejada]
        valor_convertido = valor_reais / taxa
        return (f"R$ {valor_reais:.2f} equivalem a "
                f"{moeda_desejada.upper()} {valor_convertido:.2f}. "
                f"(Cotação: {taxa:.2f})")
    else:
        return f"Erro: Moeda '{moeda_desejada}' não suportada. Tente dolar, euro ou libra."

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    
    s.listen()
    print(f"Servidor TCP ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                mensagem_cliente = data.decode('utf-8')
                print(f"Cliente enviou: {mensagem_cliente}")

                try:
                    valor_str, moeda = mensagem_cliente.split(',')
                    
                    resposta = calcular_conversao(valor_str, moeda)
                
                except ValueError:
                    resposta = "Erro: Formato da mensagem inválido. Use 'valor,moeda'."

                conn.sendall(resposta.encode('utf-8'))
            
            print(f"Conexão com {addr} foi fechada.")