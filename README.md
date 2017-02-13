ABOUT
=====
The project was initiated by Jonathan Chiang (ADM-TW) and deligated to Maker's Club, aiming to deploy air quality sensors to Trend Micro's buildings to acquire real-time readings of,
- PM 2.5
- temperature
- humidity
- CO2 in ppm

We decided to use the following configuration,
- G3 PM 2.5 sensor (sold in Taobao, can be replaced by A4 or G5)
- SHT31 I2C sensor (precise temperature + humidity)
- SenseAir S8 (CO2)
- Nokia 5110 LCD as indicator and debugger
- Extra LED as a chasis indicator


PINOUT
======
We use Raspberry Pi Model B+.  Don't use Model A as the GPIO pins are not enough for extended use.

G3 PM 2.5
---------
G3 talks UART in 9600 N 8 1.  Connect the pins as (left RPi, right G3):
- 5V to Pin 1 (VIN)
- GND to Pin 2 (GND)
- RX to Pin 5 (TX)

SHT31
-----
SHT31 works on I2C.  Connect the pins as (left RPi, right LCD):
- 3V3 to VIN (can be 5V, but we used all 5V in our configuration)
- GND to GND
- SDA1 to SDA
- SCL to CLK

Nokia 5110 LCD
--------------
Copied from [https://learn.adafruit.com/nokia-5110-3310-lcd-python-library/usage](Adafruit Nokia 5110 Library), the pins are (left RPi, right LCD):
- 3.3V to VIN
- GND to GND
- GPIO23 to D/C
- GPIO24 to RST
- CE0 to CE
- SCLK to CLK
- MOSI to DIN

Indicator LED
-------------
Use normal 3.3V LED without resistor.  It's OK.
- GND to GND
- GPIO16 to VIN

SOFTWARE
========
It is necessary to enable I2C, SPI and GPIO support in Raspbian.  You should enable Serial, but there is something to patch.

1. Comment out `T0:23:respawn:/sbin/getty -L ttyAMA0` in `/etc/inittab`.
2. Remove `console=ttyAMA0,115200` in `/boot/cmdline.txt`.
3. Serial console is thus disabled.  Use HDMI.

```bash
sudo apt-get install python-pip python-dev build-essential python-imaging git
sudo pip install RPi.GPIO
git clone https://github.com/adafruit/Adafruit_Nokia_LCD.git
cd Adafruit_Nokia_LCD
sudo python setup.py install
```
