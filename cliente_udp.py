# cliente_udp.py

import socket

# --- Configuração do Cliente ---
HOST = '127.0.0.1'  # O endereço do servidor
PORT = 65433        # A porta do servidor UDP
SERVER_ADDRESS = (HOST, PORT)

# Cria o socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    
    # Loop para permitir múltiplas conversões
    while True:
        # Pede a entrada do usuário
        valor = input("Digite o valor em R$ (ou 'sair' para encerrar): ")
        if valor.lower() == 'sair':
            break
        
        moeda = input("Digite a moeda de destino (dolar, euro, libra): ")
        if moeda.lower() == 'sair':
            break

        # Formata a mensagem para "valor,moeda"
        mensagem = f"{valor},{moeda}"
        
        # Envia a mensagem PARA O ENDEREÇO DO SERVIDOR. Não há conexão prévia.
        s.sendto(mensagem.encode('utf-8'), SERVER_ADDRESS)
        
        # Espera pela resposta do servidor
        # O cliente também usa recvfrom para saber de quem veio a resposta
        data, addr = s.recvfrom(1024)
        
        # Decodifica a resposta e a exibe
        resposta_servidor = data.decode('utf-8')
        print(f"\nResposta do servidor: {resposta_servidor}\n")
        print("-" * 30)

print("Cliente encerrado.")