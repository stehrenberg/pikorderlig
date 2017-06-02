# pikorderlig
A simple application for recording audio via linein, some fancy visualization with LEDs and a sleek web interface.

## Prerequisites
* Python 3.6.1

## Setting up the project on the Pi
* clone the repo and copy it to your Pi
* install pip (the Python package manager): ```apt-get install python3-pip```
* if pip is already installed, you might need to upgrade it with ```pip install -U pip```
* install Pybuilder: ```pip install pybuilder```
* run the project's build script with ```./pikorderlig/src/build.py``` (that installs additional dependencies)
* now you can run the software with ```./pikorderlig/src/pikorderlig.py```
