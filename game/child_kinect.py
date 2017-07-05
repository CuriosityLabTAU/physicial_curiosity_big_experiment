import rospy
from std_msgs.msg import String

class ChildKinect():
    kinect_listener = None

    def __init__(self):
        self.current_state = None
        self.current_param = None

        print('Starting kinect')
        self.current_state = 'started'

        rospy.init_node('poses_listener', anonymous=True)
        rospy.Subscriber("kinect_poses", String, self.got_pose)

    def wait_for_start_pose(self):
        self.current_state = 'wait_for_start_pose'

    def wait_for_yes_pose(self):
        self.current_state = 'wait_for_yes_pose'

    def wait_for_current_pose(self):
        self.current_state = 'wait_for_current_pose'

    def wait(self):
        pass

    def got_pose(self, data):
        poses = eval(data.data)
        if self.current_state == 'wait_for_start_pose':
            if poses[2] == 1:
                self.current_state = 'start_pose_detected'
                return

        if self.current_state == 'wait_for_yes_pose':
            if poses[2] == 1:
                self.current_state = 'yes_pose_detected'
                return

        if self.current_state == 'wait_for_current_pose':
            self.current_param = poses
            self.current_state = 'received_pose'



