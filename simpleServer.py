import socket
import threading
import time
from checksum import *

BUFFERSIZE = 1024


def server():
    localIP    = "127.0.0.1"
    localPort  = 20001

    # Crie um socket de datagrama
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Vincular ao endereço e ip
    UDPServerSocket.bind((localIP, localPort))
    print("Servido ligado e ouvindo")

    acks = {}
    # Escutando os dados de entrada
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(BUFFERSIZE)
        
        packet = bytesAddressPair[0].decode()
        address = bytesAddressPair[1]
        
        message = packet[17:]
        cksum = packet[1:17]
        ack = packet[0]
        print(address, ack, cksum, message)
        
        client_key = f'{address[0]}:{str(address[1])}'
        print(client_key)
        
           
        if verify_check(checksum(message, compl_1=False), cksum): # Não está corrompido segundo o checksum
            if client_key in acks.keys(): # Vejo se temos historico do cliente
                if ack == acks[client_key]: # comparo acks
                    # Sending a reply to client
                    if acks[client_key] == '1':
                        acks[client_key] ='0'
                    else:
                        acks[client_key] = '1'
                    packet = acks[client_key]+cksum+message
                    UDPServerSocket.sendto(packet.encode(), address) # Mando o pacote recebido 
                else:
                    print(f"ERROR: acks não batem ----> ack_r={ack} e ack={acks[client_key]}")
            else:
                # Sending a reply to client
                acks[client_key] = '0'
                if ack == acks[client_key]:
                    packet = acks[client_key]+cksum+message
                    UDPServerSocket.sendto(packet.encode(), address)
        else:
            print("ERROR: está corrompido segundo o checksum")
                
        
if __name__=='__main__':
    server()