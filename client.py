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
    print(f"Você é o Jogador {id}. Posicione seus 3 barcos.")

    for _ in range(3):
        while True:
            print("Insira as coordenadas de posicionamento:")
            print("Formato: <tamanho> <x_inicio> <y_inicio> [x_fim y_fim]")
            print("Exemplo para barco de 1 casa: 1 3 3")
            print("Exemplo para barco de 2 casas: 2 2 2 2 3")
            input_coords = input().split()
            
            if len(input_coords) == 3 or len(input_coords) == 5:
                tamanho, x_inicio, y_inicio = map(int, input_coords[:3])

                
                if 0 <= x_inicio <= 5 and 0 <= y_inicio <= 5 and tab1[x_inicio][y_inicio] == 0:
                    if tamanho == 1:
                        break  # Barco de 1 casa
                    elif tamanho == 2 and len(input_coords) == 5:
                        x_fim, y_fim = map(int, input_coords[3:])
                        
                        if 0 <= x_fim <= 5 and 0 <= y_fim <= 5 and (x_inicio == x_fim and y_inicio == y_fim):
                            print("Coordenadas de finalização inválidas ou barco não está na mesma linha/coluna.")
                        else:
                            break
                    else:
                        print("Tamanho de barco inválido. Use 1 para barco de 1 casa ou 2 para barco de 2 casas.")
                else:
                    print("Coordenadas inválidas ou barco já posicionado nessa posição. Escolha outra.")
            else:
                print("Formato inválido. Use <tamanho> <x_inicio> <y_inicio> [x_fim y_fim].")
        
        cli.positionar(id, x_inicio, y_inicio)
        tab1[x_inicio][y_inicio] = 1
        
        if tamanho == 2:
            cli.positionar(id, x_fim, y_fim)
            tab1[x_fim][y_fim] = 1

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
