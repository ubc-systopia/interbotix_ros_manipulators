import sys
import json
import time
import numpy as np
import yaml
from yaml import Loader
from sensor_msgs.msg import JointState

sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules')
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from pyniryo import tcp_client
from workflow_utils import apply_offset_translation, global_to_local_viper, local_to_global_viperx, viperx_move, local_to_global_ned, global_to_local_ned, ned2_move
from workflow_utils import get_viperx_gripper_state, access_new_origin_locations


def test_offset(descr, local_ned_location, local_viperx_location):
    global_from_viperx = local_to_global_viperx(local_viperx_location)
    local_ned_from_viperx = global_to_local_ned(global_from_viperx)
    local_ned_from_viperx_offset = apply_offset_translation(local_ned_from_viperx)

    print("\n----",descr,"----")
    print("Local N grid coords (expected wanted pose): ", local_ned_location)
    print("Local N grid coords from V w/o offset: ", local_ned_from_viperx)
    print("Local N grid coords from V with offset (actual): ", local_ned_from_viperx_offset)

    return local_ned_from_viperx_offset


def print_global_values(descr, local_viperx_location):
    global_from_viperx = local_to_global_viperx(local_viperx_location)
    print("\n----",descr,"----")
    print("Global coords from V: ", global_from_viperx)


def print_all_global_vals():
    print_global_values("min grid", [0.52,0.0034,0.0135])
    print_global_values("max grid", [0.61,0.228,0.10])
    print_global_values("min dosing", [0.06,0.43,0.0135])    
    print_global_values("max dosing", [0.27,0.51,0.29])
    print_global_values("min ts", [0.436,-0.32,0.0135])    
    print_global_values("max ts", [0.549,-0.23,0.081])


def print_new_global_vals():
    with open('locations.json', 'r') as f:
        locs = json.load(f)
    f.close()
    half_grid = locs["half_grid"]["viperx"]
    hotplate = locs["hotplate"]["viperx"]
    half_grid_mins = [half_grid["min_x"], half_grid["min_y"], half_grid["min_z"]]
    print_global_values("half_grid_mins",half_grid_mins)
    half_grid_maxs = [half_grid["max_x"], half_grid["max_y"], half_grid["max_z"]]
    print_global_values("half_grid_maxs",half_grid_maxs)
    hotplate_mins = [hotplate["min_x"], hotplate["min_y"], hotplate["min_z"]]
    print_global_values("hotplate_mins",hotplate_mins)
    hotplate_maxs = [hotplate["max_x"], hotplate["max_y"], hotplate["max_z"]]
    print_global_values("hotplate_maxs",hotplate_maxs)

if __name__ == '__main__':
    # print_all_global_vals()
    # print_new_global_vals()

    local_ned = global_to_local_ned([-0.02, -0.0146, -0.1965])
    local_viper = global_to_local_viper([-0.02, -0.0146, -0.1965])

    global_from_viper = local_to_global_viperx([0.52, 0.0034, 0.0135])
    global_from_ned = local_to_global_ned([0.326, -0.028, 0.018])

    print(global_from_viper)
    print(global_from_ned)
    
    # local_pose_min = [thermoshaker['viperx']['min_x'],thermoshaker['viperx']['min_y'],thermoshaker['viperx']['min_z']]
    # local_pose_max = [thermoshaker['viperx']['max_x'],thermoshaker['viperx']['max_y'],thermoshaker['viperx']['max_z']]
    
    # global_pose_min = local_to_global_viperx(local_pose_min)
    # global_pose_max = local_to_global_viperx(local_pose_max)
    
    # grid_nw_viperx_pickup_safe_height_local = [0.54, -0.00222128,  0.23]
    # grid_nw_viperx_pickup_safe_height_global = local_to_global_viperx(grid_nw_viperx_pickup_safe_height_local)
    
    # grid_nw_viperx_pickup_local = [0.53,   0.00102628, 0.11]
    # grid_nw_viperx_pickup_global = local_to_global_viperx(grid_nw_viperx_pickup_local) 
    
    """
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    # print(viperx.arm.get_cartesian_pose())
    # [0.54, 0.018,  0.23]
    # viperx.arm.set_ee_pose_components(x=0.54, y=0.018, z=0.23)
    
    viperx.arm.go_to_sleep_pose() 
    print(get_viperx_gripper_state(viperx))
    
    viperx.gripper.open() 
    print(get_viperx_gripper_state(viperx))
    
    viperx.gripper.close()
    print(get_viperx_gripper_state(viperx))
    
    viperx.arm.go_to_sleep_pose() 
    viperx.gripper.open()
    print(get_viperx_gripper_state(viperx))

    exit(1)
    # viperx.gripper.open()
    # print(viperx.arm.get_joint_commands())
    """
    
    # ned2_ip = "169.254.200.200"
    # global ned2
    # ned2 = tcp_client.NiryoRobot(ned2_ip)
    # ned2.calibrate_auto()
    # ned2.update_tool()
    # ned2.move_to_home_pose()
    # print(ned2.get_joints())

    
    # pose = [0.313,-0.170,0.1,0,0,0]
    # pose=[0.265,-0.162,0.1,0,0,0]
    # ned2.move_pose(pose)
    # exit(1)

    # viperx_move(viperx, grid_nw_viperx_pickup_safe_height_global, "test")
    # viperx_move(viperx, grid_nw_viperx_pickup_global, "test")
    # viperx_pick_up_object(viperx, global_pose_max, "test")
    
    """
    Want: translate local coords to global coords in locations.json
    Test locations: grid_min, grid_max
    
    grid_viperx = [[0.52,0.0034,0.0135],[0.61,0.228,0.10]]
    # Ned = [max_x,min_y,min_z],[min_x,max_y,max_z]
    grid_ned2 = [[0.462,-0.035,0.08],[0.265,0.068,0.133]]
    
    dosing_viperx = [[0.06,0.43,0.0135],[0.27,0.51,0.29]]
    dosing_ned2 = [[0.071,-0.422,0.08],[-0.012,-0.219,0.330]]

    test_offset("Min Grid", grid_ned2[0], grid_viperx[0])
    test_offset("Max Grid", grid_ned2[1], grid_viperx[1])

    test_offset("Min Dosing", dosing_ned2[0], dosing_viperx[0])
    test_offset("Max Dosing", dosing_ned2[1], dosing_viperx[1])
    """

    """
    Want: test coord systemation translation
     e.g. local viper -> global -> local ned
     e.g. local ned -> global -> local viper
    

    # grid_nw_pickup_safe_height, grid_nw_pickup
    # grid_nw_viperx = [[0.54, -0.00222128,  0.23],[0.53,   0.00102628, 0.11]]
    grid_nw_viperx = [[0.54, 0.018,  0.23],[0.53,   0.018, 0.12]]
    grid_nw_ned2 = [[0.443, -0.014 , 0.292],[0.447, -0.022, 0.108]]

    pose_with_offset = test_offset("safe height", grid_nw_ned2[0], grid_nw_viperx[0])
    pose_with_offset = test_offset("pickup", grid_nw_ned2[1], grid_nw_viperx[1])
    """


    # viperx_move(viperx, global_pose_viperx, 1)
    # ned2_move(ned2, np.append(t1_local_ned2,([0,0,0])), 1)
    # ned2_move(ned2, np.append(t1_local_viperx,([0,0,0])), 1)
    # ned2_move(ned2, np.append(pose_with_offset,([0,0,0])), 1)
    # ned2_move(ned2, np.append(grid_nw_ned2[0],([0,0,0])), 1)
      

"""
    print("\nTest2: local ned -> global -> local viper:")
    t2_global_ned2 = local_to_global_ned(grid_nw_ned2[0])
    t2_global_viperx = local_to_global_viperx(grid_nw_viperx[0])
    
    t2_local_viperx = global_to_local_viper(t2_global_viperx)
    t2_local_ned2 = global_to_local_viper(t2_global_ned2)

    print("local viperx location made with viperx coords: ", t2_local_viperx)
    print("local viperx location made with ned coords: ", t2_local_ned2)
    
"""
    
    # viperx.arm.go_to_home_pose()
    # viperx.arm.go_to_sleep_pose()
    # viperx.arm.set_ee_pose_components(x=grid_nw_viperx[0][0],y=grid_nw_viperx[0][1],z=grid_nw_viperx[0][2])
    # viperx.arm.set_ee_pose_components(x=t2_local_ned2[0], y=t2_local_ned2[1], z=t2_local_viperx[2])
    # viperx.arm.set_ee_pose_components(x=t2_local_ned2[0], y=t2_local_ned2[1], z=t2_local_ned2[2])
    
    # local_pose_viper = global_to_local_viper(global_pose_viperx)

    # dosing_device = [[0.16402257, 0.34746304, 0.19],[0.16247981, 0.47495207, 0.19],[0.15748769, 0.45, 0.10]]
    # for pose in dosing_device:
    #     global_pose = local_to_global_viperx(pose)
    #     print(global_pose)
    #     viperx_move(viperx, global_pose, 1)
    
    # print(viperx.arm.get_cartesian_pose())
    
    
    # viperx.arm.go_to_home_pose()
    # viperx.arm.set_ee_pose_components(x=0.2, y=0.2, z=0.2)

    
    # try:
    #     # ned2.move_pose([0.1,0.1,0.1, 0.002, 0.751, 0])
    #     print(ned2.get_pose_quat())
    # except Exception as e:
    #     sys.stderr.write(str(e))