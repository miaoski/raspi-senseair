import sht31
import g3
from time import sleep
import s8
import indicator_led
import nokia5110

try:
    while True:
        indicator_led.ON()
        (t, h) = sht31.read_sht31()
        print 'tmp: %.2f' % t
        print 'hum: %d' % h
        pm25 = g3.read_g3()
        print 'pm25: %d' % pm25['pm25_cf']
        co2 = s8.read_co2()
        print 'CO2: %d' % co2
        indicator_led.OFF()
        nokia5110.show(pm25=pm25['pm25_cf'], t=t, h=h, co2=co2, loc='A19F Test')
        sleep(10)
except KeyboardInterrupt:
    print 'Bye'
finally:
    g3.close()
    s8.close()
