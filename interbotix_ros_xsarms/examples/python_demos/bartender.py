import sys
sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules')
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np

from pyniryo import tcp_client

# This script makes the end-effector perform pick, pour, and place tasks
#
# To get started, open a terminal and type 'roslaunch interbotix_xsarm_control xsarm_control.launch robot_model:=wx250'
# Then change to this directory and type 'python bartender.py  # python3 bartender.py if using ROS Noetic'

def main():
    #bot = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    # bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    # bot.arm.set_single_joint_position("waist", np.pi/2.0)
    # bot.gripper.open()
    # bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
    # bot.gripper.close()
    # bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
    # bot.arm.set_single_joint_position("waist", -np.pi/2.0)
    # bot.arm.set_ee_cartesian_trajectory(pitch=1.5)
    # bot.arm.set_ee_cartesian_trajectory(pitch=-1.5)
    # bot.arm.set_single_joint_position("waist", np.pi/2.0)
    # bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
    # bot.gripper.open()
    # bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
    # bot.arm.go_to_home_pose()
    # bot.arm.go_to_sleep_pose()



    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    ned2_ip = "169.254.200.200"
    global ned2
    ned2 = tcp_client.NiryoRobot(ned2_ip)
    ned2.calibrate_auto()
    ned2.update_tool()

    vpose = [0.5123002,  0.29463251, 0.26257251]
    viperx.arm.set_ee_pose_components(x=vpose[0], y=vpose[1], z=vpose[2])


    # viperx.arm.go_to_home_pose()
    # viperx.arm.go_to_sleep_pose()

    viperpos = viperx.arm.get_cartesian_pose()
    print('ViperX: ', viperpos)


  

    npose = []
    ned2.move_pose(npose)

    # ned2.move_to_home_pose()

    ned2pose = ned2.pose
    print('Ned2: ', ned2pose)
    

if __name__=='__main__':
    main()
