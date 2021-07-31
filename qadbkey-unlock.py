#!/usr/bin/env python3
"""
File: qadbkey-unlock.py
Authors: hornetfighter515, FatherlyFox
Year: 2021
Version: 2.0
Credits: Original by igem, https://xnux.eu/devices/feature/qadbkey-unlock.c, https://xnux.eu/devices/feature/modem-pp.html
Description: Works to assist in unlocking ADB access for the PinePhone.
P.S. Thankyou for making a functional script hornetfighter515 ❤
"""
import logging, os, argparse

def generateUnlockKey(sn):
    """
    @param sn: the serial number to generate an unlock key for
    """
    salt = "$1${0}$".format(sn)
    c = crypt("SH_adb_quectel", salt)
    # print("Salt: {0}\nCrypt: {1}\nCode: {2}\n".format(salt, c, c[12:28]))
    return c[12:28]

def main():
    if os.geteuid() != 0:
        logging.error('This script must be run as a superuser, preferrably using \'sudo\'')
        exit(1)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dev', '--device', dest='device', required=True, help='Specify device location, e.g. /dev/ttyUSB2', type=str)
        parser.add_argument('-b', '--baud', '--baudrate', dest='baudrate', default=115200, required=False, help='Specify serial baudrate, default is 115200', type=int)
        parser.add_argument('-t', '--tout', '--timeout', dest='timeout', default=2, required=False, help='Specify serial timeout, default is 2', type=int)
        args = parser.parse_args()
        
        s = Serial()
        s.port = args.device
        s.baudrate = args.baudrate
        s.timeout = args.timeout
        
        try:
            s.open()
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
            if s.isOpen():
                s.close()
            else:
                logging.error("Serial object doesn't exist, no need to close.")

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.ERROR)
    try:
        from crypt import crypt
        from serial import Serial, SerialException
        main()
    except ImportError as e:
        logging.error(e)
