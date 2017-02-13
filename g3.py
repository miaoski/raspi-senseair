import serial
from time import sleep

g3 = serial.Serial('/dev/ttyAMA0', baudrate=9600)

def g3_checksum(d):
    exp = ord(d[22]) * 256 + ord(d[23])
    c = 0
    for i in range(22):
        c += ord(d[i])
    return exp == c

def read_g3():
    while True:
        x = g3.read()
        if x != 'B': continue
        x = g3.read()
        if x != 'M': continue
        data = 'BM' + g3.read(22)
        if not g3_checksum(data):
            print 'Invalid checksum'
            sleep(1)
            continue
        pm10_cf  = ord(data[4]) * 256 + ord(data[5])
        pm25_cf  = ord(data[6]) * 256 + ord(data[7])
        pm100_cf = ord(data[8]) * 256 + ord(data[9])
        pm10     = ord(data[10]) * 256 + ord(data[11])
        pm25     = ord(data[12]) * 256 + ord(data[13])
        pm100    = ord(data[14]) * 256 + ord(data[15])
        return {'pm10_cf': pm10_cf,
                'pm25_cf': pm25_cf,
                'pm100_cf': pm100_cf,
                'pm10': pm10,
                'pm25': pm25,
                'pm100': pm100}

def close():
    g3.close()

if __name__ == '__main__':
    x = read_g3()
    print 'pm25_cf = %d, pm25 = %d' % (x['pm25_cf'], x['pm25'])
