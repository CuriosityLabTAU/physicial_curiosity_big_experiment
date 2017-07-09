

###


from naoqi import ALProxy
import sys
import almath
import json
import time
import argparse

port = 9559
robotIP = '192.168.0.100'
anim=ALProxy("ALAnimatedSpeech",robotIP,port)
cong={"bodyLnguageMde":"contextual"}


anim.say("Thank you very mauch  for your help! I an Matan and I will be here to help you", cong)