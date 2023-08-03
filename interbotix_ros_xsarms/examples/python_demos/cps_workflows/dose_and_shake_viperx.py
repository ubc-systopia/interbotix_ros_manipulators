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
# port = '1337'
# abstract = '/home/{}/niraapad/niraapad/sarwat/abstract_config_file_testbed_two_coords.json'.format(username)
# NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=abstract, domain_configdir=None)


from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
from pyniryo import tcp_client
sys.path.append(
    '/home/{}/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules'.format(username))
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial
from workflow_utils import setup_thermoshaker, viperx_pick_up_object, viperx_place_object, ned2_pick_up_object, ned2_place_object, start_stirring_soln, start_tempering_soln, stop_stirring_soln, stop_tempering_soln, disconnect_devices, locations
import time

# Set vial locations
viperx_grid = locations["grid"]["NW"]["viperx"]
viperx_dosing_device = locations["dosing_device"]["viperx"]
viperx_thermoshaker = locations["thermoshaker"]["viperx"]


def run_viperx(viperx):
    viperx.arm.go_to_sleep_pose()
    # First Time
    viperx.arm.go_to_home_pose()
    viperx_pick_up_object(viperx, viperx_grid, vial)
    viperx_place_object(viperx, viperx_thermoshaker, vial)
    viperx.arm.go_to_home_pose()

    start_tempering_soln(thermoshaker, vial, 50, 2)
    stop_tempering_soln(thermoshaker)

    viperx_pick_up_object(viperx, viperx_thermoshaker, vial)
    viperx_place_object(viperx, viperx_grid, vial)
    viperx.arm.go_to_home_pose()

    # Second Time
    viperx.arm.go_to_home_pose()
    viperx_pick_up_object(viperx, viperx_grid, vial)
    viperx_place_object(viperx, viperx_thermoshaker, vial)
    viperx.arm.go_to_home_pose()

    start_tempering_soln(thermoshaker, vial, 50, 2)
    stop_tempering_soln(thermoshaker)

    viperx_pick_up_object(viperx, viperx_thermoshaker, vial)
    viperx_place_object(viperx, viperx_grid, vial)
    viperx.arm.go_to_home_pose()

    # Third Time
    viperx.arm.go_to_home_pose()
    viperx_pick_up_object(viperx, viperx_grid, vial)
    viperx_place_object(viperx, viperx_thermoshaker, vial)
    viperx.arm.go_to_home_pose()

    start_tempering_soln(thermoshaker, vial, 50, 2)
    stop_tempering_soln(thermoshaker)

    viperx_pick_up_object(viperx, viperx_thermoshaker, vial)
    viperx_place_object(viperx, viperx_grid, vial)
    viperx.arm.go_to_home_pose()


if __name__ == '__main__':
    # Initialize devices
    kwargs = {
            'port': 'COM8',
            'dummy': True,
        }
    global thermoshaker
    thermoshaker = Thermoshaker.create(**kwargs)
    setup_thermoshaker(thermoshaker, 15.5, 30, 30)
    
    vial = Vial(10, 20)
    
    # Initialize robots
    global viperx
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    
    time.sleep(2)
    run_viperx(viperx)


    disconnect_devices(hp=False, viperx=viperx, ned2=False)