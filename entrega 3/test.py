from intencoes import *


TABELA = {
          'socket':[],
          "nome":[],
          "mesa":[],
          'conta_i':[],
          'pedidos':[]
          }

NEWTABLE = {
    
}


def informa_conta_individual(dict):
    AUXTABLE = {}
    
    for i in range(len(dict['nome'])):
        if dict['nome'][i] in AUXTABLE.keys():
            AUXTABLE[dict['nome'][i]].append(dict['pedidos'][i])
        else:
            AUXTABLE[dict['nome'][i]] = [dict['pedidos'][i]]

    for i in AUXTABLE:
        print("| " + i + " |\n")
        total = 0
        for j in AUXTABLE[i]:
            pedido = j
            preco = DICT_PRECOS_EXT[pedido]
            total+=preco
            print(pedido + " => R$ " + str(preco))
        print("Total - R$ " + str(total) + "\n")  
    


def main():
    address = ("1.1.1.1", "20001")
    c = f'{address[0]}:{str(address[1])}'
    message = "mateus"

    TABELA['socket'].append(c)
    TABELA['nome'].append(message)
    TABELA['mesa'].append(2)
    TABELA['conta_i'].append(0)
    TABELA['pedidos'].append("salada caesar")


    address = ("1.17.12.13", "10001")
    c = f'{address[0]}:{str(address[1])}'
    message = "raquel"

    TABELA['socket'].append(c)
    TABELA['nome'].append(message)
    TABELA['mesa'].append(3)
    TABELA['conta_i'].append(0)
    TABELA['pedidos'].append("limonada")


    address = ("1.1.1.1", "20001")
    c = f'{address[0]}:{str(address[1])}'
    message = "mateus"

    TABELA['socket'].append(c)
    TABELA['nome'].append(message)
    TABELA['mesa'].append(2)
    TABELA['conta_i'].append(0)
    TABELA['pedidos'].append("refrigerante")

    print(TABELA)
    print(conta_mesa_alt(TABELA, 2))
    print(conta_mesa_alt(TABELA, 3))
    #index = TABELA['nome'].index("oi")
    #print(index)

    NEWTABLE['nome'] = 2

    NEWTABLE['nome'] = 1;
    NEWTABLE['nome'] += 1;
    NEWTABLE['nome'] += 3;

    print(NEWTABLE)

    informa_conta_individual(TABELA)

if __name__ == '__main__':
    main() 