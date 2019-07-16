#!/usr/bin/python

# Apache License
# Copyright (c) 2019 Alexandros Antoniades

# Author: Alexandros Antoniades
# Date: 16/07/2019
# Description: Python library for RN2483 LoRaWAN transceiver
# Version: 0.1

# RN2483 documentation: https://ww1.microchip.com/downloads/en/DeviceDoc/40001784B.pdf

import time
import sys
import crypto
try:
    import RPi.GPIO as gpio
    dev_env = False
except(ImportError, RuntimeError):
    dev_env = True
    
    
class LoRa:
    def __init__(self):
        return(0)
    
    
    
class LoRaWAN:
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

    def __init__(self, port=None, debug=False):
        self.port = port
        self.debug = debug
        
        if self.port == None:
            raise ValueError("Invalid serial port")
        
        
        



def main():
    return(0)
    
    
if __name__ == "__main__":
    main()