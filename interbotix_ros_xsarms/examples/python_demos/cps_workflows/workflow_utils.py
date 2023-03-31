import time
import sys
from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
from dummy import SimulatedSmartDevice, Vial

sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules')
from interbotix_xs_modules.arm import InterbotixManipulatorXS


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
    # viperx.arm.go_to_home_pose()

### SETUP + TEARDOWN
def setup_thermoshaker(thermoshaker, safety_temp, wd_1, wd_2):
    thermoshaker.watchdog_safety_temperature = safety_temp
    thermoshaker.start_watchdog_mode_1(wd_1)
    thermoshaker.start_watchdog_mode_2(wd_2)
    thermoshaker.switch_to_normal_operation_mode()
    print("Completed setting up thermoshaker.")

def initialize_devices(ts, hp, dosing, soln, soln_loc, robot):
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
        dosing_device = SimulatedSmartDevice("Virtual Dosing Station", 
                                             {'plane': 'N', 'state': 'closed', 'move_time': 1}, 
                                             None, None, "dosing a vial")
    if soln:
        global vial
        vial = Vial(5, soln_loc, 20)
    if robot:
        global viperx
        viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
        # viperx.arm.go_to_home_pose()

def disconnect_devices(hp, robot):
    if hp:
        hotplate.disconnect()
    if robot:
        viperx.arm.go_to_sleep_pose()


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
def move_object(viperx, start_positions, end_positions, object):
    viperx.gripper.open(delay=2)

    # Move to the start position and pick up object
    if object == "ring":
        pickup_keys = ["approach", "pickup", "pickup_safe_height"]
        dropoff_keys = ["pickup_safe_height", "pickup", "approach"]
    else:
        pickup_keys = ["pickup_safe_height", "pickup", "pickup_safe_height"]
        dropoff_keys = ["drop_off_safe_height", "drop_off", "drop_off_safe_height"]
    
    viperx.arm.set_joint_positions(joint_positions=start_positions.get(pickup_keys[0]), moving_time=3, accel_time=None, blocking=True)
    time.sleep(1)
    viperx.arm.set_joint_positions(joint_positions=start_positions.get(pickup_keys[1]), moving_time=1, accel_time=None, blocking=True)
    time.sleep(1)
    viperx.gripper.close(delay=2)
    viperx.arm.set_joint_positions(joint_positions=start_positions.get(pickup_keys[2]), moving_time=1, accel_time=None, blocking=True)

    # Move to the end position and place object
    viperx.arm.set_joint_positions(joint_positions=end_positions.get(dropoff_keys[0]), moving_time=3, accel_time=None, blocking=True)
    time.sleep(1)
    viperx.arm.set_joint_positions(joint_positions=end_positions.get(dropoff_keys[1]), moving_time=1, accel_time=None, blocking=True)
    time.sleep(1)
    viperx.gripper.open(delay=2)
    viperx.arm.set_joint_positions(joint_positions=end_positions.get(dropoff_keys[2]), moving_time=3, accel_time=None, blocking=True)

    if object == "vial":
        vial.set_location(end_positions)



def move_object_cart(viperx, start_positions, end_positions, object):
    viperx.gripper.open(delay=2)

    # Move to the start position and pick up object
    if object == "ring":
        pickup_keys = ["approach", "pickup", "pickup_safe_height"]
        dropoff_keys = ["pickup_safe_height", "pickup", "approach"]
    else:
        pickup_keys = ["pickup_safe_height", "pickup", "pickup_safe_height"]
        dropoff_keys = ["drop_off_safe_height", "drop_off", "drop_off_safe_height"]
    
    # pose = viperx.arm.convert_joint_positions_to_cartesian(start_positions.get(pickup_keys[0]))
    # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    # time.sleep(1)
    # pose = viperx.arm.convert_joint_positions_to_cartesian(start_positions.get(pickup_keys[1]))
    # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    # time.sleep(1)
    # viperx.gripper.close(delay=2)
    # pose = viperx.arm.convert_joint_positions_to_cartesian(start_positions.get(pickup_keys[2]))
    # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])


    # Move to the end position and place object
    # pose = viperx.arm.convert_joint_positions_to_cartesian(end_positions.get(dropoff_keys[0]))
    # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    # time.sleep(1)
    # pose = viperx.arm.convert_joint_positions_to_cartesian(end_positions.get(dropoff_keys[1]))
    # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    # time.sleep(1)
    # viperx.gripper.open(delay=2)
    # pose = viperx.arm.convert_joint_positions_to_cartesian(end_positions.get(dropoff_keys[2]))
    # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    
    # if object == "vial":
    #     vial.set_location(end_positions)

def viperx_pick_up_object(viperx, pose, obj):
    print(f"Picking up {obj}.")
    viperx.gripper.open(delay=2)
    if "approach" in pose.keys():
        viperx.arm.set_ee_pose_components(x=pose["approach"][0], y=pose["approach"][1], z=pose["approach"][2])
        time.sleep(1)
    viperx.arm.set_ee_pose_components(x=pose["pickup_safe_height"][0], y=pose["pickup_safe_height"][1], z=pose["pickup_safe_height"][2])
    time.sleep(1)
    viperx.arm.set_ee_pose_components(x=pose["pickup"][0], y=pose["pickup"][1], z=pose["pickup"][2])
    time.sleep(1)
    viperx.gripper.close(delay=2)
    viperx.arm.set_ee_pose_components(x=pose["pickup_safe_height"][0], y=pose["pickup_safe_height"][1], z=pose["pickup_safe_height"][2])
    if "approach" in pose.keys():
        viperx.arm.set_ee_pose_components(x=pose["approach"][0], y=pose["approach"][1], z=pose["approach"][2])
        time.sleep(1)

def viperx_place_object(viperx, pose, obj):
    print(f"Placing {obj}.\n")
    if "approach" in pose.keys():
        viperx.arm.set_ee_pose_components(x=pose["approach"][0], y=pose["approach"][1], z=pose["approach"][2])
        time.sleep(1)
    viperx.arm.set_ee_pose_components(x=pose["pickup_safe_height"][0], y=pose["pickup_safe_height"][1], z=pose["pickup_safe_height"][2])
    time.sleep(1)
    viperx.arm.set_ee_pose_components(x=pose["pickup"][0], y=pose["pickup"][1], z=pose["pickup"][2])
    time.sleep(1)
    viperx.gripper.open(delay=2)
    viperx.arm.set_ee_pose_components(x=pose["pickup_safe_height"][0], y=pose["pickup_safe_height"][1], z=pose["pickup_safe_height"][2])
    if "approach" in pose.keys():
        viperx.arm.set_ee_pose_components(x=pose["approach"][0], y=pose["approach"][1], z=pose["approach"][2])
        time.sleep(1)
    
    # if obj == "vial":
    #     vial.set_location(positions)
