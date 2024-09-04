import sys
sys.path.append(
    '/home/cpsadmin/interbotix_ws/src/interbotix_ros_toolboxes/interbotix_xs_toolbox/interbotix_xs_modules/src/interbotix_xs_modules')

from interbotix_xs_modules.arm import InterbotixManipulatorXS
from pyniryo import tcp_client, enums_communication
import numpy as np

if __name__ == '__main__':

    # Initialize robots
    
   

    
    ############################### Ned2 ##################################
    # print('Ned2')
    # ned2_ip = "169.254.200.200"
    # ned2 = tcp_client.NiryoRobot(ned2_ip)
    # # ned2.calibrate_auto()
    # # ned2.update_tool()
    # # ned2.enable_tcp(enable=True)
    # ned2.set_tcp([0.085,0,0,0,0,0])
    # # ned2.move_pose([0.1342,0.0000, 0.1650,-0.003, 1.001, 0.000])
    # ned2.move_pose([0.2878, -0.25, 0.3884, -0.0398, 0.1151, -0.7172])
    # print('Ned2 ', ned2.get_pose())
    ########################################################################

    ############################# ViperX ##################################
    # print('Viperx')
    # global_coords = [0.2729, -0.2364, 0.3244, -0.1912, -0.0561, -0.6507]
    viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    viperx.arm.go_to_sleep_pose()
    # viperx.arm.go_to_home_pose()
    # # pose = [0.3003, 0.2321, 0.2976, 0.0038, 0.0045, 0.7074]
    # # viperx.arm.set_ee_pose_components(x=pose[0], y=pose[1], z=pose[2])
    # print('ViperX coords: ', viperx.arm.get_cartesian_pose_gripper_tip())
    # print('Original coords: ', viperx.arm.get_cartesian_pose())
    #######################################################################



    #-------------------------------------------------------------------------#


    ##################### ViperX home coords ##################################
    # ViperX coords 1:  [0.5696, -0.0026, 0.4036, -0.0015, 0.0491, -0.0046]
    # ViperX coords 2: [0.5662, -0.0043, 0.4001, -0.0015, 0.0629, -0.0077]
    # Ned2 coords: [0.5049, 0.0273, 0.4265, -0.0902, -0.1347, 0.0525]
    ############################################################################


    ##################### Random point 1 #########################################
    # ViperX gripper link coords: [0.3003, 0.2321, 0.2976, 0.0038, 0.0045, 0.7074]
    # Viperx coords: [0.3227, 0.2513, 0.2975, 0.0038, 0.0045, 0.7074]
    # ned2 coords: [0.2729, -0.2364, 0.3244, -0.1912, -0.0561, -0.6507]
    #############################################################################


    #################### Random point 2 ##########################################
    # ViperX gripper link coords derived from inverse matrix: [0.3359,  0.2401,  0.30318]
    # ned2 coords : [0.2729, -0.2364, 0.3244, -0.1912, -0.0561, -0.6507]
    #############################################################################

   
    # translation_matrix = np.array([
    #         [0.0, -1, 0.0, 0.513],
    #         [1, 0.0, 0.0, -0.5723],
    #         [0.0, 0.0, 1.0, 0.02122],
    #         [0.0,0.0, 0.0, 1.0]

    #     ])

    # rotation_matrix = np.array([
    #     [0.0, -1, 0.0],
    #     [1, 0.0, 0.0],
    #     [0.0, 0.0, 1.0]
    # ])

    # viperx_coords = [0.5696, -0.0026, 0.4036, -0.0015, 0.0491, -0.0046]
    # convert_viperx_to_global_cartesian = np.dot(translation_matrix, [viperx_coords[0:3],1])
    # convert_viperx_to_global_rotation = np.dot(rotation_matrix, viperx_coords[3:6])

    # global_coords = convert_viperx_to_global_cartesian[0:3] +  convert_viperx_to_global_rotation
    # print(global_coords)

    

    # # viperx_coords = np.array([0.3227, 0.2513, 0.2975, 1])
    # convert_global_to_viperx = np.dot(inverse_matrix, global_coords)
    # print(convert_global_to_viperx)

    # transform_ee_gripper_link = np.array([
    #         [1.0, 0.0, 0.0, 0.0295],
    #         [0.0, 1.0, 0.0, 0.0],
    #         [0.0, 0.0, 1.0, 0.0],
    #         [0.0,0.0, 0.0, 1.0]

    # ])

    # get_viperx_gripper_link = np.dot(np.linalg.inv(transform_ee_gripper_link), convert_global_to_viperx)
    # print(get_viperx_gripper_link)

    # print('Viperx')
    # viperx = InterbotixManipulatorXS("vx300s", "arm", "gripper")
    # viperx.arm.set_ee_pose_components(x=get_viperx_gripper_link[0], y=get_viperx_gripper_link[1], z=get_viperx_gripper_link[2])
    # print('ViperX coords: ', viperx.arm.get_cartesian_pose_gripper_tip())
    



    ###################################### Misc calculation ###################################################    
    # print(np.average(np.array([-0.0256,-0.0268,-0.0273,0.0245,-0.0243,-0.0255,-0.0272,-0.0248,-0.0258,-0.0294])))
    # inverse_matrix = np.linalg.inv(translation_matrix)
    ##############################################################################################################




    










