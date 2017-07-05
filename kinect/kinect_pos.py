import json
import re

class KinectPose():
    def __init__(self):
        self.poses_satisfied = []
        self.poses_names = []
        self.poses_conditions = []
        self.positions = {
            'head':{}, 'neck':{}, 'torso':{}, 'left_shoulder':{}, 'left_elbow':{}, 'left_hand':{}, 'right_shoulder':{},
            'right_elbow':{}, 'right_hand':{}, 'left_hip':{}, 'left_knee':{}, 'left_foot':{}, 'right_hip':{},
            'right_knee':{},'right_foot':{}
        }
        with open("poses_logics.json") as data_file:
            logics_json = json.load(data_file)
            #self.poses_conditions = logics_json['conditions']
            self.poses_names = logics_json['names']

    def update_position(self,positions):
        names = ['head', 'neck', 'torso', 'left_shoulder', 'left_elbow', 'left_hand', 'right_shoulder', 'right_elbow', 'right_hand', 'left_hip', 'left_knee', 'left_foot', 'right_hip', 'right_knee', 'right_foot']
        for name in names:
            self.positions[name]['x'] = positions[names.index(name)].x
            self.positions[name]['y'] = positions[names.index(name)].y
            self.positions[name]['z'] = positions[names.index(name)].z
        # self.check_conditions()

    def check_conditions(self):
        positions = self.positions
        self.poses_satisfied = []
        for pose_name in self.poses_names:
            self.poses_satisfied.append (self.check_condition(pose_name))   #(eval(condition))
        print("poses_satistied", self.poses_satisfied)
        print(self.poses_names)

    def check_condition (self,pose_name):
        if (pose_name =="right_hand_up"):
            satisfied = self.check_right_hand_up()
        elif (pose_name=="left_hand_up"):
            satisfied =  self.check_left_hand_up()
        elif (pose_name=="both_hands_up"):
            satisfied = self.check_both_hands_up()
        elif (pose_name =="right_hand_down"):
            satisfied = self.check_right_hand_down()
        elif (pose_name=="left_hand_down"):
            satisfied =  self.check_left_hand_down()
        elif (pose_name=="both_hands_down"):
            satisfied = self.check_both_hands_down()
        elif (pose_name=="right_hand_forward"):
            satisfied = self.check_right_hand_forward()
        elif (pose_name=="left_hand_forward"):
            satisfied = self.check_left_hand_forward()
        elif (pose_name=="both_hands_forward"):
            satisfied = self.check_both_hands_forward()
        elif (pose_name=="right_hand_side"):
            satisfied = self.check_right_hand_side()
        elif (pose_name=="left_hand_side"):
            satisfied = self.check_left_hand_side()
        elif (pose_name=="both_hands_side"):
            satisfied = self.check_both_hands_side()
        else:
            print("error in check condition")
        return satisfied

    def check_right_hand_up(self):
        delta_x = abs(self.positions['right_hand']['x'] - self.positions['right_shoulder']['x'])
        delta_y = self.positions['right_hand']['y'] - self.positions['right_shoulder']['y']
        delta_z = abs(self.positions['right_hand']['z'] - self.positions['right_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x'] - self.positions['left_shoulder']['x'])
        return (delta_x < 0.3 and delta_y > delta_shoulders and delta_z < 0.3)

    def check_left_hand_up(self):
        delta_x = abs(self.positions['left_hand']['x'] - self.positions['left_shoulder']['x'])
        delta_y = self.positions['left_hand']['y'] - self.positions['left_shoulder']['y']
        delta_z = abs(self.positions['left_hand']['z'] - self.positions['left_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x'] - self.positions['left_shoulder']['x'])
        return (delta_x < 0.3 and delta_y > delta_shoulders and delta_z < 0.3)

    def check_both_hands_up(self):
        return self.check_right_hand_up() and self.check_left_hand_up()

    def check_right_hand_down(self):
        delta_x = abs(self.positions['right_hand']['x'] - self.positions['right_shoulder']['x'])
        delta_y = self.positions['right_shoulder']['y'] - self.positions['right_hand']['y']
        delta_z = abs(self.positions['right_hand']['z'] - self.positions['right_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x'] - self.positions['left_shoulder']['x'])
        return (delta_x < 0.3 and delta_y > delta_shpoulders and delta_z < 0.3)

    def check_left_hand_down(self):
        delta_x = abs(self.positions['left_hand']['x'] - self.positions['left_shoulder']['x'])
        delta_y = self.positions['left_shoulder']['y'] - self.positions['left_hand']['y']
        delta_z = abs(self.positions['left_hand']['z'] - self.positions['left_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x'] - self.positions['left_shoulder']['x'])
        return (delta_x < 0.3 and delta_y > delta_shoulders and delta_z < 0.3)

    def check_both_hands_down(self):
        return self.check_right_hand_down() and self.check_left_hand_down()

    def check_right_hand_forward (self):
        delta_x = abs(self.positions['right_hand']['x']-self.positions['right_shoulder']['x'])
        delta_y = abs(self.positions['right_hand']['y']-self.positions['right_shoulder']['y'])
        delta_z = abs(self.positions['right_hand']['z']-self.positions['right_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x']-self.positions['left_shoulder']['x'])
        return (delta_x<0.3 and delta_y<0.3 and delta_z>delta_shoulders)

    def check_left_hand_forward(self):
        delta_x = abs(self.positions['left_hand']['x'] - self.positions['left_shoulder']['x'])
        delta_y = abs(self.positions['left_hand']['yp'] - self.positions['left_shoulder']['y'])
        delta_z = abs(self.positions['left_hand']['z'] - self.positions['left_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x'] - self.positions['left_shoulder']['x'])
        return (delta_x < 0.3 and delta_y < 0.3 and delta_z > delta_shoulders)

    def check_both_hands_forward(self):
        return self.check_right_hand_forward() and self.check_left_hand_forward()

    def check_right_hand_side(self):
        delta_x = abs(self.positions['right_hand']['x']-self.positions['right_shoulder']['x'])
        delta_y = abs(self.positions['right_hand']['y']-self.positions['right_shoulder']['y'])
        delta_z = abs(self.positions['right_hand']['z']-self.positions['right_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x']-self.positions['left_shoulder']['x'])
        return (delta_x>delta_shoulders and delta_y<0.3 and delta_z<0.3)

    def check_left_hand_side(self):
        delta_x = abs(self.positions['left_hand']['x'] - self.positions['left_shoulder']['x'])
        delta_y = abs(self.positions['left_hand']['y'] - self.positions['left_shoulder']['y'])
        delta_z = abs(self.positions['left_hand']['z'] - self.positions['left_shoulder']['z'])
        delta_shoulders = abs(self.positions['right_shoulder']['x'] - self.positions['left_shoulder']['x'])
        return (delta_x > delta_shoulders and delta_y < 0.3 and delta_z < 0.3)

    def check_both_hands_side(self):
        return self.check_right_hand_side() and self.check_left_hand_side()


