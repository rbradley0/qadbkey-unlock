#!/usr/bin/env python3
"""
File: qadbkey-unlock.py
Authors: hornetfighter515, FatherlyFox
Year: 2021
Version: 1.0
Credits: Original by igem, https://xnux.eu/devices/feature/qadbkey-unlock.c, https://xnux.eu/devices/feature/modem-pp.html
Description: Works to assist in unlocking of certain PinePhones.
P.S. Thankyou for making a functional script hornetfighter515 ❤
"""

import sys, logging, os

def generateUnlockKey(sn):
    """
    @param sn:  the serial number to generate an unlock key for
    """
    salt = "$1${0}$".format(sn)
    c = crypt("SH_adb_quectel", salt)
    print("Salt: {0}\nCrypt: {1}\nCode: {2}\n".format(salt, c, c[12:28]))
    return c[12:28]

def main():
    if len(sys.argv) != 2 or os.geteuid() != 0:
        print('This script must be run as a superuser, preferrably using \'sudo\'')
        print('USAGE: ./qadbkey-unlock.py <device:baudrate>')
        exit(1)
    else:
        s = None
        try:
            device_path = sys.argv[1].split(':')
            s = serial.Serial(port=device_path[0], baudrate=device_path[1], timeout=2)
            s.write(b'AT+QADBKEY?\r')
            adbkey = s.read_until('OK').decode().split('\r')
            adbkey = adbkey[2].strip('\n')[1:]
            c = generateUnlockKey(adbkey[9:])
            print('AT+QADBKEY="{0}"'.format(c))
            print('To enable ADB, run: (Modem will not sleep with ADB enabled; do \'sudo adb start-server\' after invoking this command.)')
            print('AT+QCFG="usbcfg",0x2C7C,0x125,1,1,1,1,1,1,0')
            print('To disable ADB, run: (Modem will not sleep with ADB enabled; do \'sudo adb kill-server\' before invoking this command.)')
            print('AT+QCFG="usbcfg",0x2C7C,0x125,1,1,1,1,1,0,0')
        except (SerialException, ValueError, IndexError) as e:
            logging.error(e)
        finally:
            if s.is_open and s != None:
                s.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    try:
        from crypt import crypt
        import serial
        from serial.serialutil import SerialException
        main()
    except ImportError as e:
        logging.error(e)
