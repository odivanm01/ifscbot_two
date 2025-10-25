import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # 1. Encontrar o caminho para o *nosso* pacote (ifscbot_two)
    ifscbot_two_pkg = get_package_share_directory('ifscbot_two')

    # 2. Encontrar o caminho para o pacote da base (diffdrive_arduino)
    diffdrive_arduino_pkg = get_package_share_directory('diffdrive_arduino')

    # 3. Definir a ação de incluir o launch do Lidar (o seu rplidar.launch.py)
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ifscbot_two_pkg, 'launch', 'rplidar.launch.py')
        )
    )

    # 4. Definir a ação de incluir o launch da base (diffbot.launch.py)
    diffbot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(diffdrive_arduino_pkg, 'launch', 'diffbot.launch.py')
        )
    )

    # 5. Retornar a lista de launches para executar (Lidar e Base)
    return LaunchDescription([
        rplidar_launch,
        diffbot_launch
    ])