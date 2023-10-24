import xmlrpc.client

# Função para imprimir o tabuleiro
def print_tabuleiro(tab):
    for row in tab:
        for cell in row:
            print(f"[{' ' if cell == 0 else ('x' if cell == 1 else 'o') }]", end='')
        print()

tab1 = [[0] * 6 for _ in range(6)]
tab2 = [[0] * 6 for _ in range(6)]

# Variáveis para controlar a pontuação dos jogadores
pontuacao_jogador1 = 0
pontuacao_jogador2 = 0

with xmlrpc.client.ServerProxy("http://127.0.0.1:8000/") as cli:
    id = cli.logar()

    print("Bem-vindo ao Jogo de Batalha Naval!")
    print(f"Você é o Jogador {id}. Posicione seus 3 barcos.")

    for _ in range(3):
        while True:
            vx, vy = map(int, input("Insira as coordenadas de posicionamento (x y): ").split())
            if 0 <= vx <= 5 and 0 <= vy <= 5:  # Verifique se as coordenadas estão dentro dos limites
                if tab1[vx][vy] == 0:
                    break
                else:
                    print("Você já posicionou um barco nessa posição. Escolha outra.")
            else:
                print("Coordenadas fora dos limites. Escolha valores entre 1 e 6.")
        # Adicione 1 às coordenadas antes de enviá-las para o servidor
        cli.positionar(id, vx, vy)
        # Atualize a matriz tab1 com '1' nas posições dos barcos
        tab1[vx][vy] = 1




    print("Tabuleiro após posicionar os barcos:")
    print_tabuleiro(tab1)

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
