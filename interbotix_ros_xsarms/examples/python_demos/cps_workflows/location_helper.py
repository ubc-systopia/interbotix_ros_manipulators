import sys
sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules')
from interbotix_xs_modules.arm import InterbotixManipulatorXS

if __name__ == '__main__':
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    print(viperx.arm.get_cartesian_pose())
    # viperx.arm.go_to_sleep_pose()
    # viperx.arm.go_to_home_pose()