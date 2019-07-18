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
    


class RN2483:
    # Commands for RN2483 and RN2903 can be found in the product user guide by Microchip
    COMMANDS = {
        # System commands
        "SYSTEM": {
            "SLEEP": "sys sleep {duration}",
            "RESET": "sys reset",
            "FACTORY_RESET": "sys factoryRESET",
            "ERASEFW": "sys eraseFW",
            "VERSION": "sys get ver",
            "VOLTAGE": "sys get vdd",
            "HWEUI": "sys get hweui",
            # Memory and I/O
            "NVM": {
                    "GET": "sys get nvm {address}",
                    "SET": "sys set nvm {address} {value}"
            },
            "PIN": {
                "GPIO0": "sys set pindig GPIO0 {state}",
                "GPIO1": "sys set pindig GPIO1 {state}",
                "GPIO2": "sys set pindig GPIO2 {state}",
                "GPIO3": "sys set pindig GPIO3 {state}",
                "GPIO4": "sys set pindig GPIO4 {state}",
                "GPIO5": "sys set pindig GPIO5 {state}",
                "GPIO6": "sys set pindig GPIO6 {state}",
                "GPIO7": "sys set pindig GPIO7 {state}",
                "GPIO8": "sys set pindig GPIO8 {state}",
                "GPIO9": "sys set pindig GPIO9 {state}",
                "GPIO10": "sys set pindig GPIO10 {state}",
                "GPIO11": "sys set pindig GPIO11 {state}",
                "GPIO12": "sys set pindig GPIO12 {state}",
                "GPIO13": "sys set pindig GPIO13 {state}",
                "GPIO14": "sys set pindig GPIO14 {state}"
                "UART_CTS": "sys set pindig UART_CTS {state}",
                "UART_RTS": "sys set pindig UART_RTS {state}"
            }
        },
        # LoRaWAN interface commands
        "MAC": {
            "RESET_BAND": "mac reset {band}",
            "TX": "mac tx {type} {portnumber} {data}",
            "SAVE": "mac save",
            "PAUSE": "mac pause",
            "RESUME": "mac resume",
            # LoRaWAN settings
            "DEVADDR": {
                    "GET": "mac get devaddr",
                    "SET": "mac set devaddr {address}"
            },
            "DEVEUI": {
                    "GET": "mac get deveui",
                    "SET": "mac set deveui {deveui}"
            },
            "APPEUI": {
                    "GET": "mac get appeui",
                    "SET": "mac set appeui {appeui}"
            },
            "DATARATE": {
                    "GET": "mac get dr",
                    "SET": "mac set dr {datarate}"
            },
            "BAND": "mac get band",
            "POWER_INDEX": {
                    "GET": "mac get pwridx",
                    "SET": "mac set pwridx {power_index}"
            },
            "ADAPTIVE_DATARATE": {
                    "GET": "mac get adr",
                    "SET": "mac set adr {datarate}"
            },
            "RETX": {
                    "GET": "mac get retx",
                    "SET": "mac set retx {retx}"
            },
            "RXDELAY1": {
                    "GET": "mac get rxdelay1",
                    "SET": "mac set rxdelay1 {delay}",
            },
            "RXDELAY2": "mac get rxdelay2",
            "AUTO_REPLY": {
                    "GET": "mac get ar",
                    "SET": "mac set ar {reply}",
            },
            "RX2": {
                    "GET": "mac get rx2 {band}",
                    "SET": "mac set rx2 {datarate} {frequency}",
            },
            "DYCLEPS": "mac get dcycleps",
            "MARGIN": "mac get mrgn",
            "GATEWAY_NUMBER": "mac get gwnb",
            "STATUS": "mac get status",
            "NWKSKEYSET": "mac set nwkskey {key}",
            "APPSKEYSET": "mac set appskey {key}",
            "BAT": "mac set bat {level}",
            "LINK_CKECK": "mac set linkchk {check}",
        }
        # Radio interface
        "RADIO": {
            "RX": "radio rx {size}",
            "TX": "radio tx {data}",
            "CW": "radio cw {state}",
            # Radio monitor
            "BT": {
                "GET": "radio get bt {value}",
                "SET": "radio set bt {value}",
            },
            "MODE": {
                "GET": "radio get mod {mode}",
                "SET": "radio set mod {mode}",
            },
            "FREQUENCY": {
                "GET": "radio get freq {frequency}",
                "SET": "radio set freq {frequency}"
            },
            "POWER": {
                "GET": "radio get pwr {level}",
                "SET": "radio set pwr {level}"
            },
            "SF": {
                "GET": "radio get sf {factor}",
                "SET": "radio set sf {factor}"
            },
            "AUTOFREQBAND": {
                "GET": "radio get afcbw {band}",
                "SET": "radio set afcbw {band}"
            },
            "RXBW": {
                "GET": "radio get rxbw {bandwidth}",
                "SET": "radio set rxbw {bandwidth}"
            },
            "BITRATE": {
                "GET": "radio get bitrate {bitrate}",
                "SET": "radio set bitrate {bitrate}"
            },
            "FREQDEV": {
                "GET": "radio get fdev {deviation}",
                "SET": "radio set fdev {deviation}"
            },
            "PREAMBLE": {
                "GET": "radio get prlen {preable}",
                "SET": "radio set prlen {preable}"
            },
            "CRC": {
                "GET": "radio get crc {status}",
                "SET": "radio set crc {status}"
            },
            "IQI": {
                "GET": "radio get iqi {status}",
                "SET": "radio set iqi {status}"
            },
            "CODING_RATE": {
                "GET": "radio get cr {rate}",
                "SET": "radio set cr {rate}"
            },
            "WATCHDOG": {
                "GET": "radio get wdt {length}",
                "SET": "radio set wdt {length}"
            },
            "SYNC": {
                "GET": "radio get sync {word}",
                "SET": "radio set sync {word}"
            },
            "BANDWIDTH": {
                "GET": "radio get bw {bandwidth}",
                "SET": "radio set bw {bandwidth}"
            }
        }
    }
    
    def __init__(self, serial=None, debug=False):
        self.serial = serial
        self.debug = debug
        
        if self.serial == None:
            raise ValueError("Invalid serial connection")
        
    # Get serial connection
    def serialConnection(self):
        return(self.serial)
    
    # Close serial connection
    def closeConnection(self):
        return(self.serial.deinit())
    
    # Pass and Execute command to device, return device response
    def execute(self, command):
        self.serial.write(bytes(command + "\r\n", "utf-8"))
        response = str((self.serial.readline()).decode("utf-8"))
        if self.debug:
            print("Execute: {command} Response: {response}\r\n").format(command=str(command), response=response)
        return(response)
    
    # Get device version
    def version(self):
        return(execute(self.COMMANDS["SYSTEM"]["VERSION"])
    
    # Get device voltage level
    def voltage(self):
        return(execute(self.COMMANDS["SYSTEM"]["VOLTAGE"]))
    
    # Get device hardware EUI
    def hardwareEUI(self):
        return(execute(self.COMMANDS["SYSTEM"]["HWEUI"]))
    
    # Get value at specific address (address in HEX)
    def getValueAtAddress(self, address):
        return(execute(self.COMMANDS["SYSTEM"]["NVM"]["GET"].format(address=str(address))))
    
    # Set a value at specific memory address (value in HEX)
    def setValueAtAddress(self, address, value):
        return(execute(self.COMMANDS["SYSTEM"]["NVM"]["SET"].format(address=str(address), value=str(value))))
        
    def setPin(self, pin, state):
        return(execute())

    # Set device to sleep for specific duration (duration in milliseconds)
    def sleep(self, duration):
        return(execute(self.COMMANDS["SYSTEM"]["SLEEP"].format(duration=str(duration)))
    
    # Set device to reset (ON OFF)
    def reset(self):
        return(execute(self.COMMANDS["SYSTEM"]["RESET"]))
    
    # Factory reset device
    def factoryReset(self):
        return(execute(self.COMMANDS["SYSTEM"]["FACTORY_RESET"]))
    
    # Change state of GPIO pin: 1 = UP, 0 = DOWN
    def setPin(self, pin, state):
        return(execute(self.COMMANDS["SYSTEM"]["PIN"][str(pin)].format(state=str(state))))
        
    
    
def main():
    
    uart1 = UART(PORT, BAUDRATE)
    uart1.init(BAUDRATE, bits=8, parity=None, stop=1)
    
    device = RN2483(serial=uart1, debug=True)
    
    
    
    
if __name__ == "__main__":
    main()