# servidor_udp.py

import socket
import random

# A função de conversão é exatamente a mesma da versão TCP.
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
        return (f"R$ {valor_reais:.2f} equivalem a "
                f"{moeda_desejada.upper()} {valor_convertido:.2f}. "
                f"(Cotação: {taxa:.2f})")
    else:
        return f"Erro: Moeda '{moeda_desejada}' não suportada. Tente dolar, euro ou libra."

# --- Configuração do Servidor ---
HOST = '127.0.0.1'  # Endereço IP do servidor (localhost)
PORT = 65433        # Usaremos uma porta diferente para não conflitar com o servidor TCP

# socket.AF_INET especifica que usaremos IPv4
# socket.SOCK_DGRAM especifica que usaremos o protocolo UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Vincula o socket ao endereço e porta especificados
    s.bind((HOST, PORT))
    print(f"Servidor UDP ouvindo em {HOST}:{PORT}")

    # O servidor fica em um loop infinito para processar os datagramas
    while True:
        # Aguarda o recebimento de dados. `recvfrom` é bloqueante.
        # Retorna os dados e o endereço (`addr`) do cliente que os enviou.
        data, addr = s.recvfrom(1024)
        
        # Decodifica os bytes recebidos para string
        mensagem_cliente = data.decode('utf-8')
        print(f"Mensagem recebida de {addr}: {mensagem_cliente}")
        
        try:
            # Espera-se que a mensagem seja no formato "valor,moeda"
            valor_str, moeda = mensagem_cliente.split(',')
            
            # Calcula o resultado da conversão
            resposta = calcular_conversao(valor_str, moeda)
        
        except ValueError:
            resposta = "Erro: Formato da mensagem inválido. Use 'valor,moeda'."

        # Envia a resposta de volta PARA O ENDEREÇO do cliente (`addr`)
        s.sendto(resposta.encode('utf-8'), addr)