
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
        
def verify_check(calculated, recieved):
    chunk_size = 16
    for i in range(chunk_size):
        if (calculated[i] == '0' and recieved[i] == '0') or (calculated[i] == '1' and recieved[i] == '1'):
            return False
    return True

def checksum(entry, compl_1=True):
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
        #print(type(data[i*chunk_size:i*chunk_size+chunk_size]))
        #to_sum.append(data[i*chunk_size:i*chunk_size+chunk_size])
        to_sum.append("".join(str(i) for i in data[i*chunk_size:i*chunk_size+chunk_size]))
    
    #print('to_sum = ',to_sum)
    cksum = bin_add(to_sum)  
    #print('depois de somar = ', cksum)  
    while len(cksum) > chunk_size:
        aux = len(cksum)-chunk_size
        aux2 = '0'*(chunk_size-aux) + cksum[:aux]
        cksum = bin_add([aux2, cksum[aux:]])
        
    if len(cksum) < chunk_size:
        aux = chunk_size-len(cksum)
        cksum = '0'*aux + cksum
        
    #print(cksum)
    #print(len(cksum))
    if compl_1:
        list_cs = []
        list_cs[:0] = cksum
        cksum = list_cs
        for i in range(0, chunk_size):
            if cksum[i] == '0':
                cksum[i] = '1'
            else:
                cksum[i] = '0'
        cksum = "".join(cksum)       
    #print('final = ', cksum)
    #print('int = ', int(cksum, 2))
     
    return cksum