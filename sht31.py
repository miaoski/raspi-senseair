import smbus
from time import sleep

def read_sht31():
    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(0x44, 0x2c, [0x06])
    sleep(0.5)
    data = bus.read_i2c_block_data(0x44, 0x00, 6)
    temp = data[0] * 256 + data[1]
    cTemp = -45 + (175 * temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    return (cTemp, humidity)

if __name__ == '__main__':
    (t, h) = read_sht31()
    print 'Temperature = %.2f C' % t
    print 'Humidity    = %d %%RH' % h
