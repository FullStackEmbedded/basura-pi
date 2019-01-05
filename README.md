# basura-pi
A prototype trash can sensor for the FSE 2019 Basura Trash System, installed on a Raspberry Pi Zero WH.
For this prototype, an ultrasonic ranger is used as distance sensor.

A full documentation of the project can be found [here](
https://docs.google.com/document/d/14aZPNU4AN9pGmYlxhXt_9eWmgolxFtHpdMSF23xxXis/edit).

This manual assumes that the Raspberry Pi already has a operating system installed (e.g. Raspbian)
and connection to the internet.

## Installation

### Installing the sensor
For an installation manual on how to install the ultrasonic ranger sensor, see
[RpiAutonomousCar](https://github.com/FullStackEmbedded/RpiAutonomousCar) project.

### Setting up a Virtual Environment
Set up a virtual environment in the project directory, e.g. in your home directory under 
`~/basura-pi`

    % cd basura-pi
    % sudo apt install python3 python3-pip python3-tk
    % sudo pip3 install virtualenv
    % virtualenv venv -p python3
    % source venv/bin/activate

### Installing the requirements

    (venv) % pip3 install -r requirements.txt

### Installing the sensor driver
In order for the ultrasonic ranger sensor to work properly, a driver needs to be installed.
You can use the driver from the [RpiAutonomousCar](https://github.com/FullStackEmbedded/RpiAutonomousCar) project.
For convenience purposes,the installation wheel for the Raspberry Pi is already stored under 
`/wheels`.

    (venv) % pip3 install wheels/fse2017_robot-v0.1.0.tar.gz

      
## Usage

### Sensor Calibration
First, the sensor needs to be calibrated for the trash can and receive a UUID.
Run `calibration.py` interactively and follow the instructions.

    (venv) % python3 calibration.py

### Starting the Logger Daemon
Now the logger daemon can be started.

    (venv) % python3 main.py

### Starting the Reporter
Before starting the Reporter, change the `BASURA_SERVER` variable to point to the right host and port that you want to communicate with.
If not changed, this will interact with `localhost:8000`.

The Reporter is currently not a daemon but can be started as follows:

    (venv) % watch bash reporter.sh
