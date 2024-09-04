import threading
from multiprocessing import Process
import os
import sys

#username = 'viperx'
username = 'cpsadmin'
sys.path.append(r'/home/{}/niraapad/'.format(username))

# Import the module
# import niraapad.backends
# from niraapad.lab_computer.niraapad_client import NiraapadClient

# host = 'localhost'
# port = '1338'
# abstract = '/home/{}/niraapad/niraapad/sarwat/abstract_config_file_testbed_two_coords.json'.format(username)
# NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=abstract, domain_configdir=None)


from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
from pyniryo import tcp_client
sys.path.append(
    '/home/{}/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules'.format(username))
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial
from workflow_utils import ned2_move, setup_thermoshaker, viperx_pick_up_object, viperx_place_object, ned2_pick_up_object, ned2_place_object, start_stirring_soln, start_tempering_soln, stop_stirring_soln, stop_tempering_soln, disconnect_devices, locations
import time

# Set vial locations
ned2_grid = locations["grid"]["NW"]["ned2"]
ned2_hotplate = locations["grid"]["SE"]["ned2"]
ned2_dosing_device = locations["dosing_device"]["ned2"]



def run_ned2(ned2):
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
    
    # First Time
    dosing_device.set_door("state", "open")
    ned2_pick_up_object(ned2, ned2_hotplate, vial)
    ned2_place_object(ned2, ned2_dosing_device, vial)
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])

    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.stop_action(delay=0)
    dosing_device.set_door("state", "open")
    
    
    ned2_pick_up_object(ned2, ned2_dosing_device, vial)
    ned2_place_object(ned2, ned2_hotplate, vial)
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
    start_stirring_soln(hotplate, 200, 1)
    stop_stirring_soln(hotplate, 100, 1)

    # Second Time
    dosing_device.set_door("state", "open")

    ned2_pick_up_object(ned2, ned2_hotplate, vial) 
    ned2_place_object(ned2, ned2_dosing_device, vial)
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])

    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.stop_action(delay=0)
    dosing_device.set_door("state", "open")
    
    
    ned2_pick_up_object(ned2, ned2_dosing_device, vial)
    ned2_place_object(ned2, ned2_hotplate, vial)
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
    start_stirring_soln(hotplate, 200, 1)
    stop_stirring_soln(hotplate, 100, 1)


if __name__ == '__main__':
    # Initialize devices
   
    global hotplate
    port = 'COM5'
    hotplate = MockMagneticStirrer(device_port=port)

    dosing_device = SimulatedSmartDevice("Virtual Dosing Station", {"plane": "N","state": "closed","move_time": 1},"dosing a vial")
 
    vial = Vial(10, 20)
  

    ned2_ip = "169.254.200.200"
    global ned2
    ned2 = tcp_client.NiryoRobot(ned2_ip)
    ned2.calibrate_auto()
    ned2.update_tool()
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
    exit()

    run_ned2(ned2)


    disconnect_devices(hp=False, viperx=False, ned2=ned2)