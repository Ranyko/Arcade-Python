from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate, Translate
import random
from kivymd.icon_definitions import md_icons
from app.textos import Textos

class EfeitoConfete(Widget):
    """
    Widget que renderiza uma animação de partículas (confetes) 
    para celebrar a vitória de um jogador.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.confetes = []

    def estourar(self):
        """Inicia a animação gerando partículas com posições, cores e velocidades aleatórias."""
        self.canvas.clear()
        self.confetes = []
        
        cx, cy = self.center_x, self.y + dp(100)
        
        cores = [
            (0.9, 0.2, 0.2), (0.2, 0.8, 0.2), (0.2, 0.4, 0.9), 
            (0.9, 0.8, 0.1), (0.8, 0.2, 0.8), (0.2, 0.9, 0.9)
        ]
        
        with self.canvas:
            for _ in range(120):
                r, g, b = random.choice(cores)
                cor_inst = Color(r, g, b, 1)
                
                PushMatrix()
                t_inst = Translate(cx, cy)
                rot_inst = Rotate(angle=random.uniform(0, 360), origin=(0, 0))
                tam = random.uniform(dp(8), dp(16))
                Rectangle(pos=(-tam/2, -tam/2), size=(tam, tam))
                PopMatrix()
                
                self.confetes.append({
                    "translate": t_inst,
                    "rotate": rot_inst,
                    "color": cor_inst,
                    "vx": random.uniform(-dp(400), dp(400)),
                    "vy": random.uniform(dp(400), dp(900)),
                    "rot_speed": random.uniform(-300, 300),
                    "time": 0
                })
                
        Clock.schedule_interval(self._atualizar, 1/60.0)

    def _atualizar(self, dt):
        ativas = False
        for conf in self.confetes:
            conf["time"] += dt
            if conf["time"] > 4.0:
                continue
                
            ativas = True
            conf["vy"] -= dp(900) * dt 
            

            conf["translate"].x += conf["vx"] * dt
            conf["translate"].y += conf["vy"] * dt
            conf["rotate"].angle += conf["rot_speed"] * dt

            conf["vx"] *= 0.98
            

            if conf["time"] > 2.0:
                conf["color"].a = max(0, (4.0 - conf["time"]) / 2.0)
                
        if not ativas:
            self.canvas.clear()
            return False
        return None


class ResultScreen(MDScreen):
    """
    Tela final que exibe o resultado da partida (vitória ou empate),
    atualiza o placar global e oferece opções para jogar novamente ou sair.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout_base = FloatLayout()

        self.confetes = EfeitoConfete()
        self.layout_base.add_widget(self.confetes)

        main_box = BoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Fim de Jogo",
            elevation=0
        )
        self.toolbar.size_hint_y = None
        self.toolbar.height = dp(56)
        main_box.add_widget(self.toolbar)

        self.result_card = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
            size_hint=(1, None),
            height=dp(500),
            pos_hint={"center_x": 0.5}
        )

        self.result_icon = MDLabel(
            text=md_icons["trophy"],
            font_style="Icon",
            font_size="350sp",
            size_hint=(None, None),
            size=(dp(350), dp(350)),
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=[0.95, 0.75, 0.1, 1],
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        

        self.result_card.add_widget(BoxLayout(size_hint_y=1))
        self.result_card.add_widget(self.result_icon)
        self.result_card.add_widget(BoxLayout(size_hint_y=0.2))

        self.label_resultado = MDLabel(
            text=Textos.RESULTADO_VENCEU,
            halign="center",
            font_style="H4",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(60)
        )
        self.result_card.add_widget(self.label_resultado)
        
        self.label_placar = MDLabel(
            text=Textos.PLACAR_ZERADO,
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        self.result_card.add_widget(self.label_placar)

        main_box.add_widget(self.result_card)
        main_box.add_widget(BoxLayout(size_hint_y=1))


        btn_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(140),
            spacing=dp(10)
        )

        btn_nova = MDFillRoundFlatButton(
            text=Textos.BTN_NOVA_PARTIDA_RESULT,
            size_hint=(None, None),
            size=(dp(220), dp(50)),
            pos_hint={"center_x": 0.5},
            font_size="16sp",
            on_release=lambda x: setattr(self.manager, "current", "config")
        )
        btn_box.add_widget(btn_nova)

        btn_menu = MDFlatButton(
            text=Textos.BTN_MENU_RESULT,
            size_hint=(None, None),
            size=(dp(220), dp(48)),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "menu")
        )
        btn_box.add_widget(btn_menu)
        
        main_box.add_widget(btn_box)
        main_box.add_widget(BoxLayout(size_hint_y=0.1))

        self.layout_base.add_widget(main_box)
        self.add_widget(self.layout_base)

    def atualizar_icon_tema(self):
        app = MDApp.get_running_app()
        icon_name = app.get_tema_icon()
        self.toolbar.right_action_items = [[icon_name, lambda x: app._tema_e_atualiza()]]

    def on_enter(self):
        self.atualizar_icon_tema()
        MDApp.get_running_app()._forcar_atualizacao_textos(self)

    def mostrar_resultado(self, texto):
        """
        Configura o texto de vitória/empate, atualiza o placar 
        e dispara o efeito de confetes se não houver empate.
        
        Args:
            texto (str): O texto com o resultado final (ex: 'Jogador 1 venceu!').
        """
        self.label_resultado.text = texto
        app = MDApp.get_running_app()
        
        j1_nome = app.controller.game.jogadores[0].nome
        j2_nome = app.controller.game.jogadores[1].nome

        if "venceu!" in texto:
            nome_vencedor = texto.replace(" venceu!", "")
            if nome_vencedor == j1_nome:
                app.placar["j1"] += 1
            elif nome_vencedor == j2_nome:
                app.placar["j2"] += 1
                
            self.result_icon.text = md_icons["trophy"]
            self.result_icon.text_color = [0.95, 0.75, 0.1, 1]
            

            self.confetes.estourar()
        else:
            app.placar["empates"] += 1
            self.result_icon.text = md_icons["handshake"]
            self.result_icon.text_color = [0.4, 0.4, 0.4, 1]
            
        self.label_placar.text = f"{j1_nome} {app.placar['j1']} x {app.placar['j2']} {j2_nome}"
        app.salvar_placar()
            
        self.result_card.opacity = 0
        self.result_icon.font_size = dp(350)
        anim = Animation(opacity=1, duration=0.6)
        anim.start(self.result_card)
