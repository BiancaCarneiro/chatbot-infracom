# Lista de intenções do chatbot

LISTA_OPCOES = "Digite uma das opcoes a seguir (o numero ou por extenso)\n1 - cardapio\n2 - pedido\n3 - conta individual\n4 - nao fecho com robo, chame seu gerente\n5 - nada nao, tava so testando\n6 - conta da mesa"
                
CARDAPIO = f"{'-'*25}\nPRATOS PRINCIPAIS (individuais)\n{'-'*25}\n1 - Frango a Parmegiana => R$20,00\n2 - Salada Caesar => R$17,00\n3 - Strogonoff de Frango => R$19,00\n\n{'-'*25}\nSOBREMESAS\n{'-'*25}\n4 - Torta de Limao => R$5,00\n5 - Brigadeiro => R$0,50\n\n{'-'*25}\nBEBIDAS\n6 - Limonada => R$4,00\n7 - Refrigerante => R$5,00\n{'-'*25}"                

DICT_PRECOS_EXT = {'frango a parmegiana': 20.0,
               'salada caesar': 17.0,
               'strogonoff de frango': 19.0,
               'torta de limao': 5.0,
               'brigadeiro': .5,
               'limonada': 4.,
               'refrigerante': 5.
}

DICT_PRECOS = {'1': 20.0,
               '2': 17.0,
               '3': 19.0,
               '4': 5.0,
               '5': .5,
               '6': 4.,
               '7': 5.
}


def retorna_preco(string):
    if len(string)>1:
        if string in DICT_PRECOS_EXT:
            return DICT_PRECOS_EXT[string]
    if string in DICT_PRECOS:
        return DICT_PRECOS[string]
    
def conta_mesa(dict, mesa):
    conta = 0
    for i in range(len(dict['mesa'])):
        if dict['mesa'][i] == mesa:
            conta += dict['conta_i'][i]
    return conta

def conta_mesa_alt(dict, mesa):
    conta = 0
    for i in range(len(dict['mesa'])):
        if dict['mesa'][i] == mesa:
            conta += DICT_PRECOS_EXT[dict['pedidos'][i]]
    return conta

'''
def conta_individual(dict, nome):
    
    pedidos = ''
    index = TABELA['nome'].index(nome)
    for i in range(len(dict['nome'])):
        if dict['nome'][i] == nome:
            pedidos += index
            
    return pedidos

'''

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


def retorna_opc_str(opc):
    if opc == 0:
        return CARDAPIO
    if opc == 1:
        return 'Digite qual o primeiro item que gostaria (número ou por extenso)'
    if opc == 4:
        return 'Nao seja mal educado'
    if opc == 5:
        return LISTA_OPCOES

def trata_pedir(msg):

    string = msg.split(" ")
    conta = 0
    pedir = 0
    cardapio = 0
    individual = 0
    
    for palavra in string:
        if palavra.lower() == "pedido":
            pedir += 1
        elif palavra.lower() == "pedir":
            pedir += 1
        elif palavra.lower() == "conta":
            conta += 1
        elif palavra.lower() == 'cardapio':
            cardapio += 1
        elif palavra.lower() == 'individual':
            individual += 1    
        elif palavra.lower() == 'gerente':
            return 3
        elif palavra.lower() in ['nada', 'teste', 'testando']:
            return 4
    
    if conta == 0 and pedir > 0:
        print("o cliente gostaria de fazer um pedido do cardápio")
        return 1
    elif conta == 1:
        print("cliente gostaria de pedir conta")
        if individual > 0:
            return 2
        else:
            return 5
    elif cardapio > 0:
        return 0

