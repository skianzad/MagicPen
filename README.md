ReadMe

***************************************************************
Installing Bno055
When using a serial UART device with the Raspberry Pi you'll need to make sure you disable the kernel's use of the Pi's serial port.  Normally when the Pi kernel boots up it will put a login terminal on the serial port, however if you connect a device like the BNO055 to this serial port it will get confused by the login terminal.  Luckily it's easy to disable the kernel's use of the serial port by using the raspi-config tool.
To disable the kernel serial port connect to the Raspberry Pi in a terminal (using SSH) and launch the raspi-config tool by running:
$ sudo raspi-config
Navigate the menus to the interfacomg options-> P6  Serial option and when prompted if you want a login shell over the serial port select No.  Then select the Finish menu option to exit raspi-config.
To install the software for this project you'll need to make sure your Raspberry Pi is running the latest Raspbian operating system, or your BeagleBone Black is running the latest Debian operating system.  Make sure your board is connected to the internet through a wireless or wired network connection too.

Connect to your board in a command line terminal and run the following commands to install the necessary dependencies:

sudo apt-get install -y build-essential python-dev python-smbus python-pip git


***************************************************************
Installing pyqt4 
$ sudo apt-get update
$ sudo apt-get install qt4-default




***No need***
$ sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
If the system is not working at this level then do the following
QT Core needs to be installed with
$ sudo apt-get install qt5-default
You'll need to copy over sip and PyQt5 to your Raspberry Pi (I used SFTP). Just put the tar files someplace that you can get to them easily.
You'll need to extract each of them, using the tar command, with the -xzvf tag so you'll end up with tar -xzvf sip-4.19.1.tar.gz`for sip.
In each folder, you'll need to set up for the build. This is done by typing "python config.py" in each directory.
The contents of each directory needs to be built and installed, go to your sip folder and type "make" this will take a very long time. After it's through, type "sudo make install".
Now do the same thing in your PyQt5 directory.


****************************************************************************
Installing Bluepy

sudo apt-get install libgtk2.0-dev

sudo pip install bluepy
sudo python3 -m pip install bluepy




**********************To motors********************************
PWM1	= 	GPIO 18 (pin 12) 
PWM2	=	GPIO 13  (pin33) 
DIR1      =	GPIO  20
DIR2      =	GPIO  16
********************To the trackball********************************
UP 	=	GPIO  22 
DOWN	=	GPIO  23
LEFT	=	GPIO 27
RIGHT	= 	GPIO 17
BUTTON=	GPIO 24
VCC
Gnd

*******************To the orientation sensor********************************
SPI1 	=	GPIO  10
SPI2	=	GPIO  9
SPI3	= 	GPIO 11
VCC	=	3.3V (you do not need to connect it to 5Vs)
Gnd

