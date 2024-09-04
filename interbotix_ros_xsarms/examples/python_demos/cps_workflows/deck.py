#username = 'viperx'
username = 'cpsadmin'
import sys
# import time
sys.path.append(r'C:\Users\zswat\OneDrive\Desktop\PhD\Courses\CPSC538G\Project\niraapad')

# Import the module
import niraapad.backends

from niraapad.lab_computer.niraapad_client import NiraapadClient

host = 'localhost'
port = '1337'
abstract = r'C:\Users\zswat\OneDrive\Desktop\PhD\Courses\CPSC538G\Project\niraapad\niraapad\sarwat\configs_setups\abstract_config_file_testbed_two_coords.json'
NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=abstract, domain_configdir=None)

from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
# sys.path.append(
#     '/home/{}/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules'.format(username))
# from interbotix_xs_modules.arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial
from workflow_utils import setup_thermoshaker, viperx_pick_up_object, viperx_place_object, start_shaking_soln, stop_shaking_soln, disconnect_devices, locations, get_viperx_gripper_state


# Initialize devices
kwargs = {
            'port': 'COM8',
            'dummy': True,
        }
global thermoshaker
thermoshaker = Thermoshaker.create(**kwargs)
setup_thermoshaker(thermoshaker, 15.5, 30, 30)
    
dosing_device = SimulatedSmartDevice("Virtual Dosing Station", {"plane": "N","state": "closed","move_time": 1},"dosing a vial")
 
vial = Vial(10, 20)