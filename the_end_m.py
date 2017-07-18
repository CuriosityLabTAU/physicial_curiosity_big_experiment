


robotIP = '192.168.0.102'####################Change the IP




from naoqi import ALProxy
port = 9559
managerProxy = ALProxy("ALBehaviorManager", robotIP, port)


managerProxy.post.runBehavior('physical_curiosity/m/the_end')
