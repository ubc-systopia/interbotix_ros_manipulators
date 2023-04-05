import time
import sys
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
                "pickup_safe_height": [0.54, -0.00222128,  0.23],
                "pickup": [0.53,   0.00102628, 0.11]
            },
            "ned2": {
                "pickup_safe_height": [0.451, -0.022 , 0.202, -0.099, 0.028, -0.020],
                "pickup": [0.447, -0.015, 0.108, -0.078, 0.121, -0.008]
            },
        },
        "SE": {
            "meta": "imaginary hotplate for now",
            "ned2": {
                "pickup_safe_height": [0.240, 0.061, 0.202, -0.037, 0.061, 0.046],
                "pickup": [0.233, 0.062, 0.113, -0.071, 0.076, 0.069]
            }
        }
    },
    "dosing_device": {
        "viperx": {
            "approach": [0.16402257, 0.34746304, 0.19],
            "pickup_safe_height": [0.16247981, 0.47495207, 0.19],
            "pickup": [0.15748769, 0.45, 0.10]
        }
    },
    "thermoshaker": {
        "viperx": {
            "pickup_safe_height": [0.51193886, -0.28478028,  0.21],
            "pickup": [0.51300577, -0.28429177,  0.11]
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
    # print(viperx.arm.get_ee_pose())
    # print(viperx.arm.get_joint_commands())
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
        # viperx.arm.go_to_home_pose()
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
        ned2.move_to_home_pose()
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
# TODO: could refactor these into one function, but do we want to keep fn names?
# TODO: could add a unique name/id to Vial and use getter to retrieve it for printing
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
        ned2.grasp_with_tool()
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
        ned2.release_with_tool()
        ned2.wait(1)
        ned2_move(ned2, pose["pickup_safe_height"],1)
        if "approach" in pose.keys():
            ned2_move(ned2, pose["approach"], 1)
    except Exception as e:
        sys.stderr.write(str(e))

# pose = [x,y,z,roll,pitch,yaw] where x/y/z are in m, roll/pitch/yaw are in radians
# TODO: should we support other types of moves?
def ned2_move(ned2, pose, delay):
    ned2.move_pose(pose)
    time.sleep(delay)

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
