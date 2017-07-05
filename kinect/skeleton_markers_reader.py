import rospy
from skeleton_markers.msg import Skeleton
from kinect_pos import KinectPose
from std_msgs.msg import String


def callback(data):
    # get the data (name, position):  the data is the massage
    kid_pose = KinectPose()
    kid_pose.update_position(data.position)
    message = str(kid_pose.poses_satisfied)
    # pub = rospy.Publisher ('kinect_poses', String)
    #rospy.init_node('kinect_poses_publisher')
    # rospy.loginfo(message)
    # pub.publish(message)
    print(message)

def kinect_listener():
    #init a listener to kinect and
    rospy.init_node('kinect_listener')
    rospy.Subscriber("skeleton", Skeleton, callback)
    rospy.spin()


print("rinat")
l = kinect_listener()
