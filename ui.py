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
import rospy
from std_msgs.msg import String
import threading
import json
from random import shuffle, sample

the_matrices = range(0, 7)
exp_flow = [
    {
        'behavior_before': None,
        'time': 60,
        'behavior_after': 'introduction'
    },
    {
        'behavior_before': 'explain_experiment',
        'time': 60,
        'behavior_after': None
    },
    {
        'behavior_before': 'confused_again_1',
        'time': 60,
        'behavior_after': None
    },
    {
        'behavior_before': 'confused_again_2',
        'time': 60,
        'behavior_after': None
    },
    {
        'behavior_before': 'confused_again_3',
        'time': 60,
        'behavior_after': None
    },
    {
        'behavior_before': 'confused_again_4',
        'time': 60,
        'behavior_after': None
    },
    {
        'behavior_before': 'confused_again_5',
        'time': 60,
        'behavior_after': None
    }
]

tasks = [
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    },
    {
        'behavior_before': 'explain_task',
        'time': 30,
        'behavior_after': 'good_job'
    }

]

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
    kinect_status_id = ObjectProperty()


# the app definition
class ExperimentApp(App):
    subject_id = 0
    nao_ip = '192.168.0.104'
    state = 0
    proceed = False

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

    def update_tracking(self, data):
        self.experiment_screen.ids['kinect_status_id'].text = data.data

    def goto_experiment_screen(self,subject_id,nao_ip):#go to experiment screen
        print subject_id
        print nao_ip
        self.subject_id = subject_id
        self.nao_ip = nao_ip
        t1 = threading.Thread(target=self.run_main)
        t1.start()

        threading._sleep(1.0)
        rospy.init_node('ui_node')
        rospy.Subscriber("tracking", String, self.update_tracking)
        self.flow = rospy.Publisher ('the_flow', String, queue_size=10)
        self.nao = rospy.Publisher('to_nao', String, queue_size=10)
        rospy.Subscriber("nao_state", String, self.parse_nao_state)

        threading._sleep(0.2)
        self.nao.publish('{\"action\": \"wake_up\"}')

        # subprocess.call(['python main_nao.py '+subject_id+" "+nao_ip])

        # set the current_subject matrices
        self.matrices = the_matrices
        shuffle(self.matrices)

        self.sm.current="experiment_screen"

    def run_main(self):
        os.system('python main_nao.py ' + self.subject_id + ' ' + self.nao_ip)

    def parse_nao_state(self, data):
        try:
            message = json.loads(data.data)
            if 'name' in message:
                self.proceed = True
        except:
            print('nao_state not a json: ', data.data)


    def epoch(self, behavior_before=None, time=-1, matrix=None, behavior_after=None, tasks=None):
        # task: {'behavior_before', 'time'}

        # learning round
        print('-- learning round: ', behavior_before, time, matrix, behavior_after)
        self.round(behavior_before=behavior_before, time=time, matrix=matrix, behavior_after=behavior_after)

        if tasks:
            for task in tasks:
                print('-- task round: ', behavior_before, time, matrix, behavior_after)
                self.round(behavior_before=task['behavior_before'], time=task['time'], matrix=matrix, behavior_after=task['behavior_after'])


    def round(self, behavior_before=None, time=-1, matrix=None, behavior_after=None):
        self.proceed = True
        if behavior_before:
            # publish directly to nao_ros
            robot_str = '{\"name\": \"behavior_before\", \"action\" : \"run_behavior\", \"parameters\" : [\"' + behavior_before + '\", \"wait\"]}'
            self.nao.publish(robot_str)
            self.proceed = False

        while(not self.proceed):
            pass

        if time >= 0:      # run epoch with matrix
            self.start()
            self.flow.publish(str(matrix))
            Clock.schedule_once(self.stop, time)

        while(not self.proceed):
            pass

        if behavior_before:
            # publish directly to nao_ros
            robot_str = '{\"name\": \"behavior_after\", \"action\" : \"run_behavior\", \"parameters\" : [\"' + behavior_after + '\", \"wait\"]}'
            self.nao.publish(robot_str)
            self.proceed = False

        while(not self.proceed):
            pass



    def start(self):
        self.flow.publish('start')
        self.proceed = False

    def stop(self, dt):
        self.flow.publish('stop')
        self.proceed = True

    def the_end(self):
        self.stop()
        self.flow.publish('the end')

    def next_epoch(self):
        print('=== next ===')
        current_tasks = sample(tasks, 3)
        self.epoch(behavior_before=exp_flow[self.state]['behavior_before'],
                   time=exp_flow[self.state]['time'],
                   matrix=self.matrices[self.state],
                   behavior_after=exp_flow[self.state]['behavior_after'],
                   tasks=current_tasks
                   )
        self.state += 1

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
    # node = UI_Node()
    # node.run_experiment()