

###


from naoqi import ALProxy
import sys
import almath
import json
import time
import argparse

port = 9559
robotIP = '192.168.0.104'
anim=ALProxy("ALAnimatedSpeech",robotIP,port)
cong={"bodyLnguageMde":"contextual"}


anim.say("Hello, I'm a robot that moves my hands following the gestures you make, but today I was confused and I have trouble recognizing your movements. Can you try to help me control my body", cong)


anim.say("You have 30 seconds \\ pau=1000 \\ to perform this task", cong)

anim.say("Oh, I'm so unfocused, I got confused again. You're very good at it, maybe we'll do it again? Take a minute to understand how I got confused this time and then I will ask you to do more tasks", cong)

anim.say("You are so good at understanding how I move, do you want a challenge? Now you can move me any way you want for 2 minutes, at the end of the two minutes you will not have any tasks. Can you understand how am I programmed to move? If you do not want to, you can stop here", cong)

anim.say("I had a lot of fun with you today, you were really good. I'd love you to come visit me again", cong)

anim.say("Can you make me be with both hands sideways", cong)
