# Funções auxiliares:
def tobits(s): # entrada -> string
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result # saida -> string em bits
 
def bin_add(bin_nums): # entrada -> lista de binários
    n = len(bin_nums)
    sum = 0
    for i in range(0, n):
        sum += int(bin_nums[i], 2)
    string = str(bin(sum)).split('b') # tira o b
    return string[1] # retorna a soma da lista dos binários
        
# Função para verificar o checksum
def verify_check(calculated, recieved): # entrada -> dois números binários
    chunk_size = 16
    for i in range(chunk_size):
        if (calculated[i] == '0' and recieved[i] == '0') or (calculated[i] == '1' and recieved[i] == '1'):
            return False # retorna False se os binários tem valores iguais para um mesmo index i
    return True # retorna True caso contrário

# Função para criar o checksum
def checksum(entry, compl_1=True): # entrada -> mensagem e se o checksum
    chunk_size = 16
    cksum = 0
    data = tobits(entry) # transforma a mensagem em bits
    data_len = len(data)
    
    while (data_len % chunk_size) != 0: # formato a data para todos os chunks ficarem no tamanho certo 
        data_len += 1
        data = [0] + data
    n = int(data_len/chunk_size)
    
    to_sum = []
    for i in range(0, n):
        to_sum.append("".join(str(i) for i in data[i*chunk_size:i*chunk_size+chunk_size])) # divido a data formatada em uma lista de bits
    
    cksum = bin_add(to_sum) # faço a soma bit a bit
    
    while len(cksum) > chunk_size: # vejo se tem carry e trato dele
        aux = len(cksum)-chunk_size
        aux2 = '0'*(chunk_size-aux) + cksum[:aux]
        cksum = bin_add([aux2, cksum[aux:]])
        
    if len(cksum) < chunk_size: # ajeito o tamanho do checksum, se necessário
        aux = chunk_size-len(cksum)
        cksum = '0'*aux + cksum
        
    if compl_1: # essa parte faz o complemento a um se não for especificado na chamada da função que não queremos fazer o complemento a um
        list_cs = []
        list_cs[:0] = cksum
        cksum = list_cs
        for i in range(0, chunk_size):
            if cksum[i] == '0':
                cksum[i] = '1'
            else:
                cksum[i] = '0'
        cksum = "".join(cksum)       
     
    return cksum