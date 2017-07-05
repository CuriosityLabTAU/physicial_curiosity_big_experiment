from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.text import LabelBase
import time



#import text fonts

LabelBase.register(name = "dogs", fn_regular = "dogs.ttf" )
LabelBase.register(name = "welcome", fn_regular = "welcome.ttf" )
LabelBase.register(name = "regular", fn_regular = "regular.ttf" )

# declaration of forms
# connection to .kv file
class Config(BoxLayout):
    nao_ip = ObjectProperty()
    subject_id= ObjectProperty()


# the app definition
class TabletApp(App):
    def build(self):
        # connect internal instances of form classes
        self.config = Config()

        # defines the screen manager, moves between forms
        self.sm = ScreenManager()

        # connects each form to a screen
        screen = Screen(name='config')
        screen.add_widget(self.config)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        return self.sm


if __name__ == '__main__':
    TabletApp().run()