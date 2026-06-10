from abc import ABC, abstractmethod

class Jogador:
    def __init__(self, nome, simbolo):
        self.nome = nome
        self.simbolo = simbolo

    #Jogador eh usado pra jogos simples e as Pecas caso o jogo seja mais complexo

class Peca:
    def __init__(self, nome, movimento):
        self.nome = nome
        self.movimento = movimento


class Tabuleiro:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.estado = [[" " for _ in range(colunas)] for _ in range(linhas)]
        #cria uma matriz vazia pra ser preenchida conforme necessário

    def imprimir(self):
        print("\n")
        for linha in self.estado:
            print(" | ".join(linha))
            print("-" * (self.colunas * 4 - 1))
        print("\n")

    def get_celula(self, linha, coluna):
        return self.estado[linha][coluna]

    def set_celula(self, linha, coluna, simbolo):
        self.estado[linha][coluna] = simbolo

    def celula_vazia(self, linha, coluna):
        return self.estado[linha][coluna] == " "

    def linha_cheia(self, linha):
        return " " not in self.estado[linha]

class JogoTabuleiro(ABC):
    def __init__(self, jogador1, jogador2):
        self.jogadores = [jogador1, jogador2]
        self.turno_atual = 0
        self.tabuleiro = None

    def alternar_turno(self):
        self.turno_atual = 1 - self.turno_atual

    def jogador_atual(self):
        return self.jogadores[self.turno_atual]


    #os abstract obrigam as classes filha a inicia los

    @abstractmethod
    def inicializar_jogo(self):
        pass

    @abstractmethod
    def validar_jogada(self, origem, destino):
        pass

    @abstractmethod
    def aplicar_jogada(self, origem, destino):
        pass

    @abstractmethod
    def verificar_fim_de_jogo(self):
        pass