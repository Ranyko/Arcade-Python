from src.core.base import JogoTabuleiro, Tabuleiro, Jogador

class Connect4(JogoTabuleiro):
    def __init__(self, nome_j1, nome_j2):
        j1 = Jogador(nome_j1, "⭕" )
        j2 = Jogador(nome_j2, "🔵")
        self.ultima_jogada = None

        super().__init__(j1, j2)
        self.inicializar_jogo()


    def inicializar_jogo(self):
        self.tabuleiro = Tabuleiro(6,7)
        self.turno_atual = 0

    def validar_jogada(self, origem, destino):
        _, coluna = destino

        if coluna > 6 or coluna < 0:
            return False

        return self.tabuleiro.celula_vazia(0,coluna)



    def aplicar_jogada(self, origem, destino):
        if self.validar_jogada(origem, destino):
            _, coluna = destino
            jogador = self.jogador_atual()

            for linha in range(5, -1,-1): #faz a gravidade
                if self.tabuleiro.celula_vazia(linha, coluna):
                    self.tabuleiro.set_celula(linha,coluna,jogador.simbolo)
                    self.ultima_jogada = (linha,coluna)
                    return True


        return False

    def verificar_fim_de_jogo(self):
        if not self.ultima_jogada:
            return None

        linha, coluna = self.ultima_jogada
        simbolo = self.tabuleiro.get_celula(linha,coluna)
        jogador_atual = self.jogador_atual()

        direcoes = [
            (0,1), #horizontal
            (1,0), #vertical
            (1,1), #diagonal esquerda
            (1,-1) #diagonal direita
        ]

        for d_linha, d_coluna in direcoes:
            contador = 1

            for i in range(1,4):
                l = linha + (d_linha * i)
                c = coluna + (d_coluna * i)

                if 0 <= l < 6 and 0 <= c < 7 and self.tabuleiro.get_celula(l,c) == simbolo:
                    contador += 1
                else:
                    break

            for i in range(1,4):
                l = linha - (d_linha * i)
                c = coluna - (d_coluna * i)

                if 0 <= l < 6 and 0 <= c < 7 and self.tabuleiro.get_celula(l,c) == simbolo:
                    contador += 1
                else:
                    break

            if contador >= 4:
                if self.jogadores[0].simbolo == simbolo:
                    return self.jogadores[0]
                else:
                    return self.jogadores[1]

        if self.tabuleiro.linha_cheia(0):
            return "Empate"

        return None