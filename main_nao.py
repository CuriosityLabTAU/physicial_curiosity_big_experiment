import os
import threading
from naoqi import ALProxy
import time
import sys


def intro(subject_id=0, nao_ip='192.168.0.104'):
    start_working(subject_id, nao_ip)

    time.sleep(60)


def start_working(subject_id, nao_ip):

    def worker1():
        os.system('roslaunch multi_camera_affdex multi_camera_affdex.launch')

    def worker2():
        os.system('roslaunch skeleton_markers markers.launch')
        return

    def worker3():
        os.system('python curious_game/angle_matrix.py')
        return

    def worker4():
        os.system('python ~/pycharm/twisted_server_ros_2_0/scripts/nao_ros_listener.py ' + nao_ip)
        # os.system('python ~/pycharm/curious_game/nao_ros.py ' + nao_ip)
        return

    def worker5():
        os.system('python ~/pycharm/twisted_server_ros_2_0/scripts/nao_ros_talker.py ' + nao_ip)
        # os.system('python ~/pycharm/curious_game/nao_ros.py ' + nao_ip)
        return

    def worker6():
        os.system('rosbag record -a -o data/physical_curiosity_big_experiment_' + str(subject_id) + '.bag')

    def worker7():
        os.system('python curious_game/skeleton_angles.py')



    t1 = threading.Thread(target=worker1)
    t1.start()
    threading._sleep(0.5)

    t2 = threading.Thread(target=worker2)
    t2.start()
    threading._sleep(0.2)

    t3 = threading.Thread(target=worker3)
    t3.start()
    threading._sleep(0.2)

    t4 = threading.Thread(target=worker4)
    t4.start()
    threading._sleep(0.2)

    t5 = threading.Thread(target=worker5)
    t5.start()
    threading._sleep(0.2)

    t6 = threading.Thread(target=worker6)
    t6.start()
    threading._sleep(0.2)

    t7 = threading.Thread(target=worker7)
    t7.start()
    threading._sleep(0.2)

if len(sys.argv) > 1:
    print('sys.argv', sys.argv)
    intro(int(sys.argv[1]), sys.argv[2])
else:
    intro()

