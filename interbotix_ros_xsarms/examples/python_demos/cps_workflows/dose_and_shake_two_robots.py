import sys
username = 'cpsadmin'
# sys.path.append('/home/cpsadmin/niraapad/')

# Import the module
# import niraapad.backends
# from niraapad.lab_computer.niraapad_client import NiraapadClient

# host = 'localhost'
# port = '1337'
# abstract = '/home/cpsadmin/niraapad/niraapad/sarwat/abstract_config_file_testbed_two_coords.json'
# NiraapadClient.connect_to_middlebox(host=host, port=port, abstract_configdir=None, domain_configdir=None)


from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
from pyniryo import tcp_client
sys.path.append(
    '/home/{}/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_ws_toolbox/interbotix_ws_modules/src/interbotix_xs_modules'.format(username))
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial
from workflow_utils import setup_thermoshaker, viperx_pick_up_object, viperx_place_object, ned2_pick_up_object, ned2_place_object, start_stirring_soln, start_tempering_soln, stop_stirring_soln, stop_tempering_soln, disconnect_devices, locations


if __name__ == '__main__':
    # Initialize devices
    kwargs = {
            'port': 'COM8',
            'dummy': True,
        }
    global thermoshaker
    thermoshaker = Thermoshaker.create(**kwargs)
    setup_thermoshaker(thermoshaker, 15.5, 30, 30)
    
    global hotplate
    port = 'COM5'
    hotplate = MockMagneticStirrer(device_port=port)

    dosing_device = SimulatedSmartDevice("Virtual Dosing Station", {"plane": "N","state": "closed","move_time": 1},"dosing a vial")
 
    vial = Vial(10, 20)
    
    # Initialize robots
    global viperx
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()

   
   
    ned2_ip = "169.254.200.200"
    global ned2
    ned2 = tcp_client.NiryoRobot(ned2_ip)
    ned2.calibrate_auto()
    ned2.update_tool()
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
  

    # Set vial locations
    ned2_grid = locations["grid"]["NW"]["ned2"]
    ned2_hotplate = locations["grid"]["SE"]["ned2"]
    viperx_grid = locations["grid"]["NW"]["viperx"]
    viperx_dosing_device = locations["dosing_device"]["viperx"]
    viperx_thermoshaker = locations["thermoshaker"]["viperx"]

    # Start workflow
    dosing_device.set_door("state", "open")
    vial.decap_vial()

    viperx.arm.go_to_home_pose()
    viperx_pick_up_object(viperx, viperx_grid, vial)
    viperx_place_object(viperx, viperx_dosing_device, vial)
   
    
    viperx.arm.go_to_home_pose()
    

    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.stop_action(delay=0)
    dosing_device.set_door("state", "open")
    viperx_pick_up_object(viperx, viperx_dosing_device, vial)
    viperx_place_object(viperx, viperx_thermoshaker, vial)
    dosing_device.set_door("state", "closed")
    viperx.arm.go_to_home_pose()

    start_tempering_soln(thermoshaker, vial, 50, 2)
    stop_tempering_soln(thermoshaker)
    viperx_pick_up_object(viperx, viperx_thermoshaker, vial)
    viperx_place_object(viperx, viperx_grid, vial)
    viperx.arm.go_to_home_pose()
    viperx.arm.go_to_sleep_pose()

    ned2_pick_up_object(ned2, ned2_grid, vial)
    ned2_place_object(ned2, ned2_hotplate, vial)
    ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
    start_stirring_soln(hotplate, 200, 1)
    stop_stirring_soln(hotplate, 100, 1)
    ned2_pick_up_object(ned2, ned2_hotplate, vial)
    ned2_place_object(ned2, ned2_grid, vial)
    vial.cap_vial()
    
    disconnect_devices(hp=False, viperx=viperx, ned2=ned2)
  
