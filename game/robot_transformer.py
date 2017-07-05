from game import *
from nao_move import *
import random


class RobotTransformer(object):

    def __init__(self):
        self.howie = NaoNode()
        self.child = ChildKinect()
        self.pose_received = None

    def robot_performs_action(self):
        # select the pose from the list of poses
        self.pose_selected = random.choice(self.howie.pose_names)
        print('selected: ', self.pose_selected)

        # select whether to have simon says or not
        self.hertzel_says = random.choice([True, False])
        if self.hertzel_says:
            self.howie.play_file('Hertzel says.wav')
        wav_file = self.pose_selected.replace('_', ' ') + '.wav'
        self.howie.play_file(wav_file)

        self.howie.move_to_pose(self.howie.poses[self.pose_selected])

    def get_pose_detected_names(self):
        indices = self.child.current_param
        pose_detected_names = []
        for i, ind in enumerate(indices):
            if ind:
                pose_detected_names.append(self.howie.pose_names[i])
        print(self.pose_selected, 'The poses', pose_detected_names)
        return pose_detected_names
