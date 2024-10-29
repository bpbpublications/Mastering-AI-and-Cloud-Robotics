import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'service_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shakil',
    maintainer_email='shakil@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mqtt_bridge = service_robot.mqtt_bridge:main',
            'stats_publisher = service_robot.stats_publisher:main',
            'cmd_subscriber = service_robot.cmd_subscriber:main',
        ],
    },
)
