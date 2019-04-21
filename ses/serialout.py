#!/usr/bin/env python3
# Serial port interface (Dynet)

# third party libraries
import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()

    print("Available comm ports")
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]") 

    return(ports)

def announce(job):
    pass
