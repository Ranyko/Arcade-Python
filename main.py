from kivy.config import Config
Config.set('graphics', 'width',     '400')
Config.set('graphics', 'height',    '711')
Config.set('graphics', 'resizable', '0')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from app.controllers.game_controller import GameController
from app.views.menu_screen       import MenuScreen
from app.views.game_select_screen import GameSelectScreen
from app.views.config_screen     import ConfigScreen
from app.views.board_screen      import BoardScreen
from app.views.result_screen     import ResultScreen


class TabuleiroApp(MDApp):

    def __init__(self):
        super().__init__()
        self.placar = None
        self.cor_j2 = None
        self.tipo_jogo = None
        self.cor_j1 = None
        self.controller = None

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        self.controller = GameController()
        self.cor_j1     = [0.25, 0.55, 0.95, 1]
        self.cor_j2     = [0.92, 0.25, 0.25, 1]


        self.placar = self._carregar_placar()

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameSelectScreen(name="select"))
        sm.add_widget(ConfigScreen(name="config"))
        sm.add_widget(BoardScreen(name="board"))
        sm.add_widget(ResultScreen(name="result"))
        return sm

    def alternar_tema(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def get_tema_icon(self):
        return "weather-night" if self.theme_cls.theme_style == "Light" else "weather-sunny"

    def tema_action_item(self):
        return [self.get_tema_icon(), lambda x: self._tema_e_atualiza()]

    def _tema_e_atualiza(self):
        self.alternar_tema()
        for screen_name in ["menu", "select", "config", "board", "result"]:
            scr = self.root.get_screen(screen_name)
            if hasattr(scr, 'atualizar_icon_tema'):
                scr.atualizar_icon_tema()
        self._forcar_atualizacao_textos(self.root)

    def _forcar_atualizacao_textos(self, widget):
        from kivymd.uix.label import MDLabel
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.card import MDCard
        
        is_dark = self.theme_cls.theme_style == "Dark"

        if isinstance(widget, MDLabel):
            if widget.theme_text_color == "Primary":
                widget.theme_text_color = "Custom"
                widget.theme_text_color = "Primary"
            elif widget.theme_text_color == "Secondary":
                widget.theme_text_color = "Custom"
                widget.theme_text_color = "Secondary"
        elif isinstance(widget, MDTextField):
            c_text = [1, 1, 1, 1] if is_dark else [0, 0, 0, 1]
            c_hint = [0.7, 0.7, 0.7, 1] if is_dark else [0.4, 0.4, 0.4, 1]
            widget.text_color_normal = c_text
            widget.text_color_focus = c_text
            widget.hint_text_color_normal = c_hint
            widget.hint_text_color_focus = c_hint
            
        elif isinstance(widget, MDCard):
            if getattr(widget, "atualiza_bg_automatico", False):
                widget.md_bg_color = [0.15, 0.15, 0.15, 1] if is_dark else [1, 1, 1, 1]

        for child in widget.children:
            self._forcar_atualizacao_textos(child)

    def _carregar_placar(self):
        import json, os
        if os.path.exists("placar.json"):
            try:
                with open("placar.json", "r") as f:
                    return json.load(f)
            except:
                pass
        return {"j1": 0, "j2": 0, "empates": 0}

    def salvar_placar(self):
        import json
        try:
            with open("placar.json", "w") as f:
                json.dump(self.placar, f)
        except:
            pass


if __name__ == "__main__":
    TabuleiroApp().run()
