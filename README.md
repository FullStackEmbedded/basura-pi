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

### Configuration
The frequency of fill state logging is configured in `settings.py`.
The frequency of reporting to the server is configured as a constant at the top of `reporter.sh`.
It should be noted that it may take several seconds to report a single fill state.
Therefore it is suggested to set the frequency of the fill state logger in the order of magnitude of minutes, not seconds.

### Sensor Calibration
First, the sensor needs to be calibrated for the trash can and receive a UUID.
Run `calibration.py` interactively and follow the instructions.

    (venv) % python3 calibration.py

### Starting the Logger
Now the Logger can be started.
Note that this does not automatically spawn a child process; instead, the process loops indefinitely.

    (venv) % python3 main.py

The Reporter should also be executed similarly so that the fill states are reported and the log is truncated.

    (venv) % ./reporter.sh
