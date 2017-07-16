

###


from naoqi import ALProxy
import sys
import almath
import json
import time
import argparse

port = 9559
robotIP = '192.168.0.103'
anim=ALProxy("ALAnimatedSpeech",robotIP,port)
cong={"bodyLnguageMde":"contextual"}
tts = ALProxy("ALTextToSpeech", robotIP, 9559)

tts.setParameter("speed", 90)


anim.say("Hi hello! I'm a robot that moving my hands following the movements of your hands.I usually know how to imitate those in front of me, but today I got confused and I do not recognize your hands very well. Can you help me control my body? I'll give you now three tasks, and for each of them you'll have 15 seconds, will you be successful?", cong)


anim.say("You have 30 seconds \\ pau=1000 \\ to perform this task", cong)

anim.say("Oh, I'm so unfocused, I got confused again. You're very good at it, maybe we'll do it again? Take a minute to understand how I got confused this time and then I will ask you to do more tasks", cong)

anim.say("You are so good at understanding how I move, do you want a challenge? Now you can move me any way you want for 2 minutes, at the end of the two minutes you will not have any tasks. Can you understand how am I programmed to move? If you do not want to, you can stop here", cong)

anim.say("I had a lot of fun with you today, you were really good. I'd love you to come visit me again", cong)

anim.say("Come on, start", cong)


