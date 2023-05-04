# username = 'viperx'
username = 'cpsadmin'
import sys

sys.path.append(r'/home/{}/niraapad/'.format(username))

# Import the module
import niraapad.backends

from niraapad.lab_computer.niraapad_client import NiraapadClient

host = 'localhost'
port = '1337'
abstract = '/home/{}/niraapad/niraapad/sarwat/abstract_config_file_testbed.json'.format(username)
NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=abstract, domain_configdir=None)

# Unnecessary on ispy, using a local forked version of ika
# import os
# module_path = os.path.abspath('/home/viperx/Downloads/ika-master/')
# sys.path.append(module_path)

from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
sys.path.append(
    '/home/{}/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules'.format(username))
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial
from workflow_utils import setup_thermoshaker, viperx_pick_up_object, viperx_place_object, ned2_pick_up_object, ned2_place_object, start_stirring_soln, start_tempering_soln, stop_stirring_soln, stop_tempering_soln, disconnect_devices, locations


# Set vial locations
ned2_grid = locations["grid"]["NW"]["ned2"]
ned2_hotplate = locations["grid"]["SE"]["ned2"]
viperx_grid = locations["grid"]["NW"]["viperx"]
viperx_dosing_device = locations["dosing_device"]["viperx"]
viperx_thermoshaker = locations["thermoshaker"]["viperx"]


def rule1():
    # Rule 1
    viperx_pick_up_object(viperx,viperx_grid, "vial")
    viperx_place_object(viperx, viperx_dosing_device, "vial")    
    # Fail (dosing device door is closed)

def rule2():
    # Rule 2
    dosing_device.set_door("state", "open")
    viperx_pick_up_object(viperx,viperx_grid, "vial")
    viperx_place_object(viperx, viperx_dosing_device, "vial")
    dosing_device.set_door("state", "closed")
    # Fail (closing door on top of ViperX)

# TODO: Rule 3
def rule3():
    viperx.arm.set_ee_pose_components()
    # Fail (collision)

# TODO: Rule 4
def rule4():
    pass
    

def rule5():
    # Rule 5
    viperx_pick_up_object(viperx,workflow_utils.locations["grid"], "vial")
    viperx_place_object(viperx, workflow_utils.locations["thermoshaker"], "vial")
    viperx.arm.go_to_home_pose()
    start_shaking_soln(thermoshaker, 200, 2)
    # Fail (heating an empty vial)

def rule7():
    # Rule 7
    dosing_device.set_door("state", "open")
    viperx_pick_up_object(viperx,workflow_utils.locations["grid"], "vial")
    viperx_place_object(viperx, workflow_utils.locations["dosing_device"], "vial")    
    viperx.arm.go_to_home_pose()
    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=vial.get_volume)
    dosing_device.stop_action(delay=0)
    dosing_device.run_action(delay=3, quantity=5)
    # Fail (attempting to dose an already full vial)

def rule8():
    # Rule 8
    dosing_device.set_door("state", "open")
    viperx_pick_up_object(viperx,workflow_utils.locations["grid"], "vial")
    viperx_place_object(viperx, workflow_utils.locations["dosing_device"], "vial")  
    viperx.arm.go_to_home_pose()
    dosing_device.run_action(delay=3, quantity=5)
    # Fail (attempt to run action before closing door)

def rule9():
    # Rule 9
    dosing_device.set_door("state", "open")
    viperx_pick_up_object(viperx,workflow_utils.locations["grid"], "vial")
    viperx_place_object(viperx, workflow_utils.locations["dosing_device"], "vial")  
    viperx.arm.go_to_home_pose()
    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.set_door("state", "open")
    # Fail (attempt to open door before stopping action)


if __name__ == '__main__':
    # Initialize devices
    kwargs = {
            'port': 'COM8',
            'dummy': True,
        }
    global thermoshaker
    thermoshaker = Thermoshaker.create(**kwargs)
    workflow_utils.setup_thermoshaker(thermoshaker, 15.5, 30, 30)

    global hotplate
    port = 'COM5'
    hotplate = MockMagneticStirrer(device_port=port)
    
    dosing_device = SimulatedSmartDevice("Virtual Dosing Station", 
                                        {'plane': 'N', 'state': 'closed', 'move_time': 1}, 
                                        "dosing a vial")
 
    vial = Vial(10, 20)
    
    # Initialize robots
    global viperx
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    viperx.arm.go_to_home_pose()

    ned2_ip = "169.254.200.200"
    global ned2
    ned2 = tcp_client.NiryoRobot(ned2_ip)
    ned2.calibrate_auto()
    ned2.update_tool()
    ned2.move_to_home_pose()

    # Run test


    workflow_utils.disconnect_devices(hp=True, viperx=viperx, ned2=False)
    
    