import socket
from checksum import *

name = input("Digite seu nome:\n")

msgFromClient = "Servidor ligado"
bytesToSend   = checksum(name)+name

serverAddressPort = ("127.0.0.1", 20001)
bufferSize        = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enviar para o servidor usando o socket UDP criado
while msgFromClient != "bye":
    UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort)
    
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg           = "mensagem do servidor: " + msgFromServer[0].decode()
    print(msg)

    msgFromClient = input()
    bytesToSend   = checksum(msgFromClient)+msgFromClient
