import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node

def generate_launch_description():

    package_name='ifscbot_two' #<--- CONFIRA SE ESTÁ CORRETO

    # 1. Inclui o Robot State Publisher (rsp.launch.py)
    # CORRETO: O notebook precisa saber a "forma" do robô (URDF) para o Rviz.
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )

    # (Joystick está comentado, ok)
    # joystick = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory(package_name),'launch','joystick.launch.py'
    #             )])
    # )

    # 2. Inclui o Twist Mux (Multiplexador de Velocidade)
    # CORRETO: O notebook vai receber comandos (teleop, etc)
    # e enviar um único comando seguro para o robô.
    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params],
            # Este é o remapping.
            # Ele pega a saída do twist_mux (no notebook) e envia
            # pela rede para o tópico do controlador (que está no RPi).
            remappings=[('/cmd_vel_out','/diffbot_base_controller/cmd_vel')]
        )

    # Este é o "local correto" para o seu teleop
    teleop_node = Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            output='screen',
            prefix='xterm -e',  # <-- Isso abre o teleop em um NOVO terminal
            parameters=[{'stamped': True}], # <-- O 'stamped:=True' que você descobriu!

            # Remapeia a saída do teleop para a ENTRADA 'teleop' do twist_mux
            # (Verifique o nome 'cmd_vel_teleop' no seu twist_mux.yaml!)
            remappings=[('/cmd_vel', 'cmd_vel_joy')]
    )

    # ... (aqui fica o código do rsp, twist_mux, teleop_node) ...

    # Define o caminho para o arquivo de configuração do Rviz
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare(package_name), "config", "main.rviz"]
    )

    # Cria o nó do Rviz2
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file]
    )

    # Lista final de nós para lançar no NOTEBOOK
    return LaunchDescription([
        rsp,
        # joystick,
        twist_mux,
        teleop_node,
        rviz_node
    ])