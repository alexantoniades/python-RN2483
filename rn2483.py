#!/usr/bin/python3
''' 
                      [ RN2483 Library ]
    Python library for RN2483 LoRaWAN transceiver
    This implementation is meant to be used on Raspberry Pi.
    [-------------------------------------------------------]
    Version:
    [0.1]:
        + Changes:
            - Completed command set dictionary
            - Added compatibility for Raspberry Pi 3B+
            - Added LoRaWAN configuration method
            - Added dbeug mode for terminal response
            - Used Pylint to improve quality of code
            - Added DOC stirngs to methods and global
        + TODO:
            - Add error handling
            - shrink for microcontrollers
            - Add ESP32 compatibility
'''
import os
import serial
from src.exceptions import *
from yaml import load, dump, Loader, Dumper
LICENSE = "Apache License 2.0 - Copyright (c) 2019 Alexandros Antoniades"
AUTHOR = "Alexandros Antoniades"
DESCRIPTION = "A python module for interfacing with the\r\n        RN2483 and RN2903 LoRaWAN transceiver"
COMPATIBLE = "- Raspberry Pi 3B+\r\n - Raspberry Pi 2\r\n - ESP32   (Coming soon) [micropython]\r\n - ESP8266 (Coming soon) [micropython]\r\n - PyBoard (Coming soon) [micropython]\r\n"
VERSION = "0.1"
DOC = {
    "UserGuide": "https://ww1.microchip.com/downloads/en/DeviceDoc/40001784B.pdf",
    "Datasheet": "http://ww1.microchip.com/downloads/en/devicedoc/50002346c.pdf"
}
GIT = "https://github.com/alexantoniades/python-RN2483"

INTRO = """
          Welcome to RN2483 Command-Line Interface
[----------------------------------------------------------]
        {description}
Version {version}
Github: {git}

Compatible with:
 {compatible}
Author: {author}
Github: {github}
License: {license}
    
Documentation can be found at:
Datasheet - {datasheet}
User Guide - {user_guide}
[----------------------------------------------------------]
""".format(
        description=DESCRIPTION,
        version=VERSION,
        git=GIT,
        compatible=COMPATIBLE,
        author=AUTHOR,
        github="https://github.com/alexantoniades",
        license=LICENSE,
        datasheet=DOC["Datasheet"],
        user_guide=DOC["UserGuide"]
)

PORT = "/dev/tty"
BAUDRATE = 57600
class Lora:
    """Commands for RN2483 and RN2903 can be found in the product user guide by Microchip"""
    
    
    
    def __init__(self, host=None, connection=None):
        ''' Class init, check if serial connection is open '''
        self.connection = connection
        self.host = host
        
        with open(os.path.join(os.path.dirname(__file__), 'src/commands.yml')) as file:
            self.commands = load(file, Loader=Loader)
            
        if self.connection is None:
            raise ConnectionError("Serial connection not defined")
        
    def serial_connection(self):
        ''' Serial connection info '''
        return(self.connection)
        
    def close_connection(self):
        ''' Close serial connection '''
        return(self.connection.close())
        
    def execute(self, command):
        ''' Passes and Executes command to device, returns devices response '''
        self.connection.write(bytes(str(command) + "\r\n", "utf-8"))
        response = (self.connection.readline()).decode("utf-8")
        return(response)
        
    def version(self):
        ''' Returns RN2483 version '''
        return(self.execute("sys get ver"))
        
    def voltage(self):
        ''' Returns RN2483 Voltage '''
        return(self.execute("sys get vdd"))
        
    def hardware_eui(self):
        ''' Returns RN2483 Hardware EUI '''
        return(self.execute("sys get hweui"))

    def reset(self):
        ''' Resets RN2483 '''
        return(self.execute("sys reset"))
        
    # Factory reset device
    def factory_reset(self):
        ''' Factory resets RN2483 '''
        return(self.execute("sys factoryRESET"))

    def get_value_at_address(self, address):
        ''' Returns value at memory address - address is in HEXadecimal'''
        return(self.execute("sys get nvm {0}".format(str(address))))
        
    def set_value_at_address(self, address, value):
        ''' Sets value at memory address - value and address are in HEXadecimal'''
        return(self.execute("sys set nvm {0} {1}".format(address, value)))
        
    def sleep(self, duration):
        ''' Sets device to sleep - duration is in milliseconds'''
        return(self.execute("sys sleep {0}".format(duration)))
        
    def set_pin(self, pin, state):
        ''' Sets state of GPIO pin (1 = UP / 0 = DOWN). GPIO is given as GPIO[0-14] '''
        if str(state) in ("high", "HIGH", "up", "UP", "true", "TRUE", "1"):
            return(self.execute("sys set pindig {0} {1}".format(str(pin), "1")))
        elif str(state) in ("low", "LOW", "down", "DOWN", "false", "FALSE", "0"):
            return(self.execute("sys set pindig {0} {1}".format(str(pin), "0")))
    
    def adaptive_datarate(self, state):
        ''' Sets the adaptive datarate to on or off '''
        return(self.execute("mac set adr {0}".format(str(state))))

    def snr(self):
        ''' Returns transceiver Signal to Noise ratio '''
        return(self.execute("radio get snr"))
    
    def send(self, data):
        ''' Send data '''
        self.execute("mac pause")
        return(self.execute("radio tx {0}".format(str((data.encode('utf-8')).hex()))))
        
    def receive(self):
        ''' Receive data '''
        self.execute("mac pause")
        self.execute("radio rx 0")
        return(str((self.connection.readline()).decode("utf-8")))

    def config(self, mode=None, auth=None, nwskey=None, 
                    appskey=None, devaddr=None, appkey=None, appeui=None):
        
        
        pass
         
def main():
    ''' Main function '''
    #print(INTRO)
    uart = serial.Serial(PORT, BAUDRATE)
    device = Lora(connection=uart)
    print(device.commands["SYSTEM"]["RESET"])

if __name__ == "__main__":
    main()
    