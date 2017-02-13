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

SensrAir S8
-----------
S8 uses a weird type of ModBus.  We used up onboard UART, so we have to use software serial.  It's 9600 N 8 1.
- 5V to G+ (upper)
- GND to G0 (lower)
- GPIO20 (soft RX) to TX (lower)
- GPIO21 (soft TX) to RX (upper)

Raspberry Pi
------------
To make it easy to assemble, please check the following pin-out.
```
SHT31_VIN          3V3  1 | 2  5V         S8_G+
SHT31_SDA      SDA I2C  3 | 4  5V         G3_VIN
SHT31_CLK      SCL I2C  5 | 6  GND        G3_GND
                 GPIO4  7 | 8  UART_TX
SHT31_GND          GND  9 | 10 UART_RX    G3_TX
                GPIO17 11 | 12 PCM_CLK
                GPIO27 13 | 14 GND        5110_GND
                GPIO22 15 | 16 GPIO23     5110_DC
5110_VIN           3V3 17 | 18 GPIO24     5110_RST
5110_DIN          MOSI 19 | 20 GND
                  MISO 21 | 22 GPIO25
5110_CLK       SPI_CLK 23 | 24 SPI_CE0    5110_CE
                   GND 25 | 26 SPI_CE1
                 ID_SD 27 | 28 ID_SC
                 GPIO5 29 | 30 GND        S8_G0
                 GPIO6 31 | 32 GPIO12
                GPIO13 33 | 34 GND        IND_LED_GND
                GPIO19 35 | 36 GPIO16     IND_LED_VIN
SHUTDOWN_SW     GPIO26 37 | 38 GPIO20     S8_TX
SHUTDOWN_SW        GND 39 | 40 GPIO21     S8_RX
```

External shutdown switch are defined to GPIO26.  Ground it to gracefully shutdown.

We have 10 GPIO left for further use.


CLIENT SIDE (Raspberry Pi)
==========================
It is necessary to enable I2C, SPI and GPIO support in Raspbian.  You should enable Serial, but there is something to patch.

1. Comment out `T0:23:respawn:/sbin/getty -L ttyAMA0` in `/etc/inittab`.
2. Remove `console=ttyAMA0,115200` in `/boot/cmdline.txt`.
3. Serial console is thus disabled.  Use HDMI.
4. Add `i2c-dev` to `/etc/modules`.
5. Install `pigpio` from joan2937 for software serial, and run `/usr/local/bin/pigpiod` when system boots.
6. Install software, run `./install.sh`

```bash
sudo apt-get install python-pip python-dev build-essential python-imaging git python-smbus i2c-tools supervisord
sudo pip install RPi.GPIO requests
cd ~/
git clone https://github.com/adafruit/Adafruit_Nokia_LCD.git
cd Adafruit_Nokia_LCD
sudo python setup.py install
echo 'i2c-dev' | sudo tee -a /etc/modules
cd ~/
git clone https://github.com/joan2937/pigpio
cd pigpio
make
sudo make install
```

Indicator LED uses `RPi.GPIO`, while software serial uses `pigpio`.  We use different package to prevent possible dysfunction of one or the other.

Security
--------
Better enable unattended update and disable `PasswordAuthentication` in `/etc/ssh/sshd_config`.


SERVER
======
Raspberry Pi posts the readings every 10 seconds to a C&C server.  The server locates at `http://10.1.148.5` (temporarily).
After POST, the server sends commands like "Indicator LED ON" or "Location is A19F Left".  Any more serious operation (like to change C&C IP) shall be done with `ssh -c`.

Setup SQLite3 database with `sqlite3 airmon.sq3 < schema.sql`.

DEPLOYMENT
==========
- Use pre-shared SSH key.
- Client IP and Mac shall be obtained by POST.
