import rospy
from std_msgs.msg import String
import numpy as np
import random


class AngleMatrix:

    def __init__(self):
        self.pNames = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll',
                       'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll']

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

        self.base_matrices['LShoulderPitch-RShoulderRoll'] = self.switch_angles('LShoulderPitch', 'RShoulderRoll')
        self.base_matrices['LShoulderRoll-RShoulderPitch'] = self.switch_angles('LShoulderRoll', 'RShoulderPitch')
        
        self.matrix = random.choice(self.base_matrices['basic'] )
        print(self.matrix, type(self.matrix))
        self.skeleton_angles = np.zeros([8])
        self.robot_angles = np.zeros([8])

        self.pub = rospy.Publisher ('nao_commands', String)
        self.log = rospy.Publisher ('experiment_log', String)

        self.exp_running = False

    def start(self):
        #init a listener to kinect angles
        rospy.init_node('angle_matrix')
        rospy.Subscriber("skeleton_angles", String, self.callback)
        rospy.Subscriber("the_flow", String, self.flow_handling)
        rospy.spin()

    def flow_handling(self, data):
        print('angle_matrix', data.data)
        if 'stop' in data.data:
            self.exp_running = False
        elif 'start' in data.data:
            self.exp_running = True
        elif 'the end' not in data.data:
            self.matrix = self.base_matrices[data.data]
            self.log.publish(str(self.matrix))


    def callback(self, data):
        if self.exp_running:
            self.skeleton_angles = np.array([float(x) for x in data.data.split(',')])

            self.calculate_robot_angles()

            self.transmit_robot_angles()

    def calculate_robot_angles(self):
        self.robot_angles = np.dot(self.matrix, self.skeleton_angles)
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
        robot_str = ''
        for name in self.pNames:
            robot_str += name + ','
        robot_str = robot_str[:-1] + ';'

        for ang in self.robot_angles:
            robot_str += str(ang) + ','
        robot_str = robot_str[:-1] + ';'
        robot_str += '0.4'
        self.pub.publish(robot_str)
        # print('*************** angle_matrix ************ published: ', robot_str)

    def switch_angles(self, angle_name_0, angle_name_1):
        matrix = np.eye(8)
        angle_0 = self.pNames.index(angle_name_0)
        angle_1 = self.pNames.index(angle_name_1)
        matrix[angle_0, angle_0] = 0
        matrix[angle_1, angle_1] = 0
        matrix[angle_0, angle_1] = 1
        matrix[angle_1, angle_0] = 1
        return matrix

angle_matrix = AngleMatrix()
angle_matrix.start()