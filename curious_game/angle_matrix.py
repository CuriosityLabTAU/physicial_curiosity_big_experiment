import rospy
from std_msgs.msg import String
import numpy as np
import random
import copy

class AngleMatrix:

    def __init__(self):
        self.pNames = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll',
                       'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll']

        self.set_base_matrices()
        
        self.matrix = random.choice(self.base_matrices['basic'] )

        self.skeleton_angles = np.zeros([8])
        self.robot_angles = np.zeros([8])

        self.pub = rospy.Publisher ('to_nao', String, queue_size=10)
        self.log = rospy.Publisher ('experiment_log', String, queue_size=10)

        self.exp_running = False

        self.msg_counter = 0

    def set_base_matrices(self):
        self.base_matrices = {}
        self.base_matrices['basic'] = np.eye(8)

        self.base_matrices['mirror'] = np.eye(8)
        self.base_matrices['mirror'][0,0] = 0
        self.base_matrices['mirror'][4,4] = 0
        self.base_matrices['mirror'][0,4] = 1
        self.base_matrices['mirror'][4,0] = 1
        self.base_matrices['mirror'][1,1] = 0
        self.base_matrices['mirror'][5,5] = 0
        self.base_matrices['mirror'][1,5] = -1
        self.base_matrices['mirror'][5,1] = -1

        # self.base_matrices[0] = self.switch_angles([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

        self.base_matrices[0] = self.switch_angles([[-1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]])

        self.base_matrices[1] = self.switch_angles([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]])

        self.base_matrices[2] = self.switch_angles([[0,0,-1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])

        self.base_matrices[3] = self.switch_angles([[0,0,0,1],[0,1,0,0],[1,0,0,0],[0,0,0,1]])

        self.base_matrices[4] = self.switch_angles([[1,0,0,0],[0,0,1,0],[0,0,1,0],[0,0,0,1]])

        self.base_matrices[5] = self.switch_angles([[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])

        self.base_matrices[6] = self.switch_angles([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])

        self.base_matrices[7] = self.switch_angles([[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]])

        self.base_matrices[8] = self.switch_angles([[0.5,0,-0.5,0],[0,1,0,0],[-0.5,0,0.5,0],[0,0,0,1]])


        # self.base_matrices[1] = self.switch_angles('LShoulderRoll', 'RShoulderPitch')
        #
        # self.base_matrices[2] = self.switch_angles('LShoulderPitch', 'LShoulderRoll')
        # self.base_matrices[3] = self.switch_angles('RShoulderPitch', 'RShoulderRoll')
        #
        # self.base_matrices[4] = self.switch_angles('LShoulderPitch', 'RShoulderRoll')
        # self.base_matrices[5] = self.switch_angles('LShoulderRoll', 'RShoulderPitch')
        #
        # self.base_matrices[6] = self.switch_angles('LShoulderPitch', 'LShoulderRoll')
        # self.base_matrices[7] = self.switch_angles('RShoulderPitch', 'RShoulderRoll')

    def start(self):
        #init a listener to kinect angles
        rospy.init_node('angle_matrix')
        rospy.Subscriber("skeleton_angles", String, self.callback)
        rospy.Subscriber("the_flow", String, self.flow_handling)
        rospy.spin()

    def flow_handling(self, data):
        if 'stop' in data.data:
            self.exp_running = False
        elif 'start' in data.data:
            self.exp_running = True
        elif 'the end' not in data.data: # got a real matrix
            self.matrix = self.base_matrices[int(data.data)]
            self.log.publish("matrix: " + str(self.matrix))

    def callback(self, data):
        if self.exp_running:
            self.skeleton_angles = np.array([float(x) for x in data.data.split(',')])

            self.calculate_robot_angles()

            self.transmit_robot_angles()

    def calculate_robot_angles(self):
        self.robot_angles = np.dot(self.matrix, self.skeleton_angles)
        #mirror
        robot_angles_org=copy.deepcopy(self.robot_angles)
        self.robot_angles[0]=robot_angles_org[4]
        self.robot_angles[1]=-robot_angles_org[5]
        self.robot_angles[4]=robot_angles_org[0]
        self.robot_angles[5]=-robot_angles_org[1]
        # safety!
        self.robot_angles[0] = np.maximum(self.robot_angles[0],-2.0850)
        self.robot_angles[0] = np.minimum(self.robot_angles[0], 2.0850)

        self.robot_angles[1] = np.maximum(self.robot_angles[1],-0.3140)
        self.robot_angles[1] = np.minimum(self.robot_angles[1], 1.3260)

        self.robot_angles[2] = np.maximum(self.robot_angles[2],-2.0850)
        self.robot_angles[2] = np.minimum(self.robot_angles[2], 2.0850)

        self.robot_angles[3] = np.maximum(self.robot_angles[3],-1.5440)
        self.robot_angles[3] = np.minimum(self.robot_angles[3],-0.0340)

        self.robot_angles[4] = np.maximum(self.robot_angles[4],-2.0850)
        self.robot_angles[4] = np.minimum(self.robot_angles[4], 2.0850)

        self.robot_angles[5] = np.maximum(self.robot_angles[5],-1.3260)
        self.robot_angles[5] = np.minimum(self.robot_angles[5], 0.3140)

        self.robot_angles[6] = np.maximum(self.robot_angles[6],-2.0850)
        self.robot_angles[6] = np.minimum(self.robot_angles[6], 2.0850)

        self.robot_angles[7] = np.maximum(self.robot_angles[7],0.0340)
        self.robot_angles[7] = np.minimum(self.robot_angles[7],1.5440)

    def transmit_robot_angles(self):
        robot_str = '{\"action\": \"change_pose\", \"parameters\": \"\\\"'
        for name in self.pNames:
            robot_str += name + ','
        robot_str = robot_str[:-1] + ';'

        for ang in self.robot_angles:
            robot_str += str(ang) + ','
        robot_str = robot_str[:-1] + ';'
        robot_str += '0.4'
        robot_str += '\\\"\"}'


        self.msg_counter += 1
        if self.msg_counter % 14 == 0:
            self.pub.publish(robot_str)

    def switch_angles(self,mat=[[],[],[],[]]):
        matrix = np.eye(8)
        mat=mat
        for row in range(4):
            for index in range(4):
                matrix[(row/2)*2 + row,(index/2)*2 + index]= mat[row][index]
        return matrix


angle_matrix = AngleMatrix()
angle_matrix.start()