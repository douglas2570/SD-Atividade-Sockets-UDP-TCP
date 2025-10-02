# cliente_tcp.py

import socket

# --- Configuração do Cliente ---
HOST = '127.0.0.1'  # O endereço do servidor
PORT = 65432        # A mesma porta usada pelo servidor

# Cria o socket e usa 'with' para garantir que será fechado ao final
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Tenta se conectar ao servidor
    try:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor em {HOST}:{PORT}")
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao servidor. Verifique se ele está em execução.")
        exit()

    # Loop para permitir múltiplas conversões na mesma conexão
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
        
        # Envia a mensagem para o servidor. Primeiro, codifica para bytes.
        s.sendall(mensagem.encode('utf-8'))
        
        # Espera pela resposta do servidor (até 1024 bytes)
        data = s.recv(1024)
        
        # Decodifica a resposta e a exibe
        resposta_servidor = data.decode('utf-8')
        print(f"\nResposta do servidor: {resposta_servidor}\n")
        print("-" * 30)

print("Conexão encerrada.")