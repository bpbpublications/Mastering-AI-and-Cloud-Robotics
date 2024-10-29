import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'first_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        # (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
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
            "publisher = first_py_pkg.first_publisher:main",
            "listener = first_py_pkg.first_subscriber:main",
            "NodeWithParams = first_py_pkg.params:main",
            "AdditionService = first_py_pkg.addition_srv:main",
            "AdditionClient = first_py_pkg.addition_client:main",
            "CountdownServer = first_py_pkg.countdown_ac_server:main",
            "CountdownClient = first_py_pkg.countdown_ac_client:main",
           
        ],
    },
)
