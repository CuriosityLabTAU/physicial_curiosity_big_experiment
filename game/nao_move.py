# -*- encoding: UTF-8 -*-

import sys
import almath
from naoqi import ALProxy
import rospy
import time


class NaoNode:

    def __init__(self):
        robotIP = '192.168.0.100'
        port = 9559

        try:
            self.motionProxy = ALProxy("ALMotion", robotIP, port)
            self.audioProxy = ALProxy("ALAudioPlayer", robotIP, port)
        except Exception,e:
            print "Could not create proxy to ALMotion"
            print "Error was: ",e
            sys.exit(1)

        # Get the Robot Configuration
        self.robotConfig = self.motionProxy.getRobotConfig()
        self.init_poses()
        self.init_utterances()

    def move_to_pose(self, pose):

        # Head     = [HeadYawAngle, HeadPitchAngle]
        #
        # LeftArm  = [ShoulderPitchAngle, +ShoulderRollAngle, +ElbowYawAngle, +ElbowRollAngle, WristYawAngle, HandAngle]
        # RightArm = [ShoulderPitchAngle, -ShoulderRollAngle, -ElbowYawAngle, -ElbowRollAngle, WristYawAngle, HandAngle]
        #
        # LeftLeg  = [0.0,                      #hipYawPitch
        #             spreadAngle,              #hipRoll
        #             -kneeAngle/2-torsoAngle,  #hipPitch
        #             kneeAngle,                #kneePitch
        #             -kneeAngle/2,             #anklePitch
        #             -spreadAngle]             #ankleRoll
        # RightLeg = [0.0, -spreadAngle, -kneeAngle/2-torsoAngle, kneeAngle, -kneeAngle/2,  spreadAngle]

        # # Gather the joints together
        # pTargetAngles = Head + LeftArm + LeftLeg + RightLeg + RightArm
        pTargetAngles = pose['head'] + pose['left_arm'] + pose['left_leg'] + pose['right_leg'] + pose['right_arm']

        # Convert to radians
        pTargetAngles = [ x * almath.TO_RAD for x in pTargetAngles]
        

        #------------------------------ send stiffness -----------------------------
        self.motionProxy.stiffnessInterpolation("Body", 1.0, 0.5)

        #------------------------------ send the commands -----------------------------
        # We use the "Body" name to signify the collection of all joints
        pNames = "Body"
        # We set the fraction of max speed
        pMaxSpeedFraction = 0.15
        # Ask motion to do this with a blocking call
        self.motionProxy.angleInterpolationWithSpeed(pNames, pTargetAngles, pMaxSpeedFraction)

    def init_poses(self):
        self.base_pose = {
            'head': [0,0],
            'left_arm': [+80,0,0,0,0,0],
            'right_arm': [+80,0,0,0,0,0],
            'left_leg': [0,0,0,0,0,0],
            'right_leg': [0,0,0,0,0,0]
        }
        
        self.pose_names = [
            "right_hand_up",
            "left_hand_up",
            "both_hands_up",
            "right_hand_down",
            "left_hand_down",
            "both_hands_down",
            "right_hand_forward",
            "left_hand_forward",
            "both_hands_forward",
            "right_hand_side",
            "left_hand_side",
            "both_hands_side"
          ]

        self.poses = {}
        for n in self.pose_names:
            self.poses[n] = {
                'head': [0,0],
                'left_arm': [+80,0,0,0,0,0],
                'right_arm': [+80,0,0,0,0,0],
                'left_leg': [0,0,0,0,0,0],
                'right_leg': [0,0,0,0,0,0]
            }
        
        self.poses['right_hand_up']['right_arm'][0] = -60
        
        self.poses['left_hand_up']['left_arm'][0] = -60
        
        self.poses['both_hands_up']['right_arm'][0] = -60
        self.poses['both_hands_up']['left_arm'][0] = -60
        #-----
        self.poses['right_hand_forward']['right_arm'][0] = 0
        self.poses['left_hand_forward']['left_arm'][0] = 0
        self.poses['both_hands_forward']['right_arm'][0] = 0
        self.poses['both_hands_forward']['left_arm'][0] = 0
        #----
        self.poses['right_hand_side']['right_arm'][0] = 0
        self.poses['right_hand_side']['right_arm'][1] = -60
        
        self.poses['left_hand_side']['left_arm'][0] = 0
        self.poses['left_hand_side']['left_arm'][1] = +60
        
        self.poses['both_hands_side']['right_arm'][0] = 0
        self.poses['both_hands_side']['right_arm'][1] = -60
        self.poses['both_hands_side']['left_arm'][0] = 0
        self.poses['both_hands_side']['left_arm'][1] = +60

    def play_file(self, filename=None):
        #plays a file and get the current position 5 seconds later
        # fileId = self.audioProxy.post.playFile("../audio_files/bye.wav")
        self.audioProxy.playFile('/home/nao/naoqi/wav/' + filename,1.0,0.0)

    def init_utterances(self):
        self.utterances = {
            'correct_pose': [
                'after Hertzel says+ currect child move OR after NO Hertzel says+ child not moved.wav',
                'after Hertzel says+ currect child move 2  OR after NO Hertzel says+ child not moved.wav',
                'after Hertzel says+ currect child move 3 OR after NO Hertzel says+ child not moved',
                'after Hertzel says+ currect child move 4 OR after NO Hertzel says+ child not moved'
            ],
            'got you': [
                'after NO Hertzel says+ child move.wav'
            ],
            'didnt get it': [
                'after Hertzel says+ wrong child move.wav',
                'after Hertzel says+ wrong child move 2.wav',
                'after Hertzel says+ wrong child move 3.wav',
                'after Hertzel says+ wrong child move 4.wav'
            ],
            #'good job': [
            #    'after Hertzel says+ currect child move OR after NO Hertzel says+ child not moved.wav',
            #    'after Hertzel says+ currect child move 2  OR after NO Hertzel says+ child not moved.wav',
            #    'after Hertzel says+ currect child move 3 OR after NO Hertzel says+ child not moved',
            #    'after Hertzel says+ currect child move 4 OR after NO Hertzel says+ child not moved'
            #]
            'good job': [
                'after NO Hertzel says+ child move.wav',
                'after NO Hertzel says+ child move.wav',
                'after NO Hertzel says+ child move.wav',
                'after NO Hertzel says+ child move.wav'
            ]
        }