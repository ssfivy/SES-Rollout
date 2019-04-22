#!/usr/bin/env python3
# Serial port interface (Dynet)

import logging

# third party libraries
import serial
import serial.tools.list_ports

class SerialOut():
    def __init__(self):
        self.all_ports = None
        self.active_port = None
        self.message = ''
        self.isText = True

    def __del__(self):
        if self.active_port is not None:
            self.active_port.close()

    def list_ports(self):
        ports = serial.tools.list_ports.comports()

        logging.info("Available comm ports")
        self.all_ports = []
        for port, desc, hwid in sorted(ports):
            logging.info(f"{port}: {desc} [{hwid}]")
            self.all_ports.append(port)

    def connect_port(self, port, speed=115200):
        if self.active_port is not None:
            self.active_port.close()
        self.active_port = serial.Serial(port, speed)
        logging.info(self.active_port)

    def announce(self, job=None):
        # job is unused, currently only for API compatibility
        if self.active_port is not None:
            logging.info('Sending to serial: "'+self.message+'"')
            if self.isText: # no conversion
                msg = bytearray(self.message, encoding='ascii')
            else: # Convert comma separated hex into bytes
                msg = bytes.fromhex(self.message.replace(' ,',''))
            self.active_port.write(msg)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    s = SerialOut()
    s.list_ports()
    s.connect_port(s.all_ports[0])
    s.announce()
    del s

