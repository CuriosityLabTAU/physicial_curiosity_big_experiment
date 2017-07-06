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
import os
import threading

import subprocess


#import text fonts

# LabelBase.register(name = "dogs", fn_regular = "dogs.ttf" )
# LabelBase.register(name = "welcome", fn_regular = "welcome.ttf" )
# LabelBase.register(name = "regular", fn_regular = "regular.ttf" )

# declaration of forms
# connection to .kv file
class Config(BoxLayout):
    pass
    # nao_ip = ObjectProperty()
    # subject_id= ObjectProperty()

class Experiment_screen(BoxLayout):
    pass


# the app definition
class ExperimentApp(App):
    subject_id = 0
    nao_ip = '192.168.0.104'

    def build(self):
        # connect internal instances of form classes
        self.config = Config()
        self.experiment_screen = Experiment_screen()

        # defines the screen manager, moves between forms
        self.sm = ScreenManager()

        # connects each form to a screen
        screen = Screen(name='config')
        screen.add_widget(self.config)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        screen = Screen(name='experiment_screen')
        screen.add_widget(self.experiment_screen)
        Window.clearcolor = (1, 1, 1, 1)
        self.sm.add_widget(screen)

        return self.sm

    def goto_experiment_screen(self,subject_id,nao_ip):#go to experiment screen
        print subject_id
        print nao_ip
        self.subject_id = subject_id
        self.nao_ip = nao_ip
        t1 = threading.Thread(target=self.run_main)
        t1.start()
        # subprocess.call(['python main_nao.py '+subject_id+" "+nao_ip])
        self.sm.current="experiment_screen"

    def run_main(self):
        os.system('python main_nao.py ' + self.subject_id + ' ' + self.nao_ip)





    def btn_released(self,btn,func,param1=None,param2=None):#button configuration
        btn.background_coler=(1,1,1,1)
        if param1 is not None:
            func_param1=param1.text
            if param2 is not None:
                func_param2 = param2.text
                func(func_param1,func_param2)
            else:
                func(func_param1)
        else:
            func()

if __name__ == '__main__':
    ExperimentApp().run()