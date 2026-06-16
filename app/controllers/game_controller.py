import json
import os
import random
from src.regras.jogo_da_velha import JogoDaVelha
from src.regras.connect_4 import Connect4

class GameController:
    """
    Controlador principal que faz a ponte entre a interface (Views) 
    e as regras de negócio (Models) do jogo.
    """
    
    def __init__(self):
        """Inicializa o estado do GameController."""
        self.game = None
        self.tipo_jogo = None
        self.fim = False
        self.contra_ia = False

    def iniciar_partida(self, tipo_jogo, nome1, nome2, contra_ia=False):
        """
        Inicia uma nova partida de acordo com o jogo escolhido.
        
        Args:
            tipo_jogo (str): 'velha' ou 'connect4'.
            nome1 (str): Nome do Jogador 1.
            nome2 (str): Nome do Jogador 2.
            contra_ia (bool): True se o adversário for a máquina.
        """
        self.tipo_jogo = tipo_jogo
        self.fim = False
        self.contra_ia = contra_ia
        
        if tipo_jogo == "velha":
            self.game = JogoDaVelha(nome1, nome2)
        else:
            self.game = Connect4(nome1, nome2)

    def get_simbolos(self):
        """
        Retorna os símbolos dos jogadores da partida atual.
        
        Returns:
            tuple: (simbolo_j1, simbolo_j2)
        """
        if self.game:
            return self.game.jogadores[0].simbolo, self.game.jogadores[1].simbolo
        return "1", "2"

    def fazer_jogada(self, linha, coluna):
        """
        Executa uma jogada no tabuleiro e verifica as consequências.
        
        Args:
            linha (int): Índice da linha da jogada.
            coluna (int): Índice da coluna da jogada.
            
        Returns:
            dict: Estado resultante da jogada, validade, e se o jogo acabou.
        """
        if self.fim or not self.game:
            return {"valida": False}
            
        if not self.game.aplicar_jogada(None, (linha, coluna)):
            return {"valida": False}
            
        resultado = self.game.verificar_fim_de_jogo()
        if resultado is not None:
            self.fim = True
            texto = "Empate!" if resultado == "Empate" else f"{resultado.nome} venceu!"
            return {
                "valida": True,
                "estado": self.game.tabuleiro.estado,
                "fim": True,
                "resultado": texto
            }
            
        self.game.alternar_turno()
        return {
            "valida": True,
            "estado": self.game.tabuleiro.estado,
            "fim": False,
            "proximo": self.game.jogador_atual().nome
        }

    def jogador_atual(self):
        """Retorna o nome do jogador do turno atual."""
        return self.game.jogador_atual().nome if self.game else ""

    def get_dimensoes(self):
        """Retorna as dimensões (linhas, colunas) do tabuleiro atual."""
        if self.game:
            return self.game.tabuleiro.linhas, self.game.tabuleiro.colunas
        return 3, 3

    def obter_jogada_ia(self):
        """
        Calcula a melhor jogada possível para a IA (Heurística simples).
        
        Returns:
            tuple: (linha, coluna) da jogada da IA, ou None se inválida.
        """
        if not self.game or self.fim:
            return None
            
        jogador_humano = self.game.jogadores[0]
        jogador_ia = self.game.jogadores[1]
        
        simbolo_humano = jogador_humano.simbolo
        simbolo_ia = jogador_ia.simbolo
        
        if self.tipo_jogo == "velha":
            #Tenta ganhar
            for r in range(3):
                for c in range(3):
                    if self.game.tabuleiro.celula_vazia(r, c):
                        self.game.tabuleiro.set_celula(r, c, simbolo_ia)
                        vencedor = self.game.verificar_fim_de_jogo()
                        self.game.tabuleiro.set_celula(r, c, " ")
                        if vencedor == jogador_ia:
                            return r, c

            #Tenta bloquear o jogador
            for r in range(3):
                for c in range(3):
                    if self.game.tabuleiro.celula_vazia(r, c):
                        self.game.tabuleiro.set_celula(r, c, simbolo_humano)
                        vencedor = self.game.verificar_fim_de_jogo()
                        self.game.tabuleiro.set_celula(r, c, " ")
                        if vencedor == jogador_humano:
                            return r, c
                            
            #Tenta por no meio
            if self.game.tabuleiro.celula_vazia(1, 1):
                return 1, 1
                
            #Tenta os cantos
            cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
            random.shuffle(cantos)
            for r, c in cantos:
                if self.game.tabuleiro.celula_vazia(r, c):
                    return r, c
                    
            # 5. Qualquer célula vazia
            vazias = []
            for r in range(3):
                for c in range(3):
                    if self.game.tabuleiro.celula_vazia(r, c):
                        vazias.append((r, c))
            if vazias:
                return random.choice(vazias)


        elif self.tipo_jogo == "connect4":
            #Tenta vencer em 1 movimento
            for c in range(7):
                if self.game.validar_jogada(None, (None, c)):
                    # Encontrar a linha onde cairia
                    r_dest = -1
                    for r in range(5, -1, -1):
                        if self.game.tabuleiro.celula_vazia(r, c):
                            r_dest = r
                            break
                    if r_dest != -1:
                        original_ultima = self.game.ultima_jogada
                        self.game.tabuleiro.set_celula(r_dest, c, simbolo_ia)
                        self.game.ultima_jogada = (r_dest, c)
                        vencedor = self.game.verificar_fim_de_jogo()
                        self.game.tabuleiro.set_celula(r_dest, c, " ")
                        self.game.ultima_jogada = original_ultima
                        if vencedor == jogador_ia:
                            return r_dest, c
                            
            #Bloqueia o jogador
            for c in range(7):
                if self.game.validar_jogada(None, (None, c)):
                    r_dest = -1
                    for r in range(5, -1, -1):
                        if self.game.tabuleiro.celula_vazia(r, c):
                            r_dest = r
                            break
                    if r_dest != -1:
                        original_ultima = self.game.ultima_jogada
                        self.game.tabuleiro.set_celula(r_dest, c, simbolo_humano)
                        self.game.ultima_jogada = (r_dest, c)
                        vencedor = self.game.verificar_fim_de_jogo()
                        self.game.tabuleiro.set_celula(r_dest, c, " ")
                        self.game.ultima_jogada = original_ultima
                        if vencedor == jogador_humano:
                            return r_dest, c
                            
            # Foca nas colunas centrais
            prefs = [3, 2, 4, 1, 5, 0, 6]
            for c in prefs:
                if self.game.validar_jogada(None, (None, c)):
                    for r in range(5, -1, -1):
                        if self.game.tabuleiro.celula_vazia(r, c):
                            return r, c
                            
        return None

    def salvar_partida(self):
        """
        Salva o estado atual da partida no arquivo 'savegame.json'.
        
        Returns:
            bool: True se salvo com sucesso, False caso contrário.
        """
        if not self.game:
            return False
            
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        data = {
            "tipo_jogo": self.tipo_jogo,
            "contra_ia": self.contra_ia,
            "fim": self.fim,
            "jogadores": [
                {"nome": self.game.jogadores[0].nome, "simbolo": self.game.jogadores[0].simbolo},
                {"nome": self.game.jogadores[1].nome, "simbolo": self.game.jogadores[1].simbolo}
            ],
            "turno_atual": self.game.turno_atual,
            "estado": self.game.tabuleiro.estado,
            "ultima_jogada": getattr(self.game, "ultima_jogada", None),
            "cor_j1": app.cor_j1,
            "cor_j2": app.cor_j2
        }
        
        try:
            with open("savegame.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar partida: {e}")
            return False

    def carregar_partida(self):
        """
        Carrega uma partida salva anteriormente do arquivo 'savegame.json'.
        
        Returns:
            bool: True se carregado com sucesso, False caso contrário.
        """
        if not os.path.exists("savegame.json"):
            return False
            
        try:
            with open("savegame.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.tipo_jogo = data["tipo_jogo"]
            self.contra_ia = data["contra_ia"]
            self.fim = data["fim"]
            
            nome1 = data["jogadores"][0]["nome"]
            nome2 = data["jogadores"][1]["nome"]
            
            if self.tipo_jogo == "velha":
                self.game = JogoDaVelha(nome1, nome2)
            else:
                self.game = Connect4(nome1, nome2)
                
            self.game.turno_atual = data["turno_atual"]
            self.game.tabuleiro.estado = data["estado"]
            
            if hasattr(self.game, "ultima_jogada"):
                self.game.ultima_jogada = data["ultima_jogada"]
                
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            app.cor_j1 = data["cor_j1"]
            app.cor_j2 = data["cor_j2"]
            app.tipo_jogo = self.tipo_jogo
            
            return True
        except Exception as e:
            print(f"Erro ao carregar partida: {e}")
            return False
