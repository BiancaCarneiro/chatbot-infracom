import socket
import time
from checksum import *

serverAddressPort = ("127.0.0.1", 20001)
bufferSize        = 1024

def send_confirmation(UDPClientSocket, ack): # Função para enviar o ACK de confirmação ao servidor
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        packet        = msgFromServer[0].decode()
        ack_r         = packet[0]
        cksum         = packet[1:17]
        server_msg    = packet[17:]
        if verify_check(checksum(server_msg, compl_1=False), cksum) and ack_r == ack:
            break
        
    confirmation = ack + cksum
    UDPClientSocket.sendto(confirmation.encode(), serverAddressPort) 
    return msgFromServer
    
def client():
    name = input("Digite seu nome:\n")

    msgFromClient = "Servidor ligado"
    bytesToSend   = '0' + checksum(name)+name


    # Cria socket UDP no client
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Enviar para o servidor usando o socket UDP criado
    ack = '0'
    UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort)
    while True:
        msgFromServer = send_confirmation(UDPClientSocket, ack)
        # depois que ele confirma o recebimento, ele atualiza o ack local
        if ack == '1':
            ack ='0'
        else:
            ack = '1'
            
        t             = time.localtime()
        packet        = msgFromServer[0].decode()
        msg           = f"{time.strftime('%H:%M', t)} CINtofome: " + packet[17:]
        print(msg)
        msgFromClient = input(f'{time.strftime("%H:%M", t)} {name}: ') # Coloca a data e o nome do cliente
        if not msgFromClient:
            msgFromClient = " "
        bytesToSend   = ack + checksum(msgFromClient)+msgFromClient
        UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort)   
        
if __name__ == '__main__':
    client()