import xmlrpc.client # Importa a biblioteca XML-RPC para comunicação com o servidor.

# Função para imprimir o tabuleiro
def print_tabuleiro(tab):
    for row in tab:
        for cell in row:
            if cell == 0:
                print("[ ]", end='')
            elif cell == 1:
                print("[x]", end='')  # Se o valor for 1, imprime 'x'
            elif cell == 2:
                print("[x]", end='')  # Se o valor for 2, também imprime 'x'
            else:
                print("[o]", end='')  # Caso contrário, imprime 'o'
        print()
        


# Cria dois tabuleiros 6x6 para representar os tabuleiros dos jogadores.
tab1 = [[0] * 6 for _ in range(6)]
tab2 = [[0] * 6 for _ in range(6)]

# Variavel para controlar a pontuação dos jogadores
pontuacao = 0

# Cria uma conexão com o servidor usando a URL "http://127.0.0.1:8000/" e obtém um ID de jogador chamando a função logar no servidor.
with xmlrpc.client.ServerProxy("http://127.0.0.1:8000/") as cli:
    id = cli.logar()
    
    # Pergunte ao jogador se ele quer jogar primeiro
    escolha_primeiro = input("Você quer jogar primeiro? (sim/não): ").lower()

    if escolha_primeiro == "sim":
        jogador_primeiro = id
        jogador_ativo = id
        print("Você jogará primeiro.\n")
    else:
        # O outro jogador jogará primeiro
        jogador_primeiro = 3 - id  # Alternar entre 1 e 2
        print(f"O Jogador {jogador_primeiro} jogará primeiro.\n")

    # Exibe uma mensagem de boas-vindas e informa ao jogador seu ID.
    print("Bem-vindo ao Jogo de Batalha Naval!")
    print(f"Você é o Jogador {id}. Posicione seus 4 barcos (1, 2, 3 e 4 casas).")

    # Loop para permitir que o jogador posicione barcos no tabuleiro.
    for tamanho in range(1, 5):
        while True:
            print(f"Insira as coordenadas de posicionamento para um barco de {tamanho} casa(s):")
            print("Formato: <x_inicio> <y_inicio> [x_fim y_fim ...]")
            input_coords = input().split()

            if len(input_coords) >= 2:
                coordinates = list(map(int, input_coords))

                if len(coordinates) == tamanho * 2:
                    valid_coordinates = True
                    for i in range(0, len(coordinates), 2):
                        x, y = coordinates[i], coordinates[i + 1]
                        if not (0 <= x <= 5 and 0 <= y <= 5 and tab1[x][y] == 0):
                            valid_coordinates = False
                            break

                    if valid_coordinates:
                        break
                    else:
                        print("Coordenadas inválidas ou barco já posicionado em alguma posição. Escolha outras.")
                else:
                    print(f"Insira exatamente {tamanho * 2} coordenadas para um barco de {tamanho} casas.")
            else:
                print("Formato inválido. Use <x_inicio> <y_inicio> [x_fim y_fim ...].")

        # Atualize o tabuleiro para todas as casas ocupadas pelo barco com o valor 1
        for i in range(0, len(coordinates), 2):
            x, y = coordinates[i], coordinates[i + 1]
            if id == 1:
                tab1[x][y] = 1
            elif id == 2:
                tab2[x][y] = 1


    print("Tabuleiro após posicionar os barcos:")
    if id == 1:
        print_tabuleiro(tab1)
    elif id == 2:
        print_tabuleiro(tab2)
    else:
        print("ID de jogador inválido.")

def enviar_tabuleiros(id, tab1, tab2):
    cli.send_tabuleiros(id, tab1, tab2)

# Após atualizar os tabuleiros no cliente
# tab1 e tab2 são as listas atualizadas no cliente
enviar_tabuleiros(id, tab1, tab2)

# Variável para controlar o jogador atual
jogador = "Jogador 1" if id == 1 else "Jogador 2"

# Entra em um loop principal que executa o jogo enquanto não houver um ganhador.
while True:
    # Obtém o estado atual do jogo (se há um ganhador).
    gg = cli.ganhador()
    if gg != "-":
        break

    # Recupere as pontuações dos jogadores
    pontuacao_jogador1 = cli.pontuacao_jogador1()
    pontuacao_jogador2 = cli.pontuacao_jogador2()

    # Imprima a pontuação dos jogadores a cada atualização
    print(f"\nPontuação - Jogador 1: {pontuacao_jogador1}, Jogador 2: {pontuacao_jogador2}")

    if gg == "-":
        ataque_p = input(f"{jogador}, insira as coordenadas de ataque (x y): ").split()
        if len(ataque_p) == 2 and all(coord.isdigit() for coord in ataque_p):
            ataque_p = list(map(int, ataque_p))
            if 0 <= ataque_p[0] <= 5 and 0 <= ataque_p[1] <= 5:
                atk = cli.atacar(id, ataque_p[0], ataque_p[1])

                if int(atk) == 1:
                    pontuacao += 1
                    print("\nVocê acertou um barco inimigo!")
                    if jogador == "Jogador 1":
                        tab2[ataque_p[0] - 1][ataque_p[1] - 1] = 'x'
                    else:
                        tab1[ataque_p[0] - 1][ataque_p[1] - 1] = 'x'
                elif int(atk) == 2:
                    print("\nVocê acertou uma posição já atacada.")
                else:
                    print("\nSeu ataque errou!")
            else:
                print("\nCoordenadas de ataque fora dos limites. Escolha valores entre 1 e 6.")
        else:
            print("\nCoordenadas de ataque inválidas. Insira duas coordenadas separadas por espaço.")

print(gg)