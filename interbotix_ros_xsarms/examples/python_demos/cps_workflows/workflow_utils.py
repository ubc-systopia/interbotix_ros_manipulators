import json
import time
import sys
import numpy as np
from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
from dummy import SimulatedSmartDevice, Vial

sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules')
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from pyniryo import tcp_client, enums_communication

### LOCATION DATA
# [x,y,z, roll, pitch, yaw]
# where x/y/z are in m, roll/pitch/yaw are in radians
locations = {
    "grid": {
        "NW": {
            "meta": "original vial location",
            "viperx": {
                "pickup_safe_height": [0.537, 0.018,  0.23],
                "pickup": [0.537, 0.018, 0.12]
            },
            "ned2": {
                "pickup_safe_height": [0.443, -0.010 , 0.292, -0.099, 0.028, -0.020],
                "pickup": [0.443, -0.010, 0.13, -0.078, 0.121, -0.008]
            },
        },
        "SE": {
            "meta": "imaginary hotplate for now",
            "ned2": {
                "pickup_safe_height": [0.23, 0.062, 0.3, -0.037, 0.061, 0.046],
                "pickup": [0.23, 0.062, 0.13, -0.033, 0.142, -0.004]
            }
        }
    },
    "dosing_device": {
        "viperx": {            
            "approach": [0.15, 0.347, 0.19],           
            "pickup_safe_height": [0.15, 0.475, 0.19],
            "pickup": [0.15, 0.45, 0.10]
        },
        "ned2": {         
            "approach": [-0.008, -0.366, 0.234, -0.033, 0.015, -1.626],           
            "pickup_safe_height": [-0.009, -0.495, 0.196, -0.046, -0.032, -1.611],
            "pickup": [-0.009, -0.495, 0.113, -0.046, -0.032, -1.611]
        }
    },
    "thermoshaker": {
        "viperx": {
            "pickup_safe_height": [0.527, -0.272,  0.23],
            "pickup": [0.527, -0.272,  0.12]
        }
    },
    "hotplate": {
        "viperx": {
            "pickup_safe_height": [],
            "pickup": []
        },
        "ned2": {
            "pickup_safe_height": [],
            "pickup": []
        }
    }
}

def get_pos_data():
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    print(viperx.arm.get_cartesian_pose())


### SETUP + TEARDOWN
def setup_thermoshaker(thermoshaker, safety_temp, wd_1, wd_2):
    thermoshaker.watchdog_safety_temperature = safety_temp
    thermoshaker.start_watchdog_mode_1(wd_1)
    thermoshaker.start_watchdog_mode_2(wd_2)
    thermoshaker.switch_to_normal_operation_mode()
    print("Completed setting up thermoshaker.")

def initialize_devices(ts, hp, dosing, soln, viper, ned):
    if ts:
        global thermoshaker
        kwargs = {
            'port': 'COM8',
            'dummy': True,
        }
        thermoshaker = Thermoshaker.create(**kwargs)
        setup_thermoshaker(15.5, 30, 30)
    if hp:
        global hotplate
        port = 'COM5'
        hotplate = MockMagneticStirrer(device_port=port)
    if dosing:
        global dosing_device
        args = {
            "name": "Virtual Dosing Station",
            "door": {'plane': 'N', 
                     'state': 'closed', 
                     'move_time': 1},
            "action": "dosing a vial"
        }
        dosing_device = SimulatedSmartDevice(args["name"], args["door"], args["action"])
    if soln:
        global vial
        args = {
            "max_vol": 5,
            "temp": 20
        }
        vial = Vial(args["max_vol"], args["temp"])
    if viper:
        global viperx
        viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
        viperx.arm.go_to_sleep_pose()
    if ned:
        ned2_ip = "169.254.200.200"
        global ned2
        ned2 = tcp_client.NiryoRobot(ned2_ip)
        ned2.calibrate_auto()
        ned2.update_tool()
        ned2.move_to_home_pose()

def disconnect_devices(hp, viperx, ned2):
    if hp:
        hotplate.disconnect()
    if viperx:
        viperx.arm.go_to_sleep_pose()
    if ned2:
        ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
        ned2.close_connection()


### HOTPLATE
def start_stirring_soln(hotplate, start_stir_rate, delay):
    print("[HOTPLATE]: Starting to stir solution...")
    hotplate.start_stirring()
    hotplate.target_stir_rate = start_stir_rate
    time.sleep(delay)

def start_heating_soln(hotplate, vial, start_temp, delay):
    print("[HOTPLATE]: Starting to heat solution...")
    hotplate.target_temperature = start_temp
    hotplate.start_heating()
    time.sleep(delay)
    # vial.change_temp(start_temp)

def stop_stirring_soln(hotplate, end_stir_rate, delay):
    hotplate.target_stir_rate = end_stir_rate
    time.sleep(delay)
    hotplate.stop_stirring()
    print("[HOTPLATE]: Stopped stirring solution.")

def stop_heating_soln(hotplate, vial, end_temp, delay):
    hotplate.target_temperature = end_temp
    time.sleep(delay)
    hotplate.stop_heating()
    print("[HOTPLATE]: Stopped heating solution.")
    # vial.change_temp(end_temp)


### THERMOSHAKER
def start_shaking_soln(thermoshaker, speed, delay):
    thermoshaker.set_speed = speed
    print("[THERMOSHAKER]: Starting to shake solution...")
    thermoshaker.start_shaking()
    time.sleep(delay)

# TODO: debug change_temp
def start_tempering_soln(thermoshaker, vial, goal_temp, delay):
    thermoshaker.set_temperature = goal_temp
    print("[THERMOSHAKER]: Starting to temper solution...")
    thermoshaker.start_tempering()
    time.sleep(delay)
    # vial.change_temp(goal_temp)

def stop_shaking_soln(thermoshaker):
    thermoshaker.stop_shaking()
    print("[THERMOSHAKER]: Stopped shaking solution.")

def stop_tempering_soln(thermoshaker):
    thermoshaker.stop_tempering()
    print("[THERMOSHAKER]: Stopped tempering solution.")


### VIPERX
# could refactor these into one function, but do we want to keep fn names?
# could add a unique name/id to Vial and use getter to retrieve it for printing
def viperx_pick_up_object(viperx, pose, obj):
    name = obj.__class__.__name__
    print(f"\n[VIPERX]: Picking up {name}.")
    viperx.gripper.open(delay=2)
    if "approach" in pose.keys():
        viperx_move(viperx, pose["approach"], 1)
    viperx_move(viperx, pose["pickup_safe_height"], 1)
    
    viperx_move(viperx, pose["pickup"], 1)
    viperx.gripper.close(delay=2)
    viperx_move(viperx, pose["pickup_safe_height"], 0)
    if "approach" in pose.keys():
        viperx_move(viperx, pose["approach"], 1)

def viperx_place_object(viperx, pose, obj):
    name = obj.__class__.__name__
    print(f"[VIPERX]: Placing {name}.\n")
    if "approach" in pose.keys():
        viperx_move(viperx, pose["approach"], 1)
    viperx_move(viperx, pose["pickup_safe_height"], 1)
    viperx_move(viperx, pose["pickup"], 1)
    viperx.gripper.open(delay=2)
    
    viperx_move(viperx, pose["pickup_safe_height"], 0)
    if "approach" in pose.keys():
        viperx_move(viperx, pose["approach"], 1)

def access_new_origin_locations(bot):
    with open('locations.json', 'r') as f:
        locs = json.load(f)
    f.close()
    
    return locs["global_origin"][bot]

# @param l_coords = [x_local, y_local, z_local]
def local_to_global_viperx(l_coords):
    translation_values = access_new_origin_locations("viperx")
    tx = translation_values["x"]
    ty = translation_values["y"]
    tz = translation_values["z"]

    # Define translation matrix
    translation = np.array(
        [
            [1, 0, 0, -tx],
            [0, 1, 0, -ty],
            [0, 0, 1, -tz],
            [0, 0, 0, 1],
        ]
    )
    
    # Convert local coordinates to homogeneous coordinates
    local_coords_homog = np.append(l_coords, 1)
    # Apply translation matrix to local coordinates
    global_coords_homog = np.dot(translation, local_coords_homog)
    # Convert global coordinates back to 3D coordinates
    global_coords = global_coords_homog[:-1]
    return global_coords

# @param g_coords = [x_global, y_global, z_global]
def global_to_local_viper(g_coords):
    # Define the translation matrix
    translation_values = access_new_origin_locations("viperx")
    tx = translation_values["x"]
    ty = translation_values["y"]
    tz = translation_values["z"]
    # tx = -0.36216396
    # ty = -0.15244984
    # tz = -0.00803854

    translation_matrix = np.array(
            [[1, 0, 0, -tx], [0, 1, 0, -ty], [0, 0, 1, -tz], [0, 0, 0, 1]]
    )
    
    # Define the global coordinates as a column vector
    global_vector = np.array([[g_coords[0]], [g_coords[1]], [g_coords[2]], [1]])

    # Compute the local coordinates
    l_coords = np.linalg.inv(translation_matrix).dot(global_vector)

    return np.reshape(l_coords[:3], (1,3))[0]


def viperx_move(viperx, pose, delay):
    viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    time.sleep(delay)


### NED2
def ned2_pick_up_object(ned2, pose, obj):
    name = obj.__class__.__name__
    print(f"\n[NED2]: Picking up {name}.")
    if "approach" in pose.keys():
        ned2_move(ned2, pose["approach"], 1)
    ned2_move(ned2, pose["pickup_safe_height"],1)
    ned2.open_gripper()
    ned2.wait(1)
    ned2_move(ned2, pose["pickup"],1)
    try:
        #ned2.grasp_with_tool()
        ned2.close_gripper()
        ned2.wait(1)
        ned2_move(ned2, pose["pickup_safe_height"],1)
        if "approach" in pose.keys():
            ned2_move(ned2, pose["approach"], 1)
    except Exception as e:
        sys.stderr.write(str(e))

def ned2_place_object(ned2, pose, obj):
    name = obj.__class__.__name__
    print(f"[NED2]: Placing {name}.\n")
    if "approach" in pose.keys():
        ned2_move(ned2, pose["approach"], 1)
    ned2_move(ned2, pose["pickup_safe_height"],1)
    ned2_move(ned2, pose["pickup"],1)
    try:
        ned2.open_gripper()
        ned2.wait(1)
        ned2_move(ned2, pose["pickup_safe_height"],1)
        if "approach" in pose.keys():
            ned2_move(ned2, pose["approach"], 1)
    except Exception as e:
        sys.stderr.write(str(e))

# @param l_coords = [x_local, y_local, z_local]
def local_to_global_ned(l_coords):
    translation_values = access_new_origin_locations("ned2")
    tx = translation_values["x"]
    ty = translation_values["y"]
    tz = translation_values["z"]

    # Define inverse translation vector
    # inv_trans = np.array([0.313, -0.170, 0.066])
    inv_trans = np.array([tx, ty, tz])

    # Define inverse rotation matrix (transpose of rot_z)
    inv_rot_z = np.array([[0, 1, 0],
                          [-1, 0, 0],
                          [0, 0, 1]])

    # Reshape local coordinate to a column vector
    l_coords = np.array(l_coords).reshape(-1, 1)

    # Apply inverse translation vector to local coordinate
    g_coords = l_coords - inv_trans.reshape(-1, 1)

    # Apply inverse rotation matrix to global coordinate
    g_coords = inv_rot_z @ g_coords

    # Reshape global coordinate to a 1D array
    return g_coords.ravel()

# @param g_coords = [x_global, y_global, z_global]
def global_to_local_ned(g_coords):
    translation_values = access_new_origin_locations("ned2")
    tx = translation_values["x"]
    ty = translation_values["y"]
    tz = translation_values["z"]

    # Define rotation matrix
    rot_z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    # Define translation vector
    # t_vector = np.array([0.313, -0.170, 0.066])
    t_vector = np.array([tx, ty, tz])

    # Reshape global coordinate to a column vector
    g_coords = np.array(g_coords).reshape(-1, 1)

    # Apply rotation matrix to global coordinate
    l_coords = rot_z @ g_coords

    # Add translation vector to local coordinate
    l_coords = l_coords + t_vector.reshape(-1, 1)

    # Reshape local coordinate to a 1D array
    return l_coords.ravel()

# given a local ned2 pose made from viperx coords, 
# translate it so that it matches the native ned2 local pose for the same position
def apply_offset_translation(ned2_pose):
    # tx = 0.044
    # ty = -0.038
    tx = 0
    ty = 0
    offset_pose = [ned2_pose[0]+tx, ned2_pose[1]+ty]
    for i in range(len(ned2_pose)-2):
        offset_pose.append(ned2_pose[i+2])
    return offset_pose
    # tz = translation_values["z"]

# pose = [x,y,z,roll,pitch,yaw] where x/y/z are in m, roll/pitch/yaw are in radians
def ned2_move(ned2, pose, delay):
    ned2.move_pose(pose)
    time.sleep(delay)


### OTHER

class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

# TODO: add call to ViperX here, push to file instead of printing
# would need to access global robot connections
def monitor_hardware(frame, event, arg):
    if event == "line":
        print(ned2.get_hardware_status())
    return monitor_hardware

# @return "closed" | "open" | "holding something"
def get_viperx_gripper_state(viperx):
    left = viperx.arm.core.robot_get_single_joint_state('left_finger')["position"]
    right = viperx.arm.core.robot_get_single_joint_state('right_finger')["position"]
    print(left, right)
    if left > 0.056 and right < -0.056:
        return "open"
    # check if bound is too tight on closed side - potentially replace 0.021 w/ 0.019 ?
    elif 0.021 < left < 0.056 and -0.056 < right < -0.021:
        return "holding something"
    else:
        return "closed"
