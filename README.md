ABOUT
=====
The project was initiated by Jonathan Chiang (ADM-TW) and deligated to Maker's Club, aiming to deploy air quality sensors to Trend Micro's buildings to acquire real-time readings of,
- PM 2.5
- temperature
- humidity
- CO2 in ppm

We decided to use the following configuration,
- G3 PM 2.5 sensor (sold in Taobao)
- SHT31 I2C sensor (precise temperature + humidity)
- SenseAir S8 (CO2)
- Nokia 5110 LCD as indicator and debugger
- Extra LED as a chasis indicator


PINOUT
======
G3 PM 2.5
---------

SHT31
-----

Nokia 5110 LCD
--------------
*N.B.* It is a known issue that the display buffer for Nokia 5110 LCD can be distorted.  Wait for next refresh.  The display should be automatically recovered.

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
