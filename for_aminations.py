

###


from naoqi import ALProxy

port = 9559
robotIP = '192.168.0.100'
anim=ALProxy("ALAnimatedSpeech",robotIP,port)
cong={"bodyLnguageMde":"contextual"}
tts = ALProxy("ALTextToSpeech", robotIP, 9559)

tts.setParameter("speed", 80)


anim.say("Hi hello! I'm a robot that moving my hands following the movements of your hands.I usually know how to imitate those in front of me, but today I got confused and I do not recognize your hands very well. Can you help me control my body? I'll give you now three tasks, and for each of them you'll have 15 seconds, will you be successful?", cong)


anim.say("Bring both my hands down", cong)

anim.say("Oh, I'm so unfocused, I got confused again. You're very good at it, maybe we'll do it again? Take a minute to understand how I got confused this time and then I will ask you to do more tasks", cong)

anim.say("You are so good at understanding how I move, do you want a challenge? Now you can move me any way you want for 2 minutes, at the end of the two minutes you will not have any tasks. Can you understand how am I programmed to move? If you do not want to, you can stop here", cong)

anim.say("Are you so good at understanding how I move, want a challenge? Now you can move me the way you want for 2 minutes, at the end of the two minutes you will not have any fat. Can you understand how I programmed to move? You can stop at any point.", cong)

anim.say("Oh, where am I? I got confused again. You helped me a lot the last time, let's do it again?. \n Take a minute to understand how I got confused this time and then ask you to do more tasks", cong)


