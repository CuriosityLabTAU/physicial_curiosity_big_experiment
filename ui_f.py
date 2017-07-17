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
import sys
import datetime


num_of_matrix=8
the_matrices = range(0, num_of_matrix)

exp_flow = [
    #step 0
    {
        'behavior_before': None,
        'time': 5.0,
        'behavior_after': 'physical_curiosity/stand_init',
        'tasks':False
    },
    #step 1
    {
        'behavior_before': 'physical_curiosity/f/opening',
        'time': -1,
        'behavior_after': None,
        'tasks':True,
        'use_matrix':0
    },
    #step 2
    {
        'behavior_before': 'physical_curiosity/f/confused1',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 3
    {
        'behavior_before': 'physical_curiosity/f/break1',
        'time': -1,
        'behavior_after': None,
        'tasks': False,
        'use_matrix': False
    },
    #step 4
    {
        'behavior_before': 'physical_curiosity/f/confused2',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 5
    {
        'behavior_before': 'physical_curiosity/f/confused3',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 6
    {
        'behavior_before': 'physical_curiosity/f/break2.1',
        'time': 120.0,
        'behavior_after': 'physical_curiosity/f/break2.2',
        'tasks': False,
        'use_matrix': False

    },
    #step 7
    {
        'behavior_before': 'physical_curiosity/f/confused2',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 8
    {
        'behavior_before': 'physical_curiosity/f/confused3',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 9
    {
        'behavior_before': 'physical_curiosity/f/break3',
        'time': -1,
        'behavior_after': None,
        'tasks': False,
        'use_matrix': False
    },
    #step 10
    {
        'behavior_before': 'physical_curiosity/f/confused2',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 11
    {
        'behavior_before': 'physical_curiosity/f/confused3',
        'time': 60.0,
        'behavior_after': None,
        'tasks': True
    },
    #step 12
    {
        'behavior_before': 'physical_curiosity/f/end_task',
        'time': 120.0,
        'behavior_after': None,
        'tasks': False
    },
    #step 13
    {
        'behavior_before': 'physical_curiosity/f/end_part_a',
        'time': -1,
        'behavior_after': None,
        'tasks': False,
        'use_matrix': False
    },
]

tasks = [
    {
        'behavior_before': 'physical_curiosity/tasks/f/two_hands_up',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/well_done'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/two_hands_forward',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/nice'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/two_hands_down',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/wow'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/two_hands_to_the_side',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/stand_init'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_up_left_hand_down',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/stand_init'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_up_left_hand_forward',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/stand_init'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_up_left_hand_to_the_side',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/well_done'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_forward_left_hand_down',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/nice'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_forward_left_hand_side',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/wow'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_to_the_side_left_hand_down',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/stand_init'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_to_the_side_left_hand_forward',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/stand_init'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_down_left_hand_to_the_side',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/stand_init'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/right_hand_down_left_hand_forward',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/well_done'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/left_hand_up_right_hand_down',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/nice'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/left_hand_up_right_hand_forward',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/tasks/wow'
    },
    {
        'behavior_before': 'physical_curiosity/tasks/f/left_hand_up_right_hand_to_the_side',
        'time': 15.0,
        'behavior_after': 'physical_curiosity/stand_init'
    }
]

# declaration of forms
# connection to .kv file
class Config(BoxLayout):
    pass
    # nao_ip = ObjectProperty()
    # subject_id= ObjectProperty()


class Experiment_screen(BoxLayout):
    kinect_status_id = ObjectProperty()
    state_text_input = ObjectProperty()
    next_button = ObjectProperty()
    timer=ObjectProperty()


# the app definition
class ExperimentApp(App):
    subject_id = 0
    nao_ip = '192.168.0.103'
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
        self.log = rospy.Publisher("experiment_log", String, queue_size=10)
        rospy.Subscriber("nao_state", String, self.parse_nao_state)


        threading._sleep(3.0)
        self.nao.publish('{\"action\": \"run_behavior\", \"parameters\": [\"dialog_posture/bhv_stand_up\"]}')
        threading._sleep(1.0)

        # set the current_subject matrices
        self.matrices = the_matrices
        shuffle(self.matrices)
        self.matrix_for_state = {}
        current_index=0
        for stage_no in range(len(exp_flow)):
            if "use_matrix" in exp_flow[stage_no] and exp_flow[stage_no]["use_matrix"]is False:
                print stage_no
                self.matrix_for_state[stage_no]=None
            elif "use_matrix" in exp_flow[stage_no] and type(exp_flow[stage_no]["use_matrix"]) is int:
                self.matrix_for_state[stage_no]=self.matrices[exp_flow[stage_no]["use_matrix"]]
            else:
                if current_index < len(self.matrices):
                    self.matrix_for_state[stage_no] =self.matrices[current_index]
                    current_index+=1
                else:
                    self.matrix_for_state[stage_no] = current_index
        print self.matrix_for_state

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
        self.log.publish("state %d, learning_round" % self.state)
        self.round(behavior_before=behavior_before, time=time, matrix=matrix, behavior_after=behavior_after)
        print "------tasks---------"
        if tasks:
            for i, task in enumerate(tasks):
                print('-- task round: ', behavior_before, time, matrix, behavior_after)
                self.log.publish("state %d, task: %d, %s" % (self.state, i, task['behavior_before']))
                self.round(behavior_before=task['behavior_before'], time=task['time'], matrix=matrix, behavior_after=task['behavior_after'])


    def round(self, behavior_before=None, time=-1, matrix=None, behavior_after=None):
        self.proceed = True
        if behavior_before:
            # publish directly to nao_ros
            robot_str = '{\"name\": \"behavior_before\", \"action\" : \"run_behavior\", \"parameters\" : [\"' + behavior_before + '\", \"wait\"]}'
            self.nao.publish(robot_str)
            self.proceed = False

        while not self.proceed:
            pass

        if time >= 0 and matrix is not None:      # run epoch with matrix
            self.delta = datetime.datetime.now()+datetime.timedelta(0, time)
            Clock.schedule_interval(self.update_timer, 0.05)


            self.exp_start()
            self.flow.publish(str(matrix))
            threading._sleep(time)

            Clock.unschedule(self.update_timer)
            self.experiment_screen.ids['timer'].text = str("00:00")

            self.exp_stop()

        if time >= 0 and matrix is None:
            self.delta = datetime.datetime.now()+datetime.timedelta(0, time)
            Clock.schedule_interval(self.update_timer, 0.05)

            self.experiment_screen.ids['timer'].text = str(time)
            threading._sleep(time)

            Clock.unschedule(self.update_timer)
            self.experiment_screen.ids['timer'].text = str("00:00")

        if behavior_after:
            # publish directly to nao_ros
            robot_str = '{\"name\": \"behavior_after\", \"action\" : \"run_behavior\", \"parameters\" : [\"' + behavior_after + '\", \"wait\"]}'
            self.nao.publish(robot_str)
            self.proceed = False

        while not self.proceed:
            pass

    def exp_start(self):
        self.flow.publish('start')
        self.proceed = False

    def exp_stop(self):
        print('---stop---')
        self.flow.publish('stop')
        self.proceed = True

    def the_end(self):
        self.exp_stop()
        self.flow.publish('the end')

    def next_epoch(self):
        self.experiment_screen.ids['next_button'].disabled = True
        threading.Thread(target=self.epoch_thread).start()

    def epoch_thread(self):
        print('=== next ===')

        self.state = int(self.experiment_screen.ids['state_text_input'].text)
        self.log.publish("current_state: %d" % self.state)
        if exp_flow[self.state]['tasks']:
            current_tasks = sample(tasks, 3)
        else:
            current_tasks = None

        self.epoch(behavior_before=exp_flow[self.state]['behavior_before'],
                   time=exp_flow[self.state]['time'],
                   matrix=self.matrix_for_state[self.state],
                   behavior_after=exp_flow[self.state]['behavior_after'],
                   tasks=current_tasks
                   )

        self.state += 1
        self.experiment_screen.ids['state_text_input'].text = str(self.state)
        self.experiment_screen.ids['next_button'].disabled = False



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

    def exit_experiment(self):
        self.nao.publish('{\"action\" : \"rest\"}')

    def update_timer(self, kt):
        delta = self.delta - datetime.datetime.now()
        minutes, seconds = str(delta).split(":")[1:]
        seconds = seconds[:5]
        self.experiment_screen.ids['timer'].text = str(minutes+':'+seconds)

if __name__ == '__main__':
    ExperimentApp().run()
