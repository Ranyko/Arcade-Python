from src.regras.connect_4 import Connect4


def iniciar_partida():
    print("\n" + "=" * 30)
    print("        Connect 4        ")
    print("=" * 30)

    nome1 = input("Digite o nome do jogador 1(⭕): ")
    nome2 = input("Digite o nome do jogador 2(🔵): ")

    jogo = Connect4(nome1, nome2)

    while True:
        jogo.tabuleiro.imprimir()
        jogador_atual = jogo.jogador_atual()

        print(f"Vez de {jogador_atual.nome} jogar com '{jogador_atual.simbolo}'")

        try:
            coluna = int(input("Digite a coluna na qual deseja jogar: ")) - 1
        except ValueError:
            print("Digite apenas numeros inteiros!")
            continue

        if jogo.aplicar_jogada(origem=None, destino=(None, coluna)):
            resultado = jogo.verificar_fim_de_jogo()

            if resultado:
                jogo.tabuleiro.imprimir()
                if resultado == "Empate":
                    print("Fim de Jogo! Empate!")
                else:
                    print(f"Fim de jogo! O jogador {resultado.nome} ({resultado.simbolo}) venceu!")
                break
            else:
                jogo.alternar_turno()

        else:
            print("Jogada inválida! Escolha outra casa vazia dentro do limite!")
