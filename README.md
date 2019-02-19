# basura-trashcan
A prototype trash can sensor for the FSE 2019 Basura Trash System, installed on a Raspberry Pi Zero WH.
For this prototype, an ultrasonic ranger is used as distance sensor.

A full documentation of the project can be found [here](
https://docs.google.com/document/d/14aZPNU4AN9pGmYlxhXt_9eWmgolxFtHpdMSF23xxXis/edit).

This manual assumes that the Raspberry Pi already has a operating system installed (e.g. Raspbian)
and connection to the internet.

## Installation

### Installing the Sensor
For an installation manual on how to install the ultrasonic ranger sensor, see
[RpiAutonomousCar](https://github.com/FullStackEmbedded/RpiAutonomousCar) project.

The Basura trash can uses the ultrasonic sensor driver contained in that repository.
The `UltrasonicRanger` class from that package is used as a driver and is bundled in this repository under `wheels/fse2017_robot-v0.1.0.tar.gz`.
This class expects the ultrasonic sensor's trigger pin to be attached to the Pi's GPIO pin 15 and the echo pin to be attached to GPIO 14.
If you choose to use other pins, the class will need to be updated accordingly.

### Setting up a Virtual Environment
Set up a virtual environment in the project directory, e.g. in your home directory under 
`~/basura-trashcan`

    % cd basura-trashcan
    % sudo apt install python3 python3-pip python3-tk
    % sudo pip3 install virtualenv
    % virtualenv venv -p python3
    % source venv/bin/activate

### Installing the Requirements

    (venv) % pip3 install -r requirements.txt

### Installing the Sensor Driver
In order for the ultrasonic ranger sensor to work properly, a driver needs to be installed.
You can use the driver from the [RpiAutonomousCar](https://github.com/FullStackEmbedded/RpiAutonomousCar) project.
For convenience purposes,the installation wheel for the Raspberry Pi is already stored under 
`/wheels`.

    (venv) % pip3 install wheels/fse2017_robot-v0.1.0.tar.gz

### Sensor Calibration
First, the sensor needs to be calibrated for the trash can and receive a UUID.
Run `calibration.py` interactively and follow the instructions.

    (venv) % sudo venv/bin/python calibration.py

### Starting the Logger Manually
Now the Logger can be started manually for a first test.
Note that this does not automatically spawn a child process; instead, the process loops indefinitely.

    (venv) % sudo venv/bin/python main.py

### Starting the Reporter Manually
Before starting the Reporter, change the `BASURA_SERVER` variable to point to the right host and port that you want to communicate with.
If not changed, this will interact with `localhost:8000`.

The Reporter is currently not a daemon but can be started as follows:

    (venv) % bash reporter.sh

### Starting the Logger  on System Startup
In order for the logger daemon to start automatically on system startup, the logger needs to be registered in *systemd*.

First, make the logger daemon file executable:

    % sudo chmod +x /home/pi/basura-trashcan/main.py

Then create a systemd unit file:

    % sudo nano /etc/systemd/system/basura-trashcan.service

Paste the following content into the file:

    [Unit]
    Description=Logger Daemon of FSE Basura Trash Can System
    
    [Service]
    Type=simple
    User=root
    Group=root
    WorkingDirectory=/home/pi/basura-trashcan
    ExecStart=/home/pi/basura-trashcan/venv/bin/python /home/pi/basura-trashcan/main.py
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target


Reload the systemd daemon configuration and enable the new service auto start.

    % sudo systemctl daemon-reload
    % sudo systemctl enable basura-trashcan.service

Finally, in order to check if everything is fine you need to reboot your Raspberry Pi.

    % sudo reboot

After the device has restarted check the status of the service:

    % sudo systemctl status basura-trashcan.service


### Starting the Reporter on System Startup
Just like the logger daemon, the reporter can be configured to start automatically on system start.

First, make the reporter shell script executable:

    % sudo chmod +x /home/pi/basura-trashcan/reporter.sh

Then create a systemd unit file:

    % sudo nano /etc/systemd/system/basura-reporter.service

Paste the following content into the file:

    [Unit]
    Description =Reporter Script of FSE Basura Trash Can System
    After=basura-trashcan.target
    
    [Service]
    Type=simple
    User=root
    Group=root
    WorkingDirectory=/home/pi/basura-trashcan
    ExecStart=bash /home/pi/basura-trashcan/reporter.sh
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target


Reload the systemd daemon configuration and enable the new service auto start.

    % sudo systemctl daemon-reload
    % sudo systemctl enable basura-reporter.service

Finally, in order to check if everything is fine you need to reboot your Raspberry Pi.

    % sudo reboot

After the device has restarted check the status of the service:

    % sudo systemctl status basura-reporter.service


## Usage

### Configuration
The frequency of fill state logging is configured in `settings.py`.
The frequency of reporting to the server is configured as a constant at the top of `reporter.sh`.
It should be noted that it may take several seconds to report a single fill state.
Therefore it is suggested to **set the frequency of the fill state logger in the order of magnitude of minutes, not seconds**.
