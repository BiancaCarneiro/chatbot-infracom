from socket import *

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def bin_add(bin_nums):
    chunk_size = len(bin_nums[0])
    n = len(bin_nums)
    sum = 0
    for i in range(0, n):
        sum += int(bin_nums[i], 2)
    string = str(bin(sum)).split('b')
    return string[1]
        
def checksum(entry):
    chunk_size = 16
    cksum = 0
    data = tobits(entry)
    data_len = len(data)
    # print(data_len)
    # print(data)
    
    while (data_len % chunk_size) != 0:
        data_len += 1
        data = [0] + data
    
    # print(data_len)
    # print(data)
    n = int(data_len/chunk_size)
    
    to_sum = []
    
    for i in range(0, n):
        print(type(data[i*chunk_size:i*chunk_size+chunk_size]))
        #to_sum.append(data[i*chunk_size:i*chunk_size+chunk_size])
        to_sum.append("".join(str(i) for i in data[i*chunk_size:i*chunk_size+chunk_size]))
    
    print('to_sum = ',to_sum)
    cksum = bin_add(to_sum)  
    print('depois de somar = ', cksum)  
    while len(cksum) > chunk_size:
        aux = len(cksum)-chunk_size
        aux2 = '0'*(chunk_size-aux) + cksum[:aux]
        cksum = bin_add([aux2, cksum[aux:]])
        
    if len(cksum) < chunk_size:
        aux = chunk_size-len(cksum)
        cksum = '0'*aux + cksum
        
    print(cksum)
    print(len(cksum))
    
    list_cs = []
    list_cs[:0] = cksum
    cksum = list_cs
    for i in range(0, chunk_size):
        if cksum[i] == '0':
            cksum[i] = '1'
        else:
            cksum[i] = '0'
    cksum = "".join(cksum)       
    print('final = ', cksum)
    print('int = ', int(cksum, 2))
     
    return cksum
    


def server():
    serverPort = 12000

    serverSocket = socket(AF_INET,SOCK_STREAM)

    serverSocket.bind(("",serverPort))

    serverSocket.listen(1)

    print ("The server is ready to receive")

    while True:

        connectionSocket, addr = serverSocket.accept()

        # sentence = connectionSocket.recv(1024).decode()
        # cksum = connectionSocket.recv(1024).decode()
        packet = connectionSocket.recv(1024).decode()
        cksum = packet[0:16]
        sentence = packet[16:]
        print(cksum)
        print(sentence)

        print(sentence, cksum)
        print(type(cksum))
        if checksum(sentence) == cksum:
            connectionSocket.send('Recebi a mensagem corretamente'.encode())
        else:
            connectionSocket.send('ERRADA'.encode())
        capitalizedSentence = sentence.upper()

        connectionSocket.send(capitalizedSentence.encode())

        connectionSocket.close()
    
if __name__ == '__main__':
    server()