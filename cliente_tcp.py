# cliente_tcp.py

import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor em {HOST}:{PORT}")
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao servidor. Verifique se ele está em execução.")
        exit()

    while True:
        valor = input("Digite o valor em R$ (ou 'sair' para encerrar): ")
        if valor.lower() == 'sair':
            break
        
        moeda = input("Digite a moeda de destino (dolar, euro, libra): ")
        if moeda.lower() == 'sair':
            break

        mensagem = f"{valor},{moeda}"
        
        s.sendall(mensagem.encode('utf-8'))
        
        data = s.recv(1024)
        
        resposta_servidor = data.decode('utf-8')
        print(f"\nResposta do servidor: {resposta_servidor}\n")
        print("-" * 30)

print("Conexão encerrada.")