from src.regras.jogo_da_velha import JogoDaVelha


def iniciar_partida():
    print("\n" + "=" * 30)
    print("         JOGO DA VELHA        ")
    print("=" * 30)

    nome1 = input("Digite o nome do Jogador 1 (X): ")
    nome2 = input("Digite o nome do jogador 2 (O): ")

    jogo = JogoDaVelha(nome1, nome2)

    while True:
        jogo.tabuleiro.imprimir()
        jogador_atual = jogo.jogador_atual()

        print(f"Vez de {jogador_atual.nome} jogar com '{jogador_atual.simbolo}'")

        try:
            linha = int(input("Escolha a linha?:  ")) - 1
            coluna = int(input("Escolha a coluna?:  ")) - 1
        except ValueError:
            print("Digite apenas numeros inteiros!")
            continue

        if jogo.aplicar_jogada(origem=None, destino=(linha, coluna)):
            resultado = jogo.verificar_fim_de_jogo()

            if resultado:
                jogo.tabuleiro.imprimir()
                if resultado == "Empate":
                    print("Fim de jogo! Deu Velha!")
                else:
                    print(f"Fim de jogo! O jogador {resultado.nome} ({resultado.simbolo}) venceu!")
                break
            else:
                jogo.alternar_turno()

        else:
            print("Jogada inválida! Escolha outra casa vazia dentro do limite!")
