import rospy
from std_msgs.msg import String
import time
import Tkinter
import sys


class Experiment(Tkinter.Tk):

    def __init__(self, parent, subject_id):
        self.flow = rospy.Publisher ('the_flow', String)
        self.matrix_names = ['basic', 'mirror', 'LShoulderPitch-RShoulderRoll', 'LShoulderRoll-RShoulderPitch']

        self.exp_running = False
        self.subject_id = subject_id
        self.state = 0

        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        rospy.init_node('experiment')
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)


        button1 = Tkinter.Button(self,text=u"   Next -->  ",
                                 command=self.next,fg = "blue",
                                 font="Arial 10 bold",
                                 height = 20, width = 20)

        button1.grid(column=0,row=0)

        button2 = Tkinter.Button(self,text=u"    The end   ",
                                 fg='red',
                                 font="Arial 10 bold",
                                 command=self.the_end,
                                 height = 4, width = 20)
        button2.grid(column=0,row=2)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def next(self):
        print(self.state)
        if self.state == 0:     # learn the basics
            self.set_matrix('basic')
            self.start()
            time.sleep(60)
            self.stop()
            self.state = 1
        elif self.state == 1:   # THE EXPERIMENT
            which_matrix = int(self.subject_id) % 2
            if which_matrix == 0:
                self.set_matrix('LShoulderPitch-RShoulderRoll')
            else:
                self.set_matrix('LShoulderRoll-RShoulderPitch')
            self.start()
            time.sleep(60)
            self.stop()
            self.state = 2
        elif self.state == 2:   # the tasks
            which_matrix = int(self.subject_id) % 2
            if which_matrix == 0:
                self.set_matrix('LShoulderPitch-RShoulderRoll')
            else:
                self.set_matrix('LShoulderRoll-RShoulderPitch')
            self.start()
            time.sleep(30)
            self.stop()
            self.state = 3
        elif self.state == 3:  # the tasks
            which_matrix = int(self.subject_id) % 2
            if which_matrix == 0:
                self.set_matrix('LShoulderPitch-RShoulderRoll')
            else:
                self.set_matrix('LShoulderRoll-RShoulderPitch')
            self.start()
            time.sleep(30)
            self.stop()
            self.state = 4
        elif self.state == 4:  # the tasks
            which_matrix = int(self.subject_id) % 2
            if which_matrix == 0:
                self.set_matrix('LShoulderPitch-RShoulderRoll')
            else:
                self.set_matrix('LShoulderRoll-RShoulderPitch')
            self.start()
            time.sleep(30)
            self.stop()
            self.state = 5

    def the_end(self):
        self.stop()
        self.flow.publish('the end')

    def start_experiment(self):
        self.start()
        time.sleep(60)
        self.stop()

    def set_matrix(self, which_matrix):
        self.flow.publish(which_matrix)

    def stop(self):
        self.flow.publish('stop')

    def start(self):
        self.flow.publish('start')

app = Experiment(None, int(sys.argv[1]))
print sys.argv
app.title('Experiment')
app.mainloop()

