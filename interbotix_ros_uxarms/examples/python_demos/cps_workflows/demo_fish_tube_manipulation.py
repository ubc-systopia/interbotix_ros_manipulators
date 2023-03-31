import os
import sys
import time

module_path = os.path.abspath('/home/viperx/Desktop/CPS-Project/niraapad/')
sys.path.append(module_path)

# Import the module
import niraapad.backends

from niraapad.lab_computer.niraapad_client import NiraapadClient

host = 'localhost'
port = '1337'
# domain = '/home/cpsadmin/niraapad/niraapad/sarwat/testbed_domain_config_file_template.json'
NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=None, domain_configdir=None)


module_path = os.path.abspath('/home/viperx/Downloads/ika-master/')
sys.path.append(module_path)


from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer

sys.path.append(
    '/home/viperx/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules/src/interbotix_xs_modules/')
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial

grid_nw = dict([
    ('pickup_safe_height', [-0.3021942377090454, 0.07516506314277649, 0.5292233824729919, -0.0015339808305725455, -0.5476311445236206, 0.0]),
    ('pickup', [-0.3021942377090454, 0.40650492906570435, 0.6273981332778931, -0.0015339808305725455, -1.0047574043273926, 0.0]),
    ('drop_off_safe_height', [-0.30526217818260193, 0.0644271969795227, 0.5859806537628174, -0.0015339808305725455, -0.62126225233078, 0.0015339808305725455]),
    ('drop_off', [-0.30526217818260193, 0.4049709439277649, 0.6320000886917114, -0.0015339808305725455, -1.006291389465332, 0.0])
    ])

    
grid_ne = dict([
    ('pickup_safe_height', [0.11658254265785217, 0.012271846644580364, 0.6059224009513855, -0.0015339808305725455, -0.5629709362983704, 0.0015339808305725455]),
    ('pickup', [0.11811652034521103, 0.3666214048862457, 0.7086991667747498, -0.0015339808305725455, -1.0461748838424683, -0.0015339808305725455]),
    ('drop_off_safe_height', [0.11658254265785217, 0.012271846644580364, 0.6059224009513855, -0.0015339808305725455, -0.5629709362983704, 0.0015339808305725455]),
    ('drop_off', [0.11811652034521103, 0.3666214048862457, 0.7086991667747498, -0.0015339808305725455, -1.0461748838424683, -0.0015339808305725455])
    ])

grid_se = dict([
    ('pickup_safe_height', [0.15033012628555298, 0.3298058807849884, 0.3666214048862457, 0.25003886222839355, -0.6795535087585449, -0.19481556117534637]),
    ('pickup', [0.15033012628555298, 0.5460971593856812, 0.401902973651886, 0.19634954631328583, -0.898912787437439, -0.12732040882110596]),
    ('drop_off_safe_height', [0.15033012628555298, 0.3298058807849884, 0.3666214048862457, 0.25003886222839355, -0.6795535087585449, -0.19481556117534637]),
    ('drop_off', [0.15033012628555298, 0.5460971593856812, 0.401902973651886, 0.19634954631328583, -0.898912787437439, -0.12732040882110596]),
    ])

grid_sw = dict([
    ('pickup_safe_height', [-0.3911651074886322, 0.34821364283561707, 0.29452431201934814, -0.6151263117790222, -0.7086991667747498, 0.4862719178199768]),
    ('pickup', [-0.38963112235069275, 0.5767768025398254, 0.33900976181030273, -0.4862719178199768, -0.9403302669525146, 0.29759228229522705]),
    ('drop_off_safe_height', [-0.3911651074886322, 0.34821364283561707, 0.29452431201934814, -0.6151263117790222, -0.7086991667747498, 0.4862719178199768]),
    ('drop_off', [-0.38963112235069275, 0.5767768025398254, 0.33900976181030273, -0.4862719178199768, -0.9403302669525146, 0.29759228229522705]),
    ])


# Different functions to get/print position/location data
def get_pos_data():
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    # viperx.arm.go_to_sleep_pose()
    print(viperx.arm.get_ee_pose())
    print(viperx.arm.get_joint_commands())


### HOTPLATE
def start_stirring_soln(start_stir_rate, delay):
    print("[HOTPLATE]: Starting to stir solution...")
    hotplate.start_stirring()
    hotplate.target_stir_rate = start_stir_rate
    time.sleep(delay)


def start_heating_soln(start_temp, delay):
    print("[HOTPLATE]: Starting to heat solution...")
    hotplate.target_temperature = start_temp
    hotplate.start_heating()
    time.sleep(delay)
    vial.set_temp(start_temp)


def stop_stirring_soln(end_stir_rate, delay):
    hotplate.target_stir_rate = end_stir_rate
    time.sleep(delay)
    hotplate.stop_stirring()
    print("[HOTPLATE]: Stopped stirring solution.")


def stop_heating_soln(end_temp, delay):
    hotplate.target_temperature = end_temp
    time.sleep(delay)
    hotplate.stop_heating()
    print("[HOTPLATE]: Stopped heating solution.")
    vial.set_temp(end_temp)


### THERMOSHAKER
def start_shaking_soln(speed, delay):
    thermoshaker.set_speed = speed
    print("[THERMOSHAKER]: Starting to shake solution...")
    thermoshaker.start_shaking()
    time.sleep(delay)


def start_tempering_soln(temp, delay):
    thermoshaker.set_temperature = temp
    print("[THERMOSHAKER]: Starting to temper solution...")
    thermoshaker.start_tempering()
    time.sleep(delay)
    vial.set_temp(temp)


def stop_shaking_soln():
    thermoshaker.stop_shaking()
    print("[THERMOSHAKER]: Stopped shaking solution.")


def stop_tempering_soln():
    thermoshaker.stop_tempering()
    print("[THERMOSHAKER]: Stopped tempering solution.")


def move_object(start_positions, end_positions, object):
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


def disconnect_devices(hp, robot):
    if hp:
        hotplate.disconnect()
    if robot:
        viperx.arm.go_to_sleep_pose()


def setup_thermoshaker(safety_temp, wd_1, wd_2):
    thermoshaker.watchdog_safety_temperature = safety_temp
    thermoshaker.start_watchdog_mode_1(wd_1)
    thermoshaker.start_watchdog_mode_2(wd_2)
    thermoshaker.switch_to_normal_operation_mode()
    print("Completed setting up thermoshaker.")


def initialize_devices(ts, hp, dosing, soln, robot):
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
        vial = Vial(5, grid_nw, 20)
    if robot:
        global viperx
        viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
        viperx.arm.go_to_home_pose()


if __name__ == '__main__':
    start_coords= dict([
        ('approach', [0.6013205051422119, 0.5184855461120605, 0.6933593153953552, -0.003067961661145091, -1.147417664527893, -1.5999419689178467]),
        ('pickup', [0.6013205051422119, 0.6227962374687195, 0.5307573676109314, -0.003067961661145091, -1.101398229598999, -1.5999419689178467]),
        ('pickup_safe_height', [0.6013205051422119, 0.3834952116012573, 0.5414952039718628, -0.003067961661145091, -0.8513593673706055, -1.6030099391937256]),
    ])
    goal_coords= dict([
        ('approach', [-0.14879614114761353, 0.4325825870037079, 0.921922504901886, -0.7761942744255066, -1.3606410026550293, -1.4235341548919678]),
        ('pickup', [-0.04295146465301514, 0.4632622003555298, 0.7869321703910828, -0.6749515533447266, -1.2732040882110596, -1.3867186307907104]),
        ('pickup_safe_height', [-0.0644271969795227, 0.3405437469482422, 0.8252816796302795, -0.7148350477218628, -1.2072429656982422, -1.3268934488296509])
    ])

    # get_pos_data()
    # viperx.arm.go_to_sleep_pose()
    
    devices = {
        'ts': True,
        'hp': False,
        'dosing': True,
        'soln': True,
        'robot': True
    }

    initialize_devices(ts=devices['ts'], hp=devices['hp'], dosing=devices['dosing'], soln=devices['soln'], robot=devices['robot'])
    #initialize_devices(ts=False, hp=False, dosing=True, soln=False, robot=False)
    #exit()

    # Start demo
    dosing_device.set_door("state", "open")
    move_object(grid_nw, grid_sw, "vial")
    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.stop_action(delay=0)
    dosing_device.set_door("state", "open")
    move_object(grid_sw, grid_ne, "vial")
    dosing_device.set_door("state", "closed")
    viperx.arm.go_to_home_pose()
    start_shaking_soln(200, 2)
    move_object(start_coords, goal_coords, "ring")
    stop_shaking_soln()
    move_object(grid_ne, grid_nw, "vial")
    viperx.arm.go_to_home_pose()
    disconnect_devices(hp=devices['hp'], robot=devices['robot'])
    # End demo
    
    ### WORKFLOW:
    # initial vial position = grid_nw
    # dosing device opens door
    # move vial from grid_nw to dosing device (grid_sw)
    # dosing device closes door
    # call action add substance to vial
    # open dosing device door
    # move vial from dosing device (grid_sw) to grid_ne (thermoshaker)
    # close door
    # robot goes home
    # thermoshaker heats solution
    # robot performs tower of hanoi (one ring)
    # stop heating solution
    # robot moves vial from ts (grid_ne) into initial positon (grid_nw)
    