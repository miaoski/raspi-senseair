from time import sleep
import crc16
import pigpio

s8_co2 = '\xfe\x04\x00\x03\x00\x01\xd5\xc5'
s8_abc = '\xfe\x03\x00\x1f\x00\x01\xa1\xc3'
s8_typeid_hi = '\xfe\x04\x00\x19\x00\x01\xf4\x02'
s8_typeid_lo = '\xfe\x04\x00\x1a\x00\x01\x04\x02'
s8_fwver = '\xfe\x04\x00\x1c\x00\x01\xe4\x03'
s8_id_hi = '\xfe\x04\x00\x1d\x00\x01\xb5\xc3'
s8_id_lo = '\xfe\x04\x00\x1e\x00\x01\x45\xc3'

RX = 20 # GPIO
TX = 21 # GPIO
# init software serial
pi = pigpio.pi()
pi.set_mode(RX, pigpio.INPUT)
pi.set_mode(TX, pigpio.OUTPUT)
try:
    pi.bb_serial_read_close(RX)
except:
    pass
pi.bb_serial_read_open(RX, 9600, 8)

def ser_write(data):
    pi.wave_add_new()
    pi.wave_add_serial(TX, 9600, data)
    wid = pi.wave_create()
    pi.wave_send_once(wid)
    while pi.wave_tx_busy():
        sleep(0.01)
    pi.wave_delete(wid)

def ser_read(n):
    # assume we read data at once
    (cnt, data) = pi.bb_serial_read(RX)
    return data

# Read sensor ID
def print_id():
    ser_write(s8_id_hi)
    sleep(.2)
    hi = ser_read(7)
    sleep(.2)
    ser_write(s8_id_lo)
    sleep(.2)
    lo = ser_read(7)
    sleep(.2)
    print 'Sensor ID: %02x%02x%02x%02x' % (hi[3], hi[4], lo[3], lo[4])

def print_fw_ver():
    # Read firmware version
    ser_write(s8_fwver)
    sleep(.2)
    fw = ser_read(7)
    sleep(.2)
    print 'Firmware: %d.%d' % (fw[3], fw[4])

def read_co2():
    try:
        ser_write(s8_co2)
        sleep(.2)
        d = ser_read(7)
        checksum = crc16.calcString(str(d[:5]), 0xffff)
        if checksum != d[5] + d[6] * 256:
            return None
        co2 = d[3] * 256 + d[4]
        return co2
    except Exception as e:
        print e
        pass

def close():
    pi.bb_serial_read_close(RX)
    pi.stop()

if __name__ == '__main__':
    print_id()
    print_fw_ver()
    try:
        while True:
            print read_co2()
            sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        close()
