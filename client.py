# -*- coding: utf8 -*-
import logging
import sht31
import g3
from time import sleep
import s8
import indicator_led
import nokia5110

import requests
SERVER = 'http://10.1.68.62:8080/airmon'
TIMEOUT = 5

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

led_on = False
s8.print_id()
s8.print_fw_ver()

try:
    while True:
        indicator_led.ON()
        (t, h) = sht31.read_sht31()
        pm25 = g3.read_g3()
        co2 = s8.read_co2()
        indicator_led.OFF()
        data = {'pm25': pm25['pm25_cf'],
                't': t,
                'h': h,
                'co2': co2}
        logger.info(repr(data))
        loc = 'N/A'
        try:
            r = requests.post(SERVER, data=data, timeout=TIMEOUT)
            loc = r.text
            logger.debug('Get loc = %s', loc)
        except requests.exceptions.ConnectTimeout as e:
            logger.error('Connect timeout')
            loc = 'Net Timeout'
        except requests.exceptions.RequestException as e:
            logger.error(str(e))
            loc = 'Net Error'
        nokia5110.show(data, loc=loc)
        sleep(10)
except KeyboardInterrupt:
    logger.info('Bye')
finally:
    g3.close()
    s8.close()
