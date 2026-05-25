from setuptools import find_packages, setup

package_name = "marine_ctrl"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jin",
    maintainer_email="ra2ric3@gmail.com",
    description="Simple ROS 2 Python publishers that drive a marine robot via cmd_vel.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "auto = marine_ctrl.auto_publisher:main",
            "keyboard = marine_ctrl.keyboard_publisher:main",
        ],
    },
)
