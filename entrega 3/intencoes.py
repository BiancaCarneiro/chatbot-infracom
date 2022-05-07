# Lista de intenções do chatbot

LISTA_OPCOES = "Digite uma das opcoes a seguir (o numero ou por extenso)\n1 - cardapio\n2 - pedido\n3 - conta individual\n4 - nao fecho com robo, chame seu gerente\n5 - nada nao, tava so testando\n6 - conta da mesa"
                
CARDAPIO = f"{'-'*25}\nPRATOS PRINCIPAIS (individuais)\n{'-'*25}\n1 - Frango a Parmegiana => R$20,00\n2 - Salada Caesar => R$17,00\n3 - Strogonoff de Frango => R$19,00\n\n{'-'*25}\nSOBREMESAS\n{'-'*25}\n4 - Torta de Limao => R$5,00\n5 - Brigadeiro => R$0,50\n\n{'-'*25}\nBEBIDAS\n6 - Limonada => R$4,00\n7 - Refrigerante => R$5,00\n{'-'*25}\n\n{LISTA_OPCOES}"                

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

# Alternativa para conta_mesa
# Busca pedidos feitos na mesa, e retorna o resultado
def conta_mesa_alt(dict, mesa):
    conta = 0
    for i in range(len(dict['mesa'])):
        if dict['mesa'][i] == mesa:
            for item in dict['pedidos'][i]:
                pedido = list(item.keys())[0]
                conta += DICT_PRECOS_EXT[pedido]
    return conta


# Faz uma busca, e imprime no terminal a relação de clientes, o que cada um consumiu, e quanto ele consumiu
def informa_conta_individual(dict):
    AUXTABLE = {}
    output = ""
    for i in range(len(dict['nome'])):
        if dict['nome'][i] in AUXTABLE.keys():
            #AUXTABLE[dict['nome'][i]].append(dict['pedidos'][i])
            AUXTABLE[dict['nome'][i]] += dict['pedidos'][i]
        else:
            AUXTABLE[dict['nome'][i]] = dict['pedidos'][i]

    print(AUXTABLE)
    for i in AUXTABLE:
        #print("| " + i + " |\n")
        output += "| " + i + " |\n"
        total = 0
        for j in AUXTABLE[i]:
            pedido = list(j.keys())[0]
            preco = DICT_PRECOS_EXT[pedido]
            total+=preco
            #print(pedido + " => R$ " + str(preco))
            output += pedido + " => R$ " + str(preco) + '\n'
        #print("Total - R$ " + str(total) + "\n")
        output += "Total - R$ " + str(total) + "\n"
    
    return output

def conta_ip(dict, id):
    conta = 0

    for i in range(len(dict['socket'])):
        if dict['socket'][i] == id:
            for item in dict['pedidos'][i]:
                pedido = list(item.keys())[0]
                conta+=DICT_PRECOS_EXT[pedido]

    return conta

def trata_pedido(msg):
    if msg.isdigit():
        pedido = int(msg)
        if pedido < 8:
            return pedido
        return 0
    
    keys = list(DICT_PRECOS_EXT.keys())
    for i in range(len(keys)):
        if keys[i].lower() in msg.lower() or msg.lower() in keys[i].lower():
            return i+1
    
    return 0

def trata_pedir(msg):
    if msg.isdigit():
        return int(msg)
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
            return 4
        elif palavra.lower() in ['nada', 'teste', 'testando']:
            return 5
    
    if pedir > 0:
        if cardapio > 0:
            return 1
        elif conta > 0 :
            if individual > 0:
                return 3
            else:
                return 6
        else:
            return 2 # pedido
    elif cardapio > 0:
            return 1
    elif conta > 0 :
        if individual > 0:
            return 3
        else:
            return 6
    return 1