import socket
from checksum import *

def client():
    name = input("Digite seu nome:\n")

    msgFromClient = "Servidor ligado"
    bytesToSend   = '0' + checksum(name)+name

    serverAddressPort = ("127.0.0.1", 20001)
    bufferSize        = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Enviar para o servidor usando o socket UDP criado
    ack = '0'
    UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort)
    while msgFromClient != "bye":
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        print(msgFromServer)
        packet = msgFromServer[0].decode()
        msg           = "mensagem do servidor: " + packet
        print(msg)
        print(msgFromServer)
        
        ack_r = packet[0]
        cksum = packet[1:17]
        server_msg = packet[17:]
        
        if verify_check(checksum(server_msg, compl_1=False), cksum):
            if ack == ack_r:
                msgFromClient = input()
                bytesToSend   = ack + checksum(msgFromClient)+msgFromClient
                UDPClientSocket.sendto(bytesToSend.encode(), serverAddressPort)   
                if ack == '1':
                    ack ='0'
                else:
                    ack = '1'
            else:
                print(f"ERROR: acks não batem ----> ack_r={ack_r} e ack={ack}")
        else:
            print("ERROR: está corrompido segundo o checksum")
        
if __name__ == '__main__':
    client()