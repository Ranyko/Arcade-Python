from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty
from app.textos import Textos

class IndicadorTurno(Widget):
    """
    Widget customizado que desenha um círculo colorido para 
    indicar visualmente de quem é a vez de jogar.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(20), dp(20))
        self.cor = [0.8, 0.8, 0.8, 1]
        self.bind(pos=self._desenhar, size=self._desenhar)
        self._desenhar()

    def _desenhar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.cor)
            Ellipse(pos=self.pos, size=self.size)

    def atualizar(self, cor):
        self.cor = cor
        self._desenhar()


class CelulaBase(MDCard):
    """
    Classe base abstrata para as células do tabuleiro.
    Lida com os eventos de clique e feedback visual básico.
    """
    def __init__(self, linha, coluna, ao_clicar, **kwargs):
        super().__init__(**kwargs)
        self.linha = linha
        self.coluna = coluna
        self.ao_clicar = ao_clicar
        self.ocupada = False
        self.style = "elevated"
        self.elevation = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.ocupada:
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.collide_point(*touch.pos):
                self.ao_clicar(self.linha, self.coluna)
            return True
        return super().on_touch_up(touch)


class CelulaVelha(CelulaBase):
    """Célula específica para o Jogo da Velha, com label de texto para 'X' ou 'O'."""
    escala_texto = NumericProperty(0.1)

    def __init__(self, linha, coluna, ao_clicar, **kwargs):
        super().__init__(
            linha=linha,
            coluna=coluna,
            ao_clicar=ao_clicar,
            **kwargs
        )
        self.radius = [8]
        self.label = MDLabel(
            text=Textos.ESPACO_VAZIO,
            halign="center",
            valign="center",
            font_style="H3",
            theme_text_color="Primary"
        )

        self.add_widget(self.label)

    def atualizar(self, simbolo, cor):
        """Atualiza a célula com o símbolo do jogador e aplica uma animação de escala."""
        if cor is None:
            return
        if not self.ocupada:
            self.ocupada = True
            self.md_bg_color = cor
            self.label.text = simbolo
            self.label.theme_text_color = "Custom"
            self.label.text_color = [1, 1, 1, 1]
            
            self.opacity = 0
            self.label.font_size = 1
            anim = Animation(opacity=1, duration=0.3)
            anim.start(self)
            
            def animar_fonte(dt):
                anim_font = Animation(font_size=dp(48), duration=0.4, t='out_back')
                anim_font.start(self.label)
            Clock.schedule_once(animar_fonte, 0.05)


class CelulaConnect4(CelulaBase):
    """Célula específica para Connect 4, com um círculo desenhado no canvas."""
    desloc_y = NumericProperty(dp(400))

    def __init__(self, linha, coluna, ao_clicar, **kwargs):
        super().__init__(
            linha=linha,
            coluna=coluna,
            ao_clicar=ao_clicar,
            **kwargs
        )
        self.cor_peca = None
        self.md_bg_color = [0.08, 0.22, 0.52, 1]
        self.radius = [4]
        self.desloc_y = 0
        self.bind(pos=self._redesenhar, size=self._redesenhar, desloc_y=self._redesenhar)
        
        app = MDApp.get_running_app()
        app.theme_cls.bind(theme_style=self._redesenhar)

    def _redesenhar(self, *args):
        self.canvas.after.clear()
        with self.canvas.after:
            app = MDApp.get_running_app()
            is_dark = app.theme_cls.theme_style == "Dark"
            vazia_cor = [0.18, 0.18, 0.18, 1] if is_dark else [0.82, 0.82, 0.82, 1]
            Color(*(self.cor_peca if self.cor_peca else vazia_cor))
            m = min(self.width, self.height) * 0.12
            d = min(self.width, self.height) - 2 * m
            Ellipse(
                pos=(self.x + (self.width - d) / 2, self.y + (self.height - d) / 2 + self.desloc_y),
                size=(d, d)
            )

    def atualizar(self, cor):
        """Atualiza a cor da peça e aplica animação de queda (bounce)."""
        if cor is None:
            return
        if not self.ocupada:
            self.ocupada = True
            self.cor_peca = cor
            

            self.desloc_y = dp(400)
            anim = Animation(desloc_y=0, duration=0.6, t='out_bounce')
            anim.start(self)


class BoardScreen(MDScreen):
    """
    Tela principal de jogatina. Contém o tabuleiro dinâmico,
    indicador de turno, timer e lógica de interação do usuário com o jogo.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.celulas = {}
        self.mapa_cores = {}
        self.bloqueado = False
        self.tempo_restante = 15
        self.timer_event = None

        layout = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(8))

        self.toolbar = MDTopAppBar(
            title="Partida",
            elevation=0
        )
        self.toolbar.size_hint_y = None
        self.toolbar.height = dp(56)
        layout.add_widget(self.toolbar)


        self.status_card = MDCard(
            size_hint=(1, None),
            height=dp(80),
            padding=dp(12),
            radius=[12],
            elevation=0,
            style="elevated",
            orientation="vertical"
        )
        self.status_card.atualiza_bg_automatico = True
        
        #Turno
        linha_turno = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=0.5)
        self.indicador = IndicadorTurno(pos_hint={"center_y": 0.5})
        self.label_status = MDLabel(
            text=Textos.VEZ_DE_INICIAL,
            font_style="Subtitle1",
            pos_hint={"center_y": 0.5},
            adaptive_width=True
        )
        
        self.label_timer = MDLabel(
            text=Textos.TEMPO_INICIAL,
            font_style="H6",
            theme_text_color="Error",
            pos_hint={"center_y": 0.5},
            halign="right"
        )
        
        linha_turno.add_widget(self.indicador)
        linha_turno.add_widget(self.label_status)
        linha_turno.add_widget(self.label_timer)
        self.status_card.add_widget(linha_turno)
        
        # Placar global
        self.label_placar = MDLabel(
            text=Textos.PLACAR_INICIAL,
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=0.5
        )
        self.status_card.add_widget(self.label_placar)
        layout.add_widget(self.status_card)

        # Tabuleiro
        self.grade = GridLayout(spacing=dp(4), padding=dp(4))
        layout.add_widget(self.grade)

        # Botão voltar (autossave)
        btn_menu = MDFlatButton(
            text=Textos.BTN_VOLTAR_SALVAR,
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(44)),
            on_release=lambda x: self.voltar_e_salvar()
        )
        layout.add_widget(btn_menu)

        self.add_widget(layout)

    def atualizar_icon_tema(self):
        app = MDApp.get_running_app()
        icon_name = app.get_tema_icon()
        self.toolbar.right_action_items = [[icon_name, lambda x: app._tema_e_atualiza()]]

    def on_enter(self):
        self.atualizar_icon_tema()
        MDApp.get_running_app()._forcar_atualizacao_textos(self)

    def voltar_e_salvar(self):
        app = MDApp.get_running_app()
        app.controller.salvar_partida()
        self.parar_timer()
        Snackbar(text=Textos.MSG_SALVO).open()
        self.manager.current = "menu"

    def iniciar_timer(self):
        self.parar_timer()
        self.tempo_restante = 15
        self.label_timer.text = Textos.TEMPO_FORMAT.format(self.tempo_restante)
        self.timer_event = Clock.schedule_interval(self._tick_timer, 1)

    def parar_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def _tick_timer(self, dt):
        if self.bloqueado:
            return
        self.tempo_restante -= 1
        self.label_timer.text = Textos.TEMPO_FORMAT.format(self.tempo_restante)
        if self.tempo_restante <= 0:
            self.parar_timer()
            Snackbar(text=Textos.MSG_TEMPO_ESGOTADO).open()
            app = MDApp.get_running_app()
            app.controller.game.alternar_turno()
            self.atualizar_status_visual()
            self.verificar_vez_ia()

    def montar_tabuleiro(self):
        """Constrói a grade (grid) de células baseada nas dimensões do jogo escolhido."""
        app = MDApp.get_running_app()
        linhas, colunas = app.controller.get_dimensoes()
        sim1, sim2 = app.controller.get_simbolos()

        self.mapa_cores = {sim1: app.cor_j1, sim2: app.cor_j2}

        self.grade.clear_widgets()
        self.grade.cols = colunas
        self.celulas = {}

        classe_celula = CelulaVelha if app.tipo_jogo == "velha" else CelulaConnect4

        for l in range(linhas):
            for c in range(colunas):
                cel = classe_celula(linha=l, coluna=c, ao_clicar=self.clicar_celula)
                self.celulas[(l, c)] = cel
                self.grade.add_widget(cel)

        self.toolbar.title = Textos.TITULO_VELHA if app.tipo_jogo == "velha" else Textos.TITULO_CONNECT4
        self.bloqueado = False
        
        # Placar global da sessão
        p = app.placar
        j1 = app.controller.game.jogadores[0].nome
        j2 = app.controller.game.jogadores[1].nome
        self.label_placar.text = Textos.PLACAR_FORMAT.format(j1, p['j1'], p['j2'], j2, p['empates'])
        
        self.atualizar_status_visual()

    def clicar_celula(self, linha, coluna):
        """
        Callback disparado quando uma célula é clicada.
        Processa a jogada interagindo com o GameController.
        """
        if self.bloqueado:
            return

        app = MDApp.get_running_app()
        resultado = app.controller.fazer_jogada(linha, coluna)

        if not resultado["valida"]:
            return

        self.atualizar_grade(resultado["estado"])

        if resultado["fim"]:
            self.parar_timer()
            self.manager.get_screen("result").mostrar_resultado(resultado["resultado"])
            self.manager.current = "result"
        else:
            self.atualizar_status_visual()
            self.verificar_vez_ia()

    def verificar_vez_ia(self):
        """Verifica se é o turno da máquina e agenda a sua jogada."""
        app = MDApp.get_running_app()
        if app.controller.contra_ia and app.controller.game.turno_atual == 1:
            self.bloqueado = True
            self.label_status.text = Textos.IA_PENSANDO
            self.indicador.atualizar(app.cor_j2)
            self.parar_timer()
            self.label_timer.text = Textos.ESPACO_VAZIO.strip()
            Clock.schedule_once(lambda dt: self.executar_rodada_ia(), 0.8)

    def executar_rodada_ia(self):
        app = MDApp.get_running_app()
        jogada = app.controller.obter_jogada_ia()
        
        if jogada is None:
            self.bloqueado = False
            self.atualizar_status_visual()
            return
            
        linha, coluna = jogada
        resultado = app.controller.fazer_jogada(linha, coluna)
        
        if not resultado["valida"]:
            self.bloqueado = False
            self.atualizar_status_visual()
            return
            
        self.atualizar_grade(resultado["estado"])
        
        if resultado["fim"]:
            self.parar_timer()
            self.manager.get_screen("result").mostrar_resultado(resultado["resultado"])
            self.manager.current = "result"
        else:
            self.bloqueado = False
            self.atualizar_status_visual()

    def atualizar_grade(self, estado):
        """Atualiza todas as células da interface com o estado atual do Model."""
        app = MDApp.get_running_app()
        for (l, c), cel in self.celulas.items():
            valor = estado[l][c]
            if valor != " ":
                cor = self.mapa_cores.get(valor)
                if app.tipo_jogo == "velha":
                    cel.atualizar(valor, cor)
                else:
                    cel.atualizar(cor)

    def atualizar_status_visual(self):
        """Atualiza as labels de turno e a cor do indicador visual na parte superior."""
        app = MDApp.get_running_app()
        if not app.controller.game:
            return
            
        nome_atual = app.controller.jogador_atual()
        self.label_status.text = Textos.VEZ_DE_FORMAT.format(nome_atual)
        
        turno = app.controller.game.turno_atual
        cor = app.cor_j1 if turno == 0 else app.cor_j2
        self.indicador.atualizar(cor)
        
        anim = Animation(opacity=0.3, duration=0.2) + Animation(opacity=1, duration=0.2)
        anim.start(self.indicador)
        
        if not self.bloqueado:
            self.iniciar_timer()