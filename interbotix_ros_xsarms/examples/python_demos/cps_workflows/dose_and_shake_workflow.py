import sys
from ika.thermoshaker import Thermoshaker
from ika.magnetic_stirrer import MockMagneticStirrer
sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules/src/interbotix_xs_modules')
from arm import InterbotixManipulatorXS
from dummy import SimulatedSmartDevice, Vial
from workflow_utils import setup_thermoshaker, viperx_pick_up_object, viperx_place_object, start_shaking_soln, stop_shaking_soln, disconnect_devices, locations, get_viperx_gripper_state

if __name__ == '__main__':

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
    
    global viperx
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    
    
    viperx.arm.go_to_sleep_pose()
  
    viperx.arm.go_to_home_pose()
    viperx.arm.go_to_sleep_pose()
    exit()

    # Set vial locations
    grid_location = locations["grid"]["NW"]["viperx"]
    dosing_device_location = locations["dosing_device"]["viperx"]
    thermoshaker_location = locations["thermoshaker"]["viperx"]

    # Start workflow
    dosing_device.set_door("state", "open")
    viperx_pick_up_object(viperx, grid_location, vial)
    viperx_place_object(viperx, dosing_device_location, vial)
    
    viperx.arm.go_to_home_pose()

    dosing_device.set_door("state", "closed")
    dosing_device.run_action(delay=3, quantity=5)
    dosing_device.stop_action(delay=0)
    dosing_device.set_door("state", "open")

    viperx_pick_up_object(viperx, dosing_device_location, vial)
    viperx_place_object(viperx, thermoshaker_location, vial)

    
    viperx.arm.go_to_home_pose()
    dosing_device.set_door("state", "closed")

    start_shaking_soln(thermoshaker, 200, 2)
    stop_shaking_soln(thermoshaker)

    viperx_pick_up_object(viperx, thermoshaker_location, vial)
    viperx_place_object(viperx, grid_location, vial)
    
    viperx.arm.go_to_home_pose()
    disconnect_devices(hp=False, viperx=viperx, ned2=False)
  
    