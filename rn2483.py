#!/usr/bin/python

# Apache License 2.0
# Copyright (c) 2019 Alexandros Antoniades

# Author: Alexandros Antoniades
# Date: 16/07/2019
# Description: Python library for RN2483 LoRaWAN transceiver
# This implementation is meant to be used with a Micropython implementation on Raspberry Pi, ESP32, PyBoard etc.
# Version: 0.1

# RN2483 documentation: https://ww1.microchip.com/downloads/en/DeviceDoc/40001784B.pdf

import time
import sys
import Crypto
from machine import UART, ADC, Pin, PWM
    
# Commands for RN2483 and RN2903 can be found in the product user guide by Microchip
COMMANDS = {
        "SYS_SLEEP": b"sys sleep {}",
        "SYS_RST": b"sys reset",
        "SYS_FACRST": b"sys factoryRESET",
        "SYS_ERASEFW": b"sys eraseFW",

        "SYS_VER": b"sys get ver",
        "SYS_VDD": b"sys get vdd",
        "SYS_HWEUI": b"sys get hweui",
        "SYS_NVMAT": b"sys get nvm {}",

        "SYS_NVMSET": b"sys set nvm {} {}",
        "SYS_PINCFG": b"sys set pindig {0} {1}",

        "MAC_RSTBAND": b"mac reset {}",
        "MAC_TX": b"mac tx {0} {1} {2}",
        "MAC_SAVE": b"mac save",
        "MAC_PAUSE": b"mac pause",
        "MAC_RESUME": b"mac resume",

        "MAC_DEVADDR": b"mac get devaddr",
        "MAC_DEVEUI": b"mac get deveui",
        "MAC_APPEUI": b"mac get appeui",
        "MAC_DR": b"mac get dr",
        "MAC_BAND": b"mac get band",
        "MAC_PWRIDX": b"mac get pwridx",
        "MAC_ADR": b"mac get adr",
        "MAC_RETX": b"mac get retx",
        "MAC_RXDELAY1": b"mac get rxdelay1",
        "MAC_RXDELAY2": b"mac get rxdelay2",
        "MAC_AR": b"mac get ar",
        "MAC_RX2": b"mac get rx2 {}",
        "MAC_DYCLEPS": b"mac get dcycleps",
        "MAC_MRGN": b"mac get mrgn",
        "MAC_GWNB": b"mac get gwnb",
        "MAC_STATUS": b"mac get status",

        "MAC_DEVADDRSET": b"mac set devaddr {}",
        "MAC_DEVEUISET": b"mac set deveui {}",
        "MAC_APPEUISET": b"mac set appeui {}",
        "MAC_NWKSKEYSET": b"mac set nwkskey {}",
        "MAC_APPSKEYSET": b"mac set appskey {}",
        "MAC_PWRIDXSET": b"mac set pwridx {}",
        "MAC_DRSET": b"mac set dr {}",
        "MAC_ADRSET": b"mac set adr {}",
        "MAC_BATSET": b"mac set bat {}",
        "MAC_RETXSET": b"mac set retx {}",
        "MAC_LINKCHKSET": b"mac set linkchk {}",
        "MAC_RXDELAY1SET": b"mac set rxdelay1 {}",
        "MAC_ARSET": b"mac set ar {}",
        "MAC_RXSET": b"mac set rx2 {0} {1}",
    }

class LoRa:
    
    def __init__(self, serial=None, debug=False):
        self.serial = serial
        self.debug = debug
        
        if self.serial == None:
            raise ValueError("Invalid serial connection")
        
    def serialConnection(self):
        return(self.serial)
    
    def closeConnection(self):
        return(self.serial.deinit())
    
    def execute(self, command):
        self.serial.write(command + "\r\n")
        response = str(self.serial.readline())
        if self.debug:
            print("Execute: {} Response: {}\r\n").format(command, response)
        return(response)
        
    def cmd(self, command):
        return execute(self.COMMANDS[str(command)])
        
    def version(self):
        return cmd()

def main():
    serial = UART(PORT, BAUDRATE)
    serial.init(BAUDRATE, bits=8, parity=None, stop=1)
    
    
    
if __name__ == "__main__":
    main()