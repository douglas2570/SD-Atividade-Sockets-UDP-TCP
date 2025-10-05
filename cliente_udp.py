# cliente_udp.py

import socket

HOST = '127.0.0.1'
PORT = 65433
SERVER_ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    
    while True:
        valor = input("Digite o valor em R$ (ou 'sair' para encerrar): ")
        if valor.lower() == 'sair':
            break
        
        moeda = input("Digite a moeda de destino (dolar, euro, libra): ")
        if moeda.lower() == 'sair':
            break

        mensagem = f"{valor},{moeda}"
        
        s.sendto(mensagem.encode('utf-8'), SERVER_ADDRESS)
        
        data, addr = s.recvfrom(1024)
        
        resposta_servidor = data.decode('utf-8')
        print(f"\nResposta do servidor: {resposta_servidor}\n")
        print("-" * 30)

print("Cliente encerrado.")