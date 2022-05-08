from setuptools import find_packages, setup

setup(
    name='netbox_config_manager',
    version='0.1',
    description='PLUGIN DESCRIPTION HERE',
    url='https://gitlab.init7.net/netbox/EDIT_URL_HERE',
    author='Jens Vogler',
    license='MIT',
    install_requires=[
        "ncclient>=0.6.13,<0.7",
        "pyang>=2.5,<3",
        "hvac>=0.11.2,<0.12"
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
