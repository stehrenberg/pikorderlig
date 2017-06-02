# pikorderlig
A simple application for recording audio via linein, some fancy visualization with LEDs and a sleek web interface.

## Prerequisites
* Python 3.6.1 (see https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f)

## Setting up the project on the Pi
* clone the repo and copy it to your Pi
* install packages: ```apt-get install python3-pip libsndfile1 libffi-dev```
* if pip is already installed, you might need to upgrade it with ```pip install -U pip```
* install Pybuilder: ```python3.6 -m pip install pybuilder```
* run the project's build script with ```./pikorderlig/src/build.py``` (that installs additional dependencies)
* now you can run the software with ```./pikorderlig/src/pikorderlig.py```

## PIP
After installing Python 3.6.1, run the following commands:
* `sudo apt-get install python3-pip`
* `pip install -U pip`
* `ln -s /usr/local/bin/pip3.6 /usr/bin/pip`