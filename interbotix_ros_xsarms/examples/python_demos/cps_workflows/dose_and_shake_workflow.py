username = 'viperx'
# username = 'cpsadmin'
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
import workflow_utils

if __name__ == '__main__':

    # Initialize devices
    kwargs = {
            'port': 'COM8',
            'dummy': True,
        }
    global thermoshaker
    thermoshaker = Thermoshaker.create(**kwargs)
    workflow_utils.setup_thermoshaker(thermoshaker, 15.5, 30, 30)
    
    dosing_device = SimulatedSmartDevice("Virtual Dosing Station", {"plane": "N","state": "closed","move_time": 1},"dosing a vial")
 
    vial = Vial(10, 20)
    
    global viperx
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    viperx.arm.go_to_home_pose()
    

    # Start demo
    dosing_device.set_door("state", "open")
    workflow_utils.viperx_pick_up_object(viperx,workflow_utils.locations["grid"], "vial")
    workflow_utils.viperx_place_object(viperx, workflow_utils.locations["dosing_device"], "vial")
    
    viperx.arm.go_to_home_pose()

    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.stop_action(delay=0)
    dosing_device.set_door("state", "open")
    workflow_utils.viperx_pick_up_object(viperx, workflow_utils.locations["dosing_device"], "vial")
    workflow_utils.viperx_place_object(viperx, workflow_utils.locations["thermoshaker"], "vial")
    viperx.arm.go_to_home_pose()
    dosing_device.set_door("state", "closed")

    workflow_utils.start_shaking_soln(thermoshaker, 200, 2)
    workflow_utils.stop_shaking_soln(thermoshaker)

    viperx.arm.go_to_home_pose()
    workflow_utils.viperx_pick_up_object(viperx, workflow_utils.locations["thermoshaker"], "vial")
    workflow_utils.viperx_place_object(viperx, workflow_utils.locations["grid"], "vial")
    
    viperx.arm.go_to_home_pose()
    workflow_utils.disconnect_devices(hp=False, viperx=viperx, ned2=False)
  
    