import rospy
from std_msgs.msg import String
from naoqi import ALProxy
import sys
import almath
import time
import datetime


class NaoNode():
    def __init__(self):
        self.robotIP = '192.168.0.104'
        self.port = 9559

        try:
            self.motionProxy = ALProxy("ALMotion", self.robotIP, self.port)
            self.audioProxy = ALProxy("ALAudioPlayer", self.robotIP, self.port)
            self.postureProxy = ALProxy("ALRobotPosture", self.robotIP, self.port)
        except Exception,e:
            print "Could not create proxy to ALMotion"
            print "Error was: ",e
            sys.exit(1)

        # Get the Robot Configuration
        self.robotConfig = self.motionProxy.getRobotConfig()
        self.motionProxy.setStiffnesses("Body", 1.0)
        self.postureProxy.goToPosture("StandInit", 0.5)
        self.motionProxy.setCollisionProtectionEnabled('Arms', True)
        self.motionProxy.post.angleInterpolationWithSpeed(['HeadPitch'], [-0.5], 0.2)

        # self.motionProxy.rest()

        self.communicating = False
        self.nao_movements = rospy.Publisher ('nao_movements', String)
        self.robot_running = True

        self.counter=0

    def start(self):
        #init a listener to kinect and
        rospy.init_node('nao_listener')
        rospy.Subscriber('nao_commands', String, self.callback)
        rospy.Subscriber("the_flow", String, self.the_end)
        rospy.spin()

    def the_end(self, data):
        if 'the end' in data.data:
            self.motionProxy.rest()
            self.robot_running = False

    def callback(self, data):
        print('got message')
        if not self.communicating and self.robot_running:
            if self.counter%15==0:
                self.communicating = True

                # data = 'name1, name2;target1, target2;pMaxSpeedFraction'
                data_str = data.data
                info = data_str.split(';')
                pNames = info[0].split(',')
                pTargetAngles = [float(x) for x in info[1].split(',')]
                # print motionProxy.rest()pTargetAngles

                pMaxSpeedFraction = float(info[2])
                # print(pNames, pTargetAngles, pMaxSpeedFraction)
                # self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)
                print('---------------------------------------------------')
                print(datetime.datetime.now())
                self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)
                print(datetime.datetime.now())
                print(self.counter, ' #################### nao_ros ################### moved robot')
                self.nao_movements.publish(data_str)
                # time.sleep(0.5)
                self.communicating = False

            self.counter+=1



    # def callback(self, data):
    #     # data = 'name1, name2;target1, target2;pMaxSpeedFraction'
    #     data_str = data.data
    #     info = data_str.split(';')
    #     pNames = info[0].split(',')
    #     pTargetAngles = [float(x) for x in info[1].split(',')]
    #     # print pTargetAngles
    #     # pTargetAngles = [ x * almath.TO_RAD for x in pTargetAngles]             # Convert to radians
    #
    #     pMaxSpeedFraction = float(info[2])
    #
    #     self.communicating = True
    #     self.motionProxy.setCollisionProtectionEnabled('Arms', True)
    #     while time.gmtime()[5]%2 == 0:
    #         self.motionProxy.post.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)
    #         print(' #################### nao_ros ################### moved robot')
    #         self.communicating = False


nao = NaoNode()
nao.start()