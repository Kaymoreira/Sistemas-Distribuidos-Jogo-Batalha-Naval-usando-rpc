from xmlrpc.server import SimpleXMLRPCServer

class Users:
    def __init__(self):
        self.id = 0
        self.login = ""
        self.senha = ""
        self.ponto = 0

users = [Users(), Users()]
ganhador = 0

tab1 = [[0] * 6 for _ in range(6)]
tab2 = [[0] * 6 for _ in range(6)]

def login():
    global ganhador
    if users[0].id == 0:
        users[0].id = 1
        return 1
    else:
        users[1].id = 2
        return 2

def positionar(id, px, py):
    if id == 1:
        tab1[px][py] = 1
    else:
        tab2[px][py] = 1
    return 1

def atacar(id, px, py):
    global ganhador
    if ganhador != 0:
        return str(ganhador)  # Converta para uma string

    if px < 0 or px >= 6 or py < 0 or py >= 6:
        return "0"  # Retorna "0" para indicar que o ataque está fora dos limites

    if id == 1:
        if tab2[px][py] == 1:  # Verifica se há um barco na tabela do Jogador 2
            tab2[px][py] = 2  # Marque a posição como atacada
            users[0].ponto += 1
            if users[0].ponto == 3:  # Defina o número de acertos necessários para ganhar
                ganhador = 1
            return "1"  # Retorne "1" para indicar que o ataque foi bem-sucedido
        else:
            return "0"  # Retorne "0" para indicar que o ataque falhou

    elif id == 2:
        if tab1[px][py] == 1:  # Verifica se há um barco na tabela do Jogador 1
            tab1[px][py] = 2  # Marque a posição como atacada
            users[1].ponto += 1
            if users[1].ponto == 3:  # Defina o número de acertos necessários para ganhar
                ganhador = 2
            return "1"  # Retorne "1" para indicar que o ataque foi bem-sucedido
        else:
            return "0"  # Retorne "0" para indicar que o ataque falhou
 # Retorna "0" para indicar que o ataque falhou



def get_tabuleiro(id):
    return tab1 if id == 1 else tab2

def verificar_ganhador():
    global ganhador
    if ganhador == 1:
        return "Jogador 1 ganhou"
    elif ganhador == 2:
        return "Jogador 2 ganhou"
    return "-"


with SimpleXMLRPCServer(('127.0.0.1', 8000)) as server:
    server.register_function(login, "logar")
    server.register_function(positionar, "positionar")
    server.register_function(atacar, "atacar")
    server.register_function(get_tabuleiro, "get_tabuleiro")
    server.register_function(verificar_ganhador, "ganhador")


    print("Servidor da Batalha Naval em execução.")
    print("Aguardando conexões de jogadores...")

    server.serve_forever()
