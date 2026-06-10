from src.core.base import JogoTabuleiro, Tabuleiro, Jogador


class JogoDaVelha(JogoTabuleiro):
    def __init__(self, nome_j1, nome_j2):
        j1 = Jogador(nome_j1, "X")
        j2 = Jogador(nome_j2, "O")

        super().__init__(j1, j2)
        self.inicializar_jogo()

    def inicializar_jogo(self):
        self.tabuleiro = Tabuleiro(3, 3)
        self.turno_atual = 0


    def validar_jogada(self, origem, destino):
        linha, coluna = destino

        if linha < 0 or linha > 2 or coluna < 0 or coluna > 2:
            return False

        if self.tabuleiro.estado[linha][coluna] != " ":
            return False

        return True

    def aplicar_jogada(self, origem, destino):
        if self.validar_jogada(origem, destino):
            linha, coluna = destino
            jogador = self.jogador_atual()

            self.tabuleiro.estado[linha][coluna] = jogador.simbolo
            return True

        return False

    def verificar_fim_de_jogo(self):
        matriz = self.tabuleiro.estado

        linhas = matriz

        colunas = [[matriz[linha][coluna] for linha in range (3)] for coluna in range(3)]

        diagonal_principal = [matriz[i][i] for i in range(3)]
        diagonal_secundaria = [matriz[i][2 - i] for i in range(3)]

        todas_combinacoes = linhas + colunas + [diagonal_principal, diagonal_secundaria]

        for combinacao in todas_combinacoes:
            if len(set(combinacao)) == 1 and combinacao [0] != " ":
                simbolo_vencedor = combinacao [0]

                if self.jogadores[0].simbolo == simbolo_vencedor:
                    return self.jogadores[0]
                else:
                    return self.jogadores[1]


        for linha in matriz:
            if " " in linha:
                return None

        return "Empate"