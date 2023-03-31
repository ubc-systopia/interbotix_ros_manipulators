# import sys
# sys.path.append(r'/home/cpsadmin/niraapad/')

# import niraapad.backends
# from niraapad.lab_computer.niraapad_client import NiraapadClient

# host = 'localhost'
# port = '1337'
# # domain = '/home/cpsadmin/niraapad/niraapad/sarwat/testbed_domain_config_file_template.json'
# NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=None, domain_configdir=None)

import sys
sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules')
from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
from dummy import SimulatedSmartDevice, Vial
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import workflow_utils

# Irrelevant joint positions
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


def get_pos_data():
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    # print(viperx.arm.get_ee_pose())
    # print(viperx.arm.get_joint_commands())
    print(viperx.arm.get_cartesian_pose())
    # viperx.arm.go_to_home_pose()

if __name__ == '__main__':
    # Initializing devices
    devices = {
        'ts': False,
        'hp': False,
        'dosing': False,
        'soln': False,
        'robot': True
    }

    # TODO: push **kwargs changes in ika fork
    if devices['ts']:
        global thermoshaker
        kwargs = {
            'port': 'COM8',
            'dummy': True,
            # TODO
        }
        thermoshaker = Thermoshaker.create(**kwargs)
        workflow_utils.setup_thermoshaker(thermoshaker, 15.5, 30, 30)
    if devices['hp']:
        global hotplate
        port = 'COM5'
        hotplate = MockMagneticStirrer(device_port=port)
    if devices['dosing']:
        global dosing_device
        dosing_device = SimulatedSmartDevice("Virtual Dosing Station", 
                                             {'plane': 'N', 'state': 'closed', 'move_time': 1}, 
                                             None, #TODO 
                                             None, "dosing a vial")
    if devices['soln']:
        global vial
        vial = Vial(5, None, 20) #TODO
    if devices['robot']:
        global viperx
        viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")

    # PRINT LOC DATA
    print(viperx.arm.get_cartesian_pose())
    # viperx.arm.go_to_sleep_pose()
    # viperx.arm.go_to_home_pose()

    # Start demo
    # dosing_device.set_door("state", "open")
    # move_object(grid_nw, grid_sw, "vial")
    # viperx.arm.go_to_home_pose()
    # dosing_device.set_door("state", "closed")
    # dosing_device.run_action(delay=3, quantity=5)
    # dosing_device.stop_action(delay=0)
    # dosing_device.set_door("state", "open")
    # move_object(grid_sw, grid_ne, "vial")
    # dosing_device.set_door("state", "closed")
    # viperx.arm.go_to_home_pose()
    # start_shaking_soln(200, 2)
    # move_object(start_coords, goal_coords, "ring")
    # stop_shaking_soln()
    # move_object(grid_ne, grid_nw, "vial")
    # viperx.arm.go_to_home_pose()
    # disconnect_devices(hp=devices['hp'], robot=devices['robot'])
    # End demo
    