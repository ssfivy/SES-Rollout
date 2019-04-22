#!/usr/bin/env python3
# Serial port interface (Dynet)

import logging

# third party libraries
import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()

    logging.info("Available comm ports")
    for port, desc, hwid in sorted(ports):
        logging.info(f"{port}: {desc} [{hwid}]")

    return(ports)

def announce(job):
    pass
