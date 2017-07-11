"""
This component should read the messages sent from the receiving device to the serial port.
After receiving the message the data will be stored in the database. The Web App will
get that data and show it.
"""

import serial
import sys
import argparse
import config

from models import *

PACKET_LEN = 22

# create command line arguments parser
parser = argparse.ArgumentParser(
    description='To read data from the receiving device, using serial communication.')
# option to indicate the serial port
parser.add_argument(
    '--port', help="The serial port that the device is connected to (ex: /dev/ttyUSB0)")
# option to indicate the baud rate
parser.add_argument('--baud_rate', help="The baud rate of the serial connection (ex: 9600)")


def hexRepr (string) :
    """
    Represents the hexadecimal representation of a byte string
    """

    return "0x" + "".join("{:02x}".format(b) for b in string)


def getPacketComponents (packet) :
    """
    Split the packet(22 bytes) into it's components, according to the format:\n
    | reservoir id (2 bytes) | pH (4 bytes) | water level (4 bytes) | conductivity (4 bytes) |
    | salinity (4 bytes) | tds (4 bytes) |
    """

    try :
        result = {
            'reservoir'   : int(packet[0:2]),
            'pH'          : int(packet[2:6]),
            'waterLevel'  : int(packet[6:10]),
            'conductivity': int(packet[10:14]),
            'salinity'    : int(packet[14:18]),
            'tds'         : int(packet[18:22]),
        }
    except Exception as e:
        print("[main#getPacketComponents] packet with invalid format received: {}".format(e))
        return None
    
    return result


if __name__ == '__main__' :
    cmdArgs = parser.parse_args()
    # port and baud rate are required
    if cmdArgs.port == None or cmdArgs.baud_rate == None :
        print('both the serial port and the baud rate arguments are required.')
        parser.print_usage()
        sys.exit(1)

    print('App started...')
    
    serialCon = serial.Serial(cmdArgs.port, cmdArgs.baud_rate)  
    
    # read the serial port continuously        
    while true :
        packet = serialCon.read(PACKET_LEN)
        # split the packet into it's parts
        resultData = getPacketComponents(packet)
        if resultData is None :
            print("[main] unable to save this measuremet. Read {}".format(hexRepr(packet)))
        else :
            measurement = Measuremet(**resultData)
            # measurement.save()