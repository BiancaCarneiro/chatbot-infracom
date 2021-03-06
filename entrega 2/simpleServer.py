import socket
from checksum import *

BUFFERSIZE = 1024
TIMEOUT    = 1e-100
ACKS       = {}

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
    print("Servido ligado e ouvindo")

    # Escutando os dados de entrada
    while(True):
        UDPServerSocket.settimeout(None) # Desliga timeout para escutar clientes
        bytesAddressPair = UDPServerSocket.recvfrom(BUFFERSIZE) # Recebo do cliente
        packet           = bytesAddressPair[0].decode()
        address          = bytesAddressPair[1]
        
        message = packet[17:]
        cksum   = packet[1:17]
        ack     = packet[0]
        print(address, message)
        
        client_key = f'{address[0]}:{str(address[1])}'
        if client_key not in ACKS.keys():
            ACKS[client_key] = '0'        
           
        if verify_check(checksum(message, compl_1=False), cksum) and ack == ACKS[client_key]: # Não está corrompido segundo o checksum e o ACK está certo
            send_data(UDPServerSocket, ACKS[client_key]+cksum+message, address)
            
        # Atualiza ACKS do servidor
        if ACKS[client_key] == '1':
            ACKS[client_key] ='0'
        else:
            ACKS[client_key] = '1'
        
if __name__=='__main__':
    server()