import xmlrpc.client

# Função para imprimir o tabuleiro
def print_tabuleiro(tab):
    for row in tab:
        for cell in row:
            print(f"[{' ' if cell == 0 else ('1' if tamanho == 1 else ('2' if tamanho == 2 else 'o')) }]", end='')
        print()
        



tab1 = [[0] * 6 for _ in range(6)]
tab2 = [[0] * 6 for _ in range(6)]

# Variáveis para controlar a pontuação dos jogadores
pontuacao_jogador1 = 0
pontuacao_jogador2 = 0

with xmlrpc.client.ServerProxy("http://127.0.0.1:8000/") as cli:
    id = cli.logar()

    print("Bem-vindo ao Jogo de Batalha Naval!")
    print(f"Você é o Jogador {id}. Posicione seus 4 barcos (1, 2, 3 e 4 casas).")

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

while True:
    gg = cli.ganhador()
    if gg != "-":
        break

    # Imprima a pontuação dos jogadores a cada atualização
    print(f"Pontuação - Jogador 1: {pontuacao_jogador1}, Jogador 2: {pontuacao_jogador2}")

    # Verifique de quem é o turno
    if id == 1 and gg == "-":
        jogador = "Jogador 1"
    elif id == 2 and gg == "-":
        jogador = "Jogador 2"
    else:
        jogador = "Jogador desconhecido"

    if gg == "-":
        ataque_p = input(f"{jogador}, insira as coordenadas de ataque (x y): ").split()
        if len(ataque_p) == 2 and all(coord.isdigit() for coord in ataque_p):
            ataque_p = list(map(int, ataque_p))
            if 0 <= ataque_p[0] <= 5 and 0 <= ataque_p[1] <= 5:
                atk = cli.atacar(id, ataque_p[0], ataque_p[1])
                print("Valor retornado da função atacar:", atk)
                if int(atk) == 1:
                    if jogador == "Jogador 1":
                        pontuacao_jogador1 += 1
                        print("Você acertou um barco inimigo!")
                        tab2[ataque_p[0] - 1][ataque_p[1] - 1] = 'x'
                    else:
                        pontuacao_jogador2 += 1
                        print("Você acertou um barco inimigo!")
                        tab1[ataque_p[0] - 1][ataque_p[1] - 1] = 'x'
                elif int(atk) == 2:
                    print("Você acertou uma posição já atacada.")
                else:
                    print("Seu ataque errou!")
            else:
                print("Coordenadas de ataque fora dos limites. Escolha valores entre 1 e 6.")
        else:
            print("Coordenadas de ataque inválidas. Insira duas coordenadas separadas por espaço.")

print(gg)
