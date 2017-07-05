import rospy
from std_msgs.msg import String
from skeleton_markers.msg import Skeleton
import numpy as np


class SkeletonAngles():
    def __init__(self):
        self.pub = rospy.Publisher ('skeleton_angles', String)
        self.names = ['head', 'neck', 'torso', 'left_shoulder', 'left_elbow', 'left_hand',
                      'right_shoulder', 'right_elbow', 'right_hand',
                      'left_hip', 'left_knee', 'left_foot', 'right_hip', 'right_knee', 'right_foot']
        self.positions = {}
        for name in self.names:
            self.positions[name] = {'x': None, 'y': None, 'z': None}

        self.skeleton_angles = np.zeros([8])

    def start(self):
        #init a listener to kinect and
        rospy.init_node('skeleton_angle')
        rospy.Subscriber("skeleton", Skeleton, self.callback)
        rospy.spin()

    def callback(self, data):
        positions = data.position
        for name in self.names:
            self.positions[name]['x'] = positions[self.names.index(name)].x
            self.positions[name]['y'] = positions[self.names.index(name)].y
            self.positions[name]['z'] = positions[self.names.index(name)].z

        #print(self.positions)


        #x_0
        x_0=np.array([self.positions["left_shoulder"]['x']-self.positions["right_shoulder"]['x'],
            self.positions["left_shoulder"]['y']-self.positions["right_shoulder"]['y'],
            self.positions["left_shoulder"]['z']-self.positions["right_shoulder"]['z']])
        x_0=(x_0/np.linalg.norm(x_0))

        #y_0
        mid_shoulder=np.array([self.positions["left_shoulder"]['x']+self.positions["right_shoulder"]['x'],
            self.positions["left_shoulder"]['y']+self.positions["right_shoulder"]['y'],
            self.positions["left_shoulder"]['z']+self.positions["right_shoulder"]['z']])/2

        mid_hip=np.array([self.positions["left_hip"]['x']+self.positions["right_hip"]['x'],
        self.positions["left_hip"]['y']+self.positions["right_hip"]['y'],
        self.positions["left_hip"]['z']+self.positions["right_hip"]['z']])/2

        torso=np.array([self.positions["torso"]['x'],
        self.positions["torso"]['y'],
        self.positions["torso"]['z']])


        y_0= mid_shoulder-torso
        y_0= y_0/np.linalg.norm(y_0)

        #z_0
        z_0=np.cross(x_0,y_0)

        #z_l2
        z_l2=np.array([self.positions["left_elbow"]['x']-self.positions["left_shoulder"]['x'],
        self.positions["left_elbow"]['y']-self.positions["left_shoulder"]['y'],
        self.positions["left_elbow"]['z']-self.positions["left_shoulder"]['z']])
        z_l2=z_l2/np.linalg.norm(z_l2)


        #thtrl
        z_2_z_0_l=np.dot(z_l2,z_0)
        z_2_y_0_l=np.dot(z_l2,y_0)
        thtl1=np.arctan2(-z_2_y_0_l,z_2_z_0_l)

        # psil1
        x_l1=x_0
        z_l1=np.dot(self.rot_x(thtl1),z_0)
        z_2_x_1_l=np.dot(z_l2,x_l1)
        z_2_z_1_l=np.dot(z_l2,z_l1)
        psil1=np.arctan2(z_2_x_1_l,z_2_z_1_l)


        #phi_L
        r_l=np.dot(self.rot_y(psil1),self.rot_x(thtl1))
        x_2l=np.dot(r_l,x_0)
        y_2l=np.dot(r_l,y_0)
        z_l4=np.array([self.positions["left_hand"]['x']-self.positions["left_elbow"]['x'],
            self.positions["left_hand"]['y']-self.positions["left_elbow"]['y'],
            self.positions["left_hand"]['z']-self.positions["left_elbow"]['z']])
        z_l4 = z_l4/np.linalg.norm(z_l4)
        z_4_y_2_l=np.dot(z_l4,y_2l)
        z_4_x_2_l=np.dot(z_l4,x_2l)
        phi_l=np.arctan2(-z_4_y_2_l,-z_4_x_2_l)

        #omega_l
        # x_3l=np.dot(self.rot_z(phi_l),x_2l)
        # z_3l=z_l2
        # z_4_x_3_l=np.dot(z_l4,x_3l)
        # z_4_z_3=np.dot(z_l4,z_3l)
        # omega_l=np.arctan2(z_4_x_3_l,z_4_z_3)
        omega_l=-np.arccos(np.dot(z_l2,z_l4))
        # print 'thtl1',thtl1,'psil1',psil1,'phi_l', phi_l,'omega_l', omega_l


        # psil1= np.arcsin(np.dot(x_0,z_l2))
        # thtl1= np.arcsin(-np.dot(y_0,z_l2)/np.cos(psil1))


        #z_r2
        z_r2=np.array([self.positions["right_elbow"]['x']-self.positions["right_shoulder"]['x'],
            self.positions["right_elbow"]['y']-self.positions["right_shoulder"]['y'],
            self.positions["right_elbow"]['z']-self.positions["right_shoulder"]['z']])
        z_r2=z_r2/np.linalg.norm(z_r2)

        #thtrl
        z_2_z_0_r=np.dot(z_r2,z_0)
        z_2_y_0_r=np.dot(z_r2,y_0)
        thtr1=np.arctan2(-z_2_y_0_r,z_2_z_0_r)

        # psil1
        x_r1=x_0
        z_r1=np.dot(self.rot_x(thtr1),z_0)
        z_2_x_1_r=np.dot(z_r2,x_r1)
        z_2_z_1_r=np.dot(z_r2,z_r1)
        psir1=np.arctan2(z_2_x_1_r,z_2_z_1_r)

        #phi_r
        r_r=np.dot(self.rot_y(psir1),self.rot_x(thtr1))
        x_2r=np.dot(r_r,x_0)
        y_2r=np.dot(r_r,y_0)
        z_r4=np.array([self.positions["right_hand"]['x']-self.positions["right_elbow"]['x'],
            self.positions["right_hand"]['y']-self.positions["right_elbow"]['y'],
            self.positions["right_hand"]['z']-self.positions["right_elbow"]['z']])
        z_r4=z_r4/np.linalg.norm(z_r4)
        z_4_y_2_r=np.dot(z_r4,y_2r)
        z_4_x_2_r=np.dot(z_r4,x_2r)
        phi_r=np.arctan2(z_4_y_2_r,z_4_x_2_r)

        #omega_l
        # x_3l=np.dot(self.rot_z(phi_l),x_2l)
        # z_3l=z_l2
        # z_4_x_3_l=np.dot(z_l4,x_3l)
        # z_4_z_3=np.dot(z_l4,z_3l)
        # omega_l=np.arctan2(z_4_x_3_l,z_4_z_3)
        omega_r=np.arccos(np.dot(z_r2,z_r4))



        # psir1= np.arcsin(np.dot(x_0,z_r2))
        # thtr1= np.arcsin(-np.dot(y_0,z_r2)/np.cos(psir1))


        # y_l2= np.dot(np.dot(self.rot_y(psil1) ,self.rot_x(thtl1)),y_0)

        #x_l2
        # x_l2= np.dot(np.dot(self.rot_y(psil1) ,self.rot_x(thtl1)),x_0)

        #z_l4
        # z_l4=np.array([self.positions["left_hand"]['x']-self.positions["left_elbow"]['x'],
        # self.positions["left_hand"]['y']-self.positions["left_elbow"]['y'],
        # self.positions["left_hand"]['z']-self.positions["left_elbow"]['z']])
        # z_l4 = z_l4/np.linalg.norm(z_l4)

        # z_l4_2=np.array([np.dot(z_l4,x_l2),np.dot(z_l4,y_l2),np.dot(z_l4,z_l2)])

        # eta_l= np.arctan2(z_l4_2[0],z_l4_2[1])
        # omega_l=-np.arccos(z_l4_2[2])
        # print omega_l


        # omega_l=-np.arccos(np.dot(z_l2,z_l4)) #LElbowRoll
        # eta_l=np.arcsin(np.dot(z_l4,y_l2)/np.sin(omega_l)) #LElbowYaw
        # omega_l=-np.arccos(np.dot(z_l2,z_l4)) #LElbowRoll

        # print 'omega_l',omega_l,'eta_l',eta_l
        # print "psir1",psir1*60,"thtr1",thtr1*60



        # self.skeleton_angles[0:4] = np.zeros([4])

        self.skeleton_angles[0]=thtl1
        self.skeleton_angles[1]=psil1
        # self.skeleton_angles[2]=phi_l
        # self.skeleton_angles[3]=omega_l

        # takes right_shoulder, right_elbow, right_hand --> 4 angles
        # self.skeleton_angles[4:8] = np.zeros([4])

        self.skeleton_angles[4]=thtr1
        self.skeleton_angles[5]=psir1
        # self.skeleton_angles[6]=phi_r
        # self.skeleton_angles[7]=omega_r

        pub_str = ''
        for s in self.skeleton_angles:
            pub_str += str(s) + ','
        self.pub.publish(pub_str[:-1])
        # print('====== skeleton_angles ====== published: ', pub_str[:-1])







    def rot_x(self,alpa):
        R= np.array([[1,0,0],[0,np.cos(alpa),np.sin(alpa)],[0,-np.sin(alpa),np.cos(alpa)]])
        return R

    def rot_y(self,alpa):
        R= np.array([[np.cos(alpa),0,-np.sin(alpa)],[0,1,0],[np.sin(alpa),0,np.cos(alpa)]])
        return R

    def rot_z(self,alpa):
        R= np.array([[np.cos(alpa),np.sin(alpa),0],[-np.sin(alpa),np.cos(alpa),0],[0,0,1]])
        return R






skeleton_angles = SkeletonAngles()
skeleton_angles.start()