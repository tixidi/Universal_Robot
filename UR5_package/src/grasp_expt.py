#!/usr/bin/env python

###
#
# @author Jayakrishnan HJ
# 
# @date May 2018
#
##

import rospy
import tf
from gpd.msg import GraspConfigList
from tf import TransformListener
from geometry_msgs.msg import PointStamped

import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String

class grasper:

    def __init__(self):
        self.listener = TransformListener()
        # Subscribe to the ROS topic that contains the grasps.
        self.sub = rospy.Subscriber('/detect_grasps/clustered_grasps', GraspConfigList, self.grasp_callback)
        self.grasp_acc = []
        self.tempPoint = PointStamped()
        self.transformedPoint = PointStamped()
        
        ## initiate a RobotCommander object. This object is an interface to the
        ## robot as a whole
        self.robot = moveit_commander.RobotCommander()

        ## Instantiate a PlanningSceneInterface object.  This object is an interface
        ## to the world surrounding the robot.
        self.scene = moveit_commander.PlanningSceneInterface()

        ## Instantiate a MoveGroupCommander object.  This object is an interface
        ## to one group of joints.  
        self.group = moveit_commander.MoveGroupCommander("manipulator")


        ## We create this DisplayTrajectory publisher which is used below to publish
        ## trajectories for RVIZ to visualize.
        self.display_trajectory_publisher = rospy.Publisher(
                                          '/move_group/display_planned_path',
                                          moveit_msgs.msg.DisplayTrajectory)
        
    def grasp_callback(self, msg):
        #global grasps
        self.grasps_acc = msg.grasps
        print self.grasps_acc[1].sample
        print msg.header
        self.tempPoint.point = self.grasps_acc[1].sample
        self.tempPoint.header = msg.header
        
        try:
        
            now = rospy.Time(0)
           # self.listener.waitForTransform( "/camera_rgb_optical_frame", "/camera_link", now, rospy.Time(0.1))
            print "Transformed"
            self.transformedPoint = self.listener.transformPoint("/camera_link", self.tempPoint)
        
        except(tf.LookupException, tf.ConnectivityException):
            pass
            
            
        quaternion = tf.transformations.quaternion_from_euler(0, 0, 0)
        pose_target = geometry_msgs.msg.Pose()  
        pose_target.orientation.x = quaternion[0]
        pose_target.orientation.y = quaternion[1]
        pose_target.orientation.z = quaternion[2]
        pose_target.orientation.w = quaternion[3]
        pose_target.position.x = self.transformedPoint.point.x
        pose_target.position.y = self.transformedPoint.point.y
        pose_target.position.z = self.transformedPoint.point.z
     
        self.group.set_pose_target(pose_target)
        plan1 = self.group.plan()
  

        print "============ Waiting while RVIZ displays plan1..."
        rospy.sleep(5)
        self.group.go(wait=True)
        

#def listener():
  
#  rospy.init_node('grasp_expt', anonymous=True)
#  rospy.Subscriber('/detect_grasps/clustered_grasps ',GraspConfigList , grasp_callback)
#  rospy.spin()

def main():
    # Create a ROS node.
    rospy.init_node('get_grasps')
    g1 = grasper()
    rate = rospy.Rate(1)
    rate.sleep()
    rospy.spin()
    
    
if __name__=='__main__':
    main()
    
    

