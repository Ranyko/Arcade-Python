from kivymd.uix.screen  import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card    import MDCard
from kivymd.uix.label   import MDLabel, MDIcon
from kivymd.uix.button  import MDFillRoundFlatButton
from kivymd.app         import MDApp
from kivy.uix.boxlayout   import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout  import GridLayout
from kivy.metrics import dp
from app.textos import Textos


class CardJogo(MDCard):
    """
    Componente visual reutilizável que representa um cartão de seleção
    para um dos jogos disponíveis na aplicação.
    """
    def __init__(self, titulo, icone, tipo, ao_selecionar, **kwargs):
        """Inicializa o cartão de jogo com os ícones, título e callback."""
        super().__init__(**kwargs)
        self.tipo          = tipo
        self.ao_selecionar = ao_selecionar

        self.atualiza_bg_automatico = True

        self.size_hint   = (None, None)
        self.size        = (dp(148), dp(148))
        self.radius      = [16]
        self.elevation   = 0
        self.padding     = dp(12)
        self.orientation = "vertical"
        self.spacing     = dp(6)

        self.add_widget(MDIcon(
            icon=icone,
            halign="center",
            font_size=dp(44),
            size_hint_y=None,
            height=dp(44),
            theme_text_color="Primary",
            pos_hint={"center_x": 0.5}
        ))

        self.add_widget(MDLabel(
            text=titulo,
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(28),
            pos_hint={"center_x": 0.5}
        ))

        self.add_widget(MDFillRoundFlatButton(
            text=Textos.BTN_JOGAR,
            size_hint=(None, None),
            size=(dp(110), dp(36)),
            pos_hint={"center_x": 0.5},
        ))

    def on_touch_down(self, touch):
        """Captura o evento de clique no cartão para efeito visual e lógica."""
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Finaliza o evento de clique e dispara a função de seleção."""
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.collide_point(*touch.pos):
                self.ao_selecionar(self.tipo)
            return True
        return super().on_touch_up(touch)


class GameSelectScreen(MDScreen):
    """Tela para o usuário escolher qual jogo de tabuleiro deseja jogar."""

    def __init__(self, **kwargs):
        """Inicializa a tela desenhando os botões e cartões de opções."""
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Selecionar Jogo",
            elevation=0,
            left_action_items=[["arrow-left", lambda x: self.voltar()]],
        )
        self.toolbar.size_hint_y = None
        self.toolbar.height = dp(56)

        grade = GridLayout(
            cols=2,
            spacing=dp(16),
            padding=dp(24),
            size_hint=(None, None),
            size=(dp(360), dp(196)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        grade.add_widget(CardJogo(
            titulo="Jogo da Velha",
            icone="close",
            tipo="velha",
            ao_selecionar=self.selecionar_jogo,
        ))
        grade.add_widget(CardJogo(
            titulo="Connect 4",
            icone="circle-multiple",
            tipo="connect4",
            ao_selecionar=self.selecionar_jogo,
        ))

        area = FloatLayout()
        area.add_widget(grade)

        layout.add_widget(self.toolbar)
        layout.add_widget(area)
        self.add_widget(layout)

    def on_enter(self):
        """Atualiza a UI assim que a tela entra em foco."""
        self.atualizar_icon_tema()
        MDApp.get_running_app()._forcar_atualizacao_textos(self)

    def selecionar_jogo(self, tipo):
        """Salva a escolha do usuário globalmente e avança para a tela de configuração."""
        MDApp.get_running_app().tipo_jogo = tipo
        self.manager.current = "config"

    def voltar(self):
        """Retorna à tela de menu."""
        self.manager.current = "menu"

    def atualizar_icon_tema(self):
        """Atualiza o ícone de alternância de tema no topo da tela."""
        app = MDApp.get_running_app()
        icon_name = app.get_tema_icon()
        self.toolbar.right_action_items = [[icon_name, lambda x: app._tema_e_atualiza()]]
