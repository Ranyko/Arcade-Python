from kivymd.uix.screen    import MDScreen
from kivymd.uix.toolbar   import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button    import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.label     import MDLabel
from kivymd.uix.snackbar  import Snackbar
from kivymd.uix.dialog    import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.app           import MDApp
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.gridlayout  import GridLayout
from kivy.uix.button      import Button
from kivy.graphics        import Color, Ellipse
from kivy.metrics         import dp
from app.cores            import CORES


class SwatchCor(Button):
    def __init__(self, nome, cor, ao_selecionar, **kwargs):
        super().__init__(
            size_hint        = (None, None),
            size             = (dp(44), dp(44)),
            background_normal= '',
            background_color = [0, 0, 0, 0],
            **kwargs
        )
        self.nome_cor      = nome
        self.cor_peca      = cor
        self.ao_selecionar = ao_selecionar
        self.selecionado   = False
        self.bind(on_release=lambda x: ao_selecionar(self))
        self.bind(pos=self._desenhar, size=self._desenhar)
        self._desenhar()

    def _desenhar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.selecionado:
                Color(1, 1, 1, 1)
                Ellipse(pos=self.pos, size=self.size)
            m = self.width * 0.11 if self.selecionado else 0
            d = self.width - 2 * m
            Color(*self.cor_peca)
            Ellipse(pos=(self.x + m, self.y + m), size=(d, d))

    def marcar(self):
        self.selecionado = True
        self._desenhar()

    def desmarcar(self):
        self.selecionado = False
        self._desenhar()


class DialogCor(MDBoxLayout):
    def __init__(self, ao_selecionar, **kwargs):
        super().__init__(
            orientation = "vertical",
            size_hint_y = None,
            height      = dp(130),
            padding     = dp(8),
            spacing     = dp(8),
            **kwargs
        )
        self.ao_selecionar = ao_selecionar
        self._swatches     = []

        grade = GridLayout(
            cols           = 5,
            spacing        = dp(8),
            size_hint      = (None, None),
            size           = (dp(252), dp(96)),
            pos_hint       = {"center_x": 0.5},
        )

        for nome, cor in CORES:
            sw = SwatchCor(nome=nome, cor=cor, ao_selecionar=self._on_sw)
            self._swatches.append(sw)
            grade.add_widget(sw)

        self._swatches[0].marcar()
        self.cor_atual = CORES[0][1]
        self.add_widget(grade)

    def _on_sw(self, sw_clicado):
        for sw in self._swatches:
            sw.desmarcar()
        sw_clicado.marcar()
        self.cor_atual = sw_clicado.cor_peca
        self.ao_selecionar(sw_clicado.cor_peca)

    def pre_selecionar(self, cor):
        for sw in self._swatches:
            sw.desmarcar()
            if sw.cor_peca == cor:
                sw.marcar()
        self.cor_atual = cor


class PreviewCor(Button):
    def __init__(self, cor_inicial, **kwargs):
        super().__init__(
            size_hint        = (None, None),
            size             = (dp(36), dp(36)),
            background_normal= '',
            background_color = [0, 0, 0, 0],
            **kwargs
        )
        self.cor_atual = cor_inicial
        self.bind(pos=self._desenhar, size=self._desenhar)
        self._desenhar()

    def _desenhar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.cor_atual)
            Ellipse(pos=self.pos, size=self.size)

    def atualizar(self, cor):
        self.cor_atual = cor
        self._desenhar()


class ConfigScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cor_j1    = CORES[1][1]   # Azul
        self.cor_j2    = CORES[0][1]   # Vermelho
        self._dialog_j1 = None
        self._dialog_j2 = None

        raiz = BoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title     = "Configurar Partida",
            elevation = 0,
            left_action_items=[["arrow-left", lambda x: self.voltar()]],
        )
        self.toolbar.size_hint_y = None
        self.toolbar.height      = dp(56)

        corpo = BoxLayout(
            orientation = "vertical",
            padding     = dp(24),
            spacing     = dp(14),
        )

        # Opção para o ‘Bot’
        self.linha_ia = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.chk_ia = MDCheckbox(
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            pos_hint={"center_y": 0.5}
        )
        self.chk_ia.bind(active=self._on_ia_active)
        
        self.lbl_ia = MDLabel(
            text="Jogar contra Computador (IA)",
            pos_hint={"center_y": 0.5},
            font_style="Body1",
            theme_text_color="Primary"
        )
        self.linha_ia.add_widget(self.chk_ia)
        self.linha_ia.add_widget(self.lbl_ia)
        corpo.add_widget(self.linha_ia)

        # Jogador 1
        corpo.add_widget(MDLabel(
            text="Jogador 1", font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None, height=dp(28),
        ))
        self.campo_j1 = MDTextField(hint_text="Nome do Jogador 1")
        corpo.add_widget(self.campo_j1)

        self._linha_cor_j1 = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self._preview_j1   = PreviewCor(cor_inicial=self.cor_j1, on_release=lambda x: self._abrir_dialog(1))
        self._linha_cor_j1.add_widget(self._preview_j1)
        self._linha_cor_j1.add_widget(MDLabel(
            text="Toque na cor para alterar",
            font_style="Body2",
            theme_text_color="Secondary",
            pos_hint={"center_y": 0.5}
        ))
        corpo.add_widget(self._linha_cor_j1)

        # Jogador 2
        self.lbl_jogador2 = MDLabel(
            text="Jogador 2", font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None, height=dp(28),
        )
        corpo.add_widget(self.lbl_jogador2)
        self.campo_j2 = MDTextField(hint_text="Nome do Jogador 2")
        corpo.add_widget(self.campo_j2)

        self._linha_cor_j2 = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self._preview_j2   = PreviewCor(cor_inicial=self.cor_j2, on_release=lambda x: self._abrir_dialog(2))
        self._linha_cor_j2.add_widget(self._preview_j2)
        self._linha_cor_j2.add_widget(MDLabel(
            text="Toque na cor para alterar",
            font_style="Body2",
            theme_text_color="Secondary",
            pos_hint={"center_y": 0.5}
        ))
        corpo.add_widget(self._linha_cor_j2)

        corpo.add_widget(BoxLayout(size_hint_y=1))

        corpo.add_widget(MDFillRoundFlatButton(
            text       = "Iniciar Partida",
            size_hint  = (None, None),
            size       = (dp(220), dp(50)),
            pos_hint   = {"center_x": 0.5},
            on_release = lambda x: self.confirmar()
        ))

        raiz.add_widget(self.toolbar)
        raiz.add_widget(corpo)
        self.add_widget(raiz)

    def _on_ia_active(self, checkbox, value):
        if value:
            self.campo_j2.text = "Computador (IA)"
            self.campo_j2.readonly = True
        else:
            self.campo_j2.text = ""
            self.campo_j2.readonly = False

    def _abrir_dialog(self, jogador):
        cor_atual = self.cor_j1 if jogador == 1 else self.cor_j2

        if jogador == 1:
            if not self._dialog_j1:
                conteudo = DialogCor(ao_selecionar=lambda c: self._salvar_cor(1, c))
                self._conteudo_j1 = conteudo
                self._dialog_j1   = MDDialog(
                    title       = "Cor do Jogador 1",
                    type        = "custom",
                    content_cls = conteudo,
                    buttons     = [MDFlatButton(
                        text="OK", on_release=lambda x: self._dialog_j1.dismiss()
                    )],
                )
            self._conteudo_j1.pre_selecionar(cor_atual)
            self._dialog_j1.open()
        else:
            if not self._dialog_j2:
                conteudo = DialogCor(ao_selecionar=lambda c: self._salvar_cor(2, c))
                self._conteudo_j2 = conteudo
                self._dialog_j2   = MDDialog(
                    title       = "Cor do Jogador 2",
                    type        = "custom",
                    content_cls = conteudo,
                    buttons     = [MDFlatButton(
                        text="OK", on_release=lambda x: self._dialog_j2.dismiss()
                    )],
                )
            self._conteudo_j2.pre_selecionar(cor_atual)
            self._dialog_j2.open()

    def _salvar_cor(self, jogador, cor):
        if jogador == 1:
            self.cor_j1 = cor
            self._preview_j1.atualizar(cor)
        else:
            self.cor_j2 = cor
            self._preview_j2.atualizar(cor)

    def on_enter(self):
        app      = MDApp.get_running_app()
        connect4 = app.tipo_jogo == "connect4"
        self.toolbar.title = "Configurar: Connect 4" if connect4 else "Configurar: Jogo da Velha"
        self.atualizar_icon_tema()
        app._forcar_atualizacao_textos(self)

        self._linha_cor_j1.opacity = 1
        self._linha_cor_j2.opacity = 1

        self.campo_j1.text = ""
        self.campo_j2.text = ""
        self.campo_j2.readonly = False
        self.chk_ia.active = False

    def confirmar(self):
        nome1 = self.campo_j1.text.strip()
        nome2 = self.campo_j2.text.strip()
        if not nome1 or not nome2:
            Snackbar(text="Preencha os dois nomes!").open()
            return
        if nome1.lower() == nome2.lower():
            Snackbar(text="Os nomes dos jogadores devem ser diferentes!").open()
            return

        app = MDApp.get_running_app()
        app.cor_j1 = self.cor_j1
        app.cor_j2 = self.cor_j2

        contra_ia = self.chk_ia.active
        app.controller.iniciar_partida(app.tipo_jogo, nome1, nome2, contra_ia=contra_ia)
        self.manager.get_screen("board").montar_tabuleiro()
        self.manager.current = "board"

    def voltar(self):
        self.manager.current = "select"

    def atualizar_icon_tema(self):
        app = MDApp.get_running_app()
        icon_name = app.get_tema_icon()
        self.toolbar.right_action_items = [[icon_name, lambda x: app._tema_e_atualiza()]]
