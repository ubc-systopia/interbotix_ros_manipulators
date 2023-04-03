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
# [x,y,z]
locations = {
    "grid": {
        "pickup_safe_height": [0.54, -0.00222128,  0.23],
        "pickup": [0.53,   0.00102628, 0.11]
    },
    "dosing_device": {
        "approach": [0.16402257, 0.34746304, 0.19],
        "pickup_safe_height": [0.16247981, 0.47495207, 0.19],
        "pickup": [0.15748769, 0.45, 0.10]
    },
    "thermoshaker": {
        "pickup_safe_height": [0.51193886, -0.28478028,  0.21],
        "pickup": [0.51300577, -0.28429177,  0.11]
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

def start_heating_soln(hotplate, start_temp, delay):
    print("[HOTPLATE]: Starting to heat solution...")
    hotplate.target_temperature = start_temp
    hotplate.start_heating()
    time.sleep(delay)
    vial.set_temp(start_temp)

def stop_stirring_soln(hotplate, end_stir_rate, delay):
    hotplate.target_stir_rate = end_stir_rate
    time.sleep(delay)
    hotplate.stop_stirring()
    print("[HOTPLATE]: Stopped stirring solution.")

def stop_heating_soln(hotplate, end_temp, delay):
    hotplate.target_temperature = end_temp
    time.sleep(delay)
    hotplate.stop_heating()
    print("[HOTPLATE]: Stopped heating solution.")
    vial.set_temp(end_temp)


### THERMOSHAKER
def start_shaking_soln(thermoshaker, speed, delay):
    thermoshaker.set_speed = speed
    print("[THERMOSHAKER]: Starting to shake solution...")
    thermoshaker.start_shaking()
    time.sleep(delay)

def start_tempering_soln(thermoshaker, temp, delay):
    thermoshaker.set_temperature = temp
    print("[THERMOSHAKER]: Starting to temper solution...")
    thermoshaker.start_tempering()
    time.sleep(delay)
    vial.set_temp(temp)

def stop_shaking_soln(thermoshaker):
    thermoshaker.stop_shaking()
    print("[THERMOSHAKER]: Stopped shaking solution.")

def stop_tempering_soln(thermoshaker):
    thermoshaker.stop_tempering()
    print("[THERMOSHAKER]: Stopped tempering solution.")


### VIPERX
# TODO: could refactor these into one function, but do we want to keep fn names?
def viperx_pick_up_object(viperx, pose, obj):
    print(f"\nPicking up {obj}.")
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
    print(f"Placing {obj}.\n")
    if "approach" in pose.keys():
        viperx_move(viperx, pose["approach"], 1)
    viperx_move(viperx, pose["pickup_safe_height"], 1)
    viperx_move(viperx, pose["pickup"], 1)
    viperx.gripper.open(delay=2)
    viperx_move(viperx, pose["pickup_safe_height"], 0)
    if "approach" in pose.keys():
        viperx_move(viperx, pose["approach"], 1)

def viperx_move(viperx, pose_key, delay):
    viperx.arm.set_ee_pose_components(x=pose_key[0], y=pose_key[1], z=pose_key[2])
    time.sleep(delay)


### NED2
def ned2_pick_up_object(ned2):
    RobotAxis = enums_communication.RobotAxis
    safe_height = 0.1 # meters
    try:
        ned2.open_gripper() # TODO: should be outside of fn?
        ned2.wait(1)
        ned2.grasp_with_tool()
        ned2.wait(1)
        ned2.shift_pose(RobotAxis.Z, safe_height)
    except Exception as e:
        sys.stderr.write(str(e))

def ned2_place_object(ned2):
    RobotAxis = enums_communication.RobotAxis
    safe_height = 0.1 # meters
    try:
        ned2.open_gripper()
        ned2.wait(1)
        ned2.shift_pose(RobotAxis.Z, safe_height)
    except Exception as e:
        sys.stderr.write(str(e))

"""
:param move_type: "pose" | "joints"
:param loc_start: PoseObject or list[float] of 6 joints or 6 coordinates (x,y,z,roll,pitch,yaw)
:param loc_end: PoseObject or list[float] of 6 joints or 6 coordinates (x,y,z,roll,pitch,yaw)
"""
def ned2_pick_and_place(ned2, move_type, start_loc, end_loc):
    RobotAxis = enums_communication.RobotAxis
    safe_height = 0.1 # meters
    try:
        # check if we need to move to safe height
        if ned2.get_pose().z <= safe_height:
            ned2.shift_pose(RobotAxis.Z, safe_height)
        ned2.move_pose(start_loc) if move_type == "pose" else ned2.move_joints(start_loc)
        ned2_pick_up_object(ned2)
        ned2.move_pose(end_loc) if move_type == "pose" else ned2.move_joints(end_loc)
        ned2_place_object(ned2)
    except Exception as e:
        sys.stderr.write(str(e))

class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

# TODO: add call to ViperX here, push to file instead of printing
def monitor_hardware(frame, event, arg):
    if event == "line":
        print(ned2.get_hardware_status())
    return monitor_hardware
