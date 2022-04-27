from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='TelegrammBot',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires = ["pyTelegramBotAPI~=4.4.0",
                        "setuptools>=49.2.1",
                        "sphinx~=4.2.0"],
    include_package_data=True,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'TelegrammBot'),
            'version': ('setup.py', '1.0'),
            'release': ('setup.py', '1.0'),
            'source_dir': ('setup.py', 'docs/source')}},
)
 
