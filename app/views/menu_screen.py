import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons


class MenuScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Menu Principal",
            elevation=0,
        )
        self.toolbar.size_hint_y = None
        self.toolbar.height = dp(56)
        layout.add_widget(self.toolbar)

        content = BoxLayout(
            orientation="vertical",
            padding=dp(32),
            spacing=dp(20),
        )


        icon_box = BoxLayout(size_hint_y=None, height=dp(180))
        icon_box.add_widget(BoxLayout(size_hint_x=1))
        self.game_icon = MDLabel(
            text=md_icons["controller-classic"],
            font_style="Icon",
            font_size="200sp",
            size_hint=(None, None),
            size=(dp(200), dp(200)),
            halign="center",
            valign="center",
            theme_text_color="Primary",
            pos_hint={"center_y": 0.5, "center_x": 0.5}
        )
        icon_box.add_widget(self.game_icon)
        icon_box.add_widget(BoxLayout(size_hint_x=1))
        content.add_widget(icon_box)

        self.titulo = MDLabel(
            text="Central de Jogos!",
            halign="center",
            font_style="H4",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(50),
        )
        content.add_widget(self.titulo)

        self.subtitulo = MDLabel(
            text="clássicos de tabuleiro",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30),
        )
        content.add_widget(self.subtitulo)

        content.add_widget(BoxLayout(size_hint_y=1))

        self.btn_iniciar = MDFillRoundFlatButton(
            text="Nova Partida",
            size_hint=(None, None),
            size=(dp(240), dp(50)),
            pos_hint={"center_x": 0.5},
            font_size="16sp",
            on_release=lambda x: self.ir_para_selecao()
        )
        content.add_widget(self.btn_iniciar)

        self.btn_carregar = MDFillRoundFlatButton(
            text="Carregar Partida",
            size_hint=(None, None),
            size=(dp(240), dp(50)),
            pos_hint={"center_x": 0.5},
            font_size="16sp",
            md_bg_color=[0.12, 0.53, 0.53, 1],
            on_release=lambda x: self.carregar_jogo()
        )
        content.add_widget(self.btn_carregar)

        self.btn_sair = MDFlatButton(
            text="Sair do Jogo",
            size_hint=(None, None),
            size=(dp(240), dp(48)),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: MDApp.get_running_app().stop()
        )
        content.add_widget(self.btn_sair)

        content.add_widget(BoxLayout(size_hint_y=1))

        layout.add_widget(content)
        self.add_widget(layout)
        self.atualizar_icon_tema()

    def on_enter(self):
        salvo_existe = os.path.exists("savegame.json")
        self.btn_carregar.disabled = not salvo_existe
        self.atualizar_icon_tema()
        MDApp.get_running_app()._forcar_atualizacao_textos(self)

    def ir_para_selecao(self):
        self.manager.current = "select"

    def carregar_jogo(self):
        app = MDApp.get_running_app()
        if app.controller.carregar_partida():
            board_scr = self.manager.get_screen("board")
            board_scr.montar_tabuleiro()
            board_scr.atualizar_grade(app.controller.game.tabuleiro.estado)
            if app.controller.contra_ia and app.controller.game.turno_atual == 1:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: board_scr.executar_rodada_ia(), 0.8)
            self.manager.current = "board"

    def atualizar_icon_tema(self):
        app = MDApp.get_running_app()
        icon_name = app.get_tema_icon()
        self.toolbar.right_action_items = [[icon_name, lambda x: app._tema_e_atualiza()]]
