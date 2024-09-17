import sys
sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules/src')

from interbotix_xs_modules.arm import InterbotixManipulatorXS
from pyniryo import tcp_client, enums_communication
import numpy as np

def viperx_end_to_mid(viperx_end_tip_coords):
    transform_ee_gripper_link = np.array([
            [1.0, 0.0, 0.0, 0.0295],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0,0.0, 0.0, 1.0]

    ])

    viperx_mid_tip_coords= np.dot(np.linalg.inv(transform_ee_gripper_link), [viperx_end_tip_coords[0], viperx_end_tip_coords[1],viperx_end_tip_coords[2],1])
    return np.ndarray.tolist(np.concatenate((viperx_mid_tip_coords[0:3], viperx_end_tip_coords[3:6])))

def viperx_mid_to_end(viperx_mid_tip_coords):
    transform_ee_gripper_link = np.array([
            [1.0, 0.0, 0.0, 0.0295],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0,0.0, 0.0, 1.0]

    ])

    viperx_end_tip_coords = np.dot(transform_ee_gripper_link, [viperx_mid_tip_coords[0], viperx_mid_tip_coords[1], viperx_mid_tip_coords[2], 1])
    return np.ndarray.tolist(np.concatenate((viperx_end_tip_coords[0:3], viperx_mid_tip_coords[3:6])))

def viperx_end_tip_to_global(viperx_end_tip_coords):
    translation_matrix = np.array([
            [0.0, -1, 0.0, 0.513],
            [1, 0.0, 0.0, -0.5723],
            [0.0, 0.0, 1.0, 0.02122],
            [0.0,0.0, 0.0, 1.0]

        ])

    rotation_matrix = np.array([
        [0.0, -1, 0.0],
        [1, 0.0, 0.0],
        [0.0, 0.0, 1.0]
    ])


    convert_viperx_to_global_cartesian = np.dot(translation_matrix, [viperx_end_tip_coords[0], viperx_end_tip_coords[1], viperx_end_tip_coords[2], 1])
    convert_viperx_to_global_rotation = np.dot(rotation_matrix, viperx_end_tip_coords[3:6])

    global_coords = np.concatenate((convert_viperx_to_global_cartesian[0:3], convert_viperx_to_global_rotation))
    return np.ndarray.tolist(global_coords)

def viperx_mid_tip_to_global(viperx_mid_tip_coords):
    viperx_end_tip_coords = viperx_mid_to_end(viperx_mid_tip_coords)
    global_coords = viperx_end_tip_to_global(viperx_end_tip_coords)
    return global_coords

def global_to_viperx_end_tip(global_coords):
    translation_matrix = np.array([
            [0.0, -1, 0.0, 0.513],
            [1, 0.0, 0.0, -0.5723],
            [0.0, 0.0, 1.0, 0.02122],
            [0.0,0.0, 0.0, 1.0]

        ])

    rotation_matrix = np.array([
        [0.0, -1, 0.0],
        [1, 0.0, 0.0],
        [0.0, 0.0, 1.0]
    ])


    convert_global_to_viperx_cartesian = np.dot(np.linalg.inv(translation_matrix), [global_coords[0], global_coords[1], global_coords[2], 1])
    convert_global_to_viperx_rotation = np.dot(np.linalg.inv(rotation_matrix), global_coords)

    viperx_end_tip_coords = np.concatenate((convert_global_to_viperx_cartesian[0:3], convert_global_to_viperx_rotation))
    return np.ndarray.tolist(viperx_end_tip_coords)

def global_to_viperx_mid_tip(global_coords):

    viperx_end_tip = global_to_viperx_end_tip(global_coords)
    viperx_mid_tip = viperx_end_to_mid(viperx_end_tip)
    return viperx_mid_tip

def viperx_run(pose=None):
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    if pose:
        # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2],roll=pose[3], pitch=pose[4], yaw=pose[5])
        viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
        print('viperx mid tip coords: ', viperx.arm.get_cartesian_pose())
        print('viperx end tip coords: ', viperx.arm.get_cartesian_pose_gripper_tip())
    return viperx.arm.get_cartesian_pose_gripper_tip()
    
def ned_run(pose=None):
    ned2_ip = "169.254.200.200"
    ned2 = tcp_client.NiryoRobot(ned2_ip)
    ned2.calibrate_auto()
    ned2.update_tool()
    ned2.enable_tcp(enable=True)
    ned2.set_tcp([0.085,0,0,0,0,0])
    ned2.move_pose([0.182, 0.007, 0.095, 0.214, 1.066, 0.047])
    if pose:
        ned2.move_pose(pose)
        print('Ned2 end tip coords', ned2.get_pose())

if __name__ == '__main__':

    # pose = [0.23, 0.062, 0.13]
    # new_pose = global_to_viperx_mid_tip(pose)
    # print(new_pose)
    # viperx_end_tip_coords = viperx_run(pose)
    # input()
    viperx_run(None)
    # input()
    
    # global_coords = viperx_end_tip_to_global(viperx_end_tip_coords)
    # ned_run(global_coords)
    # input()
    # ned_run(None)

    
