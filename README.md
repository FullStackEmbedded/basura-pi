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
    % sudo apt-get update && sudo apt-get upgrade
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


### Installing the bluetooth server
A large part of this documentation and the described code is from Levente Fuksz's great article
[*"Control a Raspberry Pi with Android Over Bluetooth"*](https://blog.iamlevi.net/2017/05/control-raspberry-pi-android-bluetooth/).

First, we have to install the necessary bluetooth libraries:

    % sudo apt-get install python-dev libbluetooth-dev
    % sudo pip3 install pybluez

> In addition, for the Python Bluetooth service to work, we will need to load the Serial Port Profile. 
This in turn requires the Bluetooth Daemon to run in compatibility mode. 
Start by editing the service startup parameters in its configuration file:

	% sudo nano /etc/systemd/system/dbus-org.bluez.service

> Just add a **-C** after **bluetoothd**. The line should look like below:

    ExecStart=/usr/lib/bluetooth/bluetoothd -C

> Now reload the service configuration and restart the Bluetooth service with the following two commands

    % sudo systemctl daemon-reload
    % sudo systemctl restart dbus-org.bluez.service

> Finally, you can now load the Serial Port profile by issuing:

    % sudo sdptool add SP

> You should get a **Serial Port service registered** message as a result, telling you that the operation was successful.

> We want to control a Raspberry Pi over Bluetooth without any other interaction. 
Therefore our Python script containing the Bluetooth service needs to start on boot. 
The best way we can achieve this is by creating a **systemd** unit file that will execute our script.

> Start by marking the Python script as executable

    % sudo chmod +x /home/pi/basura-pi/reporter.py
    
> First of all, create the systemd unit file

    % sudo nano /etc/systemd/system/basurareporter.service
    
> Paste in the following code
    
    [Unit]
    Description=Raspberry PI Bluetooth Server for Basura System
    After=bluetooth.target
     
    [Service]
    Type=simple
    User=root
    Group=root
    WorkingDirectory=/home/pi/basura-pi
    ExecStart=/home/pi/basura-pi/reporter.py -l /home/pi/basura-pi/reporter.log
     
    [Install]
    WantedBy=multi-user.target

> Now it is time to reload the systemd daemon configuration and enable the new service auto start.

    % sudo systemctl daemon-reload
    % sudo systemctl enable basurareporter.service

> Finally, in order to check if everything is fine you need to reboot your Raspberry Pi.

    % sudo reboot
    
> After the device has restarted check the status of the service using

    % sudo systemctl status basurareporter.service

> Our service should be marked as active (running).
You can also check the log file to see if it got created. 
The log file should state that the Bluetooth service is listening.

    % cat /home/pi/basura-pi/reporter.log


### Pair Bluetooth Devices

For the Pi to communicate with other devices, it needs to paired once. 
A description for manual pairing can be found 
[here](https://bluedot.readthedocs.io/en/latest/pairpipi.html#using-the-command-line).

**Tip:** The command `bluetoothctl` should be run as `sudo`.

## Usage

### Sensor Calibration
First, the sensor needs to be calibrated for the trash can and receive a UUID.
Run `calibration.py` interactively and follow the instructions.

    (venv) % python3 calibration.py

### Starting the Logger Daemon
Now the logger daemon can be started.

    (venv) % python3 main.py
