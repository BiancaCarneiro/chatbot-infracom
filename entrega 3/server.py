import socket
from intencoes import *
from checksum import *

TABELA = {
          'socket':[],
          "nome":[],
          "mesa":[],
          'pedidos':[]
          }

BUFFERSIZE = 1024
TIMEOUT    = 1e-100
ACKS       = {}
VALOR_PAGO = {}
IS_PEDIDO  = {}
CONF_CONTA = {}
IS_CONTA   = {}
    
def send_data(UDPServerSocket, packet, address): # Função para enviar as informações ao cliente
    sent_cksum = checksum(packet[17:], compl_1=False)
    client_key = f'{address[0]}:{str(address[1])}'
    UDPServerSocket.settimeout(TIMEOUT)
    UDPServerSocket.sendto(packet.encode(), address)
    while True: # checa se recebemos o ack de confirmação
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(BUFFERSIZE)
            pkt              = bytesAddressPair[0].decode()
            cksum            = pkt[1:17]
            ack              = pkt[0]
            if verify_check(sent_cksum, cksum) and ack == ACKS[client_key]:
                break
        except socket.timeout:
            UDPServerSocket.sendto(packet.encode(), address)

def server():
    localIP    = "127.0.0.1"
    localPort  = 20001

    # Crie um socket de datagrama
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Vincular ao endereço e ip
    UDPServerSocket.bind((localIP, localPort))
    print("Servidor ligado e ouvindo")

    # Escutando os dados de entrada
    while(True):
        UDPServerSocket.settimeout(None) # Desliga timeout para escutar clientes
        bytesAddressPair = UDPServerSocket.recvfrom(BUFFERSIZE) # Recebo do cliente
        packet           = bytesAddressPair[0].decode()
        address          = bytesAddressPair[1]
        
        message = packet[17:]
        cksum   = packet[1:17]
        ack     = packet[0]
        
        client_key = f'{address[0]}:{str(address[1])}'
        if verify_check(checksum(message, compl_1=False), cksum): # Não está corrompido segundo o checksum e o ACK está certo
            msg = LISTA_OPCOES
            if client_key not in ACKS.keys():
                ACKS[client_key] = '0'
                IS_PEDIDO[client_key] = False
                TABELA['socket'].append(client_key)
                TABELA['nome'].append(message)
                TABELA['mesa'].append(None)
                TABELA['pedidos'].append(None)
                VALOR_PAGO[client_key] = 0
                msg = 'Digite sua mesa'
                
            index = TABELA['socket'].index(client_key) # pego o index do elemento com a chave do cliente
            if ack == ACKS[client_key]:
                if client_key in CONF_CONTA and CONF_CONTA[client_key]:
                    msg = 'Você pagou sua conta, obrigado!\n' + LISTA_OPCOES
                if client_key in IS_CONTA and IS_CONTA[client_key] and float(message) <= conta_mesa_alt(TABELA, TABELA['mesa'][index]) and float(message) >= conta_ip(TABELA, client_key):
                    VALOR_PAGO[client_key] += float(message)
                    
                if message == 'levantar' or client_key in IS_CONTA and IS_CONTA[client_key]: 
                    IS_CONTA[client_key] = False
                    if VALOR_PAGO[client_key] == conta_ip(TABELA, client_key):
                        msg = "Volte sempre"
                    elif VALOR_PAGO[client_key] == 0:
                        msg = f"Sua conta foi R$ {conta_ip(TABELA, client_key)-VALOR_PAGO[client_key]} e a da mesa R$ {conta_mesa_alt(TABELA, TABELA['mesa'][index])}. Digite o valor a ser pago"
                        IS_CONTA[client_key] = True
                    elif VALOR_PAGO[client_key] > conta_ip(TABELA, client_key) and VALOR_PAGO[client_key] < conta_mesa_alt(TABELA, TABELA['mesa'][index]):
                        msg = f"Voce esta pagando R$ {VALOR_PAGO[client_key]-conta_ip(TABELA, client_key)} a mais que sua conta. O valor excedente sera distribuído para os outros clientes.  Deseja confirmar o pagamento? (digite sim para confirmar)"
                        CONF_CONTA[client_key] = True
                        extra = VALOR_PAGO[client_key]-conta_ip(TABELA, client_key)
                        num_membros = 0
                        for i in range(len(TABELA['mesa'])):
                            if TABELA['mesa'][i] == TABELA['mesa'][index]:
                                num_membros += 1
                        num_membros -= 1
                        if num_membros > 0:
                            for i in range(len(TABELA['mesa'])):
                                if TABELA['mesa'][i] == TABELA['mesa'][index] and i != index:
                                    VALOR_PAGO[TABELA['socket'][i]] += extra/num_membros
                    else:
                        msg = f"Sua conta foi R$ {conta_ip(TABELA, client_key)-VALOR_PAGO[client_key]} e a da mesa R$ {conta_mesa_alt(TABELA, TABELA['mesa'][index])}. Digite o valor a ser pago"
                        IS_CONTA[client_key] = True

                elif IS_PEDIDO[client_key]:
                    opc = trata_pedido(message)
                    if opc == 0:
                        IS_PEDIDO[client_key] = False
                    else:
                        keys = list(DICT_PRECOS_EXT.keys())
                        if not TABELA['pedidos'][index]:
                            TABELA['pedidos'][index] = [{f"{keys[opc-1]}":DICT_PRECOS_EXT[keys[opc-1]]}]
                        else:
                            TABELA['pedidos'][index] += [{f"{keys[opc-1]}":DICT_PRECOS_EXT[keys[opc-1]]}]
                        msg = 'Gostaria de mais algum item? (número ou por extenso)'
                else:
                    if not TABELA['mesa'][index] and len(message) < 2: # vejo se a mesa está preenchida 
                        TABELA['mesa'][index] = message
                    # TRATAR O CASO QUE O CLIENTE ENVIA UM NÚMERO INVÁLIDO DE MESA
                    elif TABELA['mesa'][index]:
                        opc = trata_pedir(message) # retorna a opcao que o cliente escolheu
                        if opc == 1:
                            msg = CARDAPIO
                        if opc == 2:
                            msg = 'Digite qual o primeiro item que gostaria (número ou por extenso)' 
                            IS_PEDIDO[client_key] = True       
                        if opc == 3:
                            conta = informa_conta_individual(TABELA)
                            msg = str(conta)
                        if opc == 4:
                            msg = 'Nao seja mal educado'
                        if opc == 5:
                            msg = LISTA_OPCOES
                        if opc == 6:
                            conta = conta_mesa_alt(TABELA, TABELA['mesa'][index])
                            msg = str(conta)
                print(TABELA)
                packet = ACKS[client_key] + checksum(msg) + str(msg)
                send_data(UDPServerSocket, packet, address)
                # Atualiza ACKS do servidor
                
                if ACKS[client_key] == '1':
                    ACKS[client_key] ='0'
                else:
                    ACKS[client_key] = '1'
        
if __name__=='__main__':
    server()