# serialendec.py
#
# OpenEAS serial ENDEC driver
#
# Author: Nate Sales

import requests
import serial


class SerialEndec:
    def __init__(self, id, port, server, baud=9600):
        self.id = str(id)
        self.server = server.strip("/")

        # Initialize the serial port
        try:
            self.serial = serial.Serial(port, baud)
        except serial.serialutil.SerialException as e:
            print("[ERROR] Connecting to ENDEC on " + port)
            print(e)
            exit()

        # Make sure the serial port is open
        if not ser.isOpen():
            print("[ERROR] Serial port " + device + " is not open.")
            exit(1)

        self.output = ""

    def monitor(self):
        if self.serial.inWaiting():
            line = self.serial.readline().decode()

            if line.startswith("<ENDECSTART>"):
                self.output = ""

            elif line.startswith("<ENDECEND>"):
                requests.post(server + "/report", data={"id": self.id, "message": output})

            else:
                self.output += line

        else:
            self.output = ""
