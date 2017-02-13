# coding: utf-8
from time import sleep
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import Image
import ImageDraw
import ImageFont
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
disp.begin(contrast=60)

image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def clear():
    draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)

def text(x, y, text):
    draw.text((x, y), text, font=font)

def show(pm25=0, t=0, h=0, co2=0, loc='N/A'):
    clear()
    text(0, 0, 'PM2.5: %d' % pm25)
    text(0, 8, 'Temp %.1f C' % t)
    text(0, 16, 'Hum %d %%RH' % h)
    text(0, 24, 'CO2 %d ppm' % co2)
    text(0, 38, loc)
    disp.image(image)
    disp.display()

if __name__ == '__main__':
    show(42, 16.5, 56, 650, 'A19F Test')
