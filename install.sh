#!/bin/bash
sudo apt-get install python-pip python-dev build-essential python-imaging git python-smbus i2c-tools supervisord
sudo pip install RPi.GPIO
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
cd ~
install -o 0 -g 0 -m 755 shutdown.py /usr/local/bin/shutdown.py
install -o 0 -g 0 -m 644 shutdown.conf /etc/supervisor/conf.d/shutdown.conf
install -o 0 -g 0 -m 644 pigpiod.conf /etc/supervisor/conf.d/pigpiod.conf
