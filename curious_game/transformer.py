from curious_game import *
from nao_move import *
import random
import numpy as np


class Transformer:

    def __init__(self, transform=None):
        # transform is the transformation the robot performs. we start with a linear transform,
        #  i.e. transform is a numpy matrix
        self.howie = NaoNode()
        self.child = ChildKinect()
        self.transform = transform
        self.pose_selected = None
        # self.hertzel_says = True

    # def robot_performs_action(self, pose):
    #     # select the pose from the list of poses
    #     self.pose_selected = random.choice(self.howie.pose_names)
    #     print('selected: ', self.pose_selected)
    #     self.howie.move_to_pose(self.howie.poses[self.pose_selected])

    def get_pose_detected_names(self):
        indices = self.child.current_param
        pose_detected_names = []
        for i, ind in enumerate(indices):
            if ind:
                pose_detected_names.append(self.howie.pose_names[i])
        print(self.pose_selected, 'The poses', pose_detected_names)
        return pose_detected_names

    def robot_performs_action(self, pose):
        # select the pose from the list of poses
        #self.pose_selected = random.choice(self.howie.pose_names)
        if self.transform is not None:
            self.pose_selected = self.transform.dot(pose)
        else:
            self.pose_selected = pose
        print('selected_: ', self.pose_selected)
        self.howie.move_to_pose(self.howie.poses[self.pose_selected])
