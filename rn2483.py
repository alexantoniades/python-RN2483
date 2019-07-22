#!/usr/bin/python
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
            - Add micropython compatibility
            - Use Cement framework to create terminal application
            - Add error handling
'''
import serial
LICENSE = """
Apache License 2.0
Copyright (c) 2019 Alexandros Antoniades
"""
AUTHOR = "Alexandros Antoniades"
DESCRIPTION = """
                      [ RN2483 Library ]
    Python library for RN2483 LoRaWAN transceiver
    This implementation is meant to be used on Raspberry Pi.
    [-------------------------------------------------------]"""
VERSION = "0.1"
DOC = {
    "UserGuide": "https://ww1.microchip.com/downloads/en/DeviceDoc/40001784B.pdf",
    "Datasheet": "http://ww1.microchip.com/downloads/en/devicedoc/50002346c.pdf"
}
GIT = "https://github.com/alexantoniades/python-RN2483"
PORT = "/dev/tty"
BAUDRATE = 57600
class RN2483:
    # Commands for RN2483 and RN2903 can be found in the product user guide by Microchip
    COMMANDS = {
        # System commands
        "SYSTEM": {
            "SLEEP": "sys sleep {duration}",                    # duration = decimal [milliseconds]
            "RESET": "sys reset",                               
            "FACTORY_RESET": "sys factoryRESET",
            "ERASEFW": "sys eraseFW",
            "VERSION": "sys get ver",
            "VOLTAGE": "sys get vdd",
            "HWEUI": "sys get hweui",
            # Memory and I/O
            "NVM": {
                "GET": "sys get nvm {address}",             # address = Hexadecimal
                "SET": "sys set nvm {address} {value}"      # address, value = Hexadecimal
            },
            "PIN": {
                "GPIO0": "sys set pindig GPIO0 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO1": "sys set pindig GPIO1 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO2": "sys set pindig GPIO2 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO3": "sys set pindig GPIO3 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO4": "sys set pindig GPIO4 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO5": "sys set pindig GPIO5 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO6": "sys set pindig GPIO6 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO7": "sys set pindig GPIO7 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO8": "sys set pindig GPIO8 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO9": "sys set pindig GPIO9 {state}",        # state = 1 or 0 [HIGH or LOW]
                "GPIO10": "sys set pindig GPIO10 {state}",      # state = 1 or 0 [HIGH or LOW]
                "GPIO11": "sys set pindig GPIO11 {state}",      # state = 1 or 0 [HIGH or LOW]
                "GPIO12": "sys set pindig GPIO12 {state}",      # state = 1 or 0 [HIGH or LOW]
                "GPIO13": "sys set pindig GPIO13 {state}",      # state = 1 or 0 [HIGH or LOW]
                "GPIO14": "sys set pindig GPIO14 {state}",      # state = 1 or 0 [HIGH or LOW]
                "UART_CTS": "sys set pindig UART_CTS {state}",  # state = 1 or 0 [HIGH or LOW]
                "UART_RTS": "sys set pindig UART_RTS {state}"   # state = 1 or 0 [HIGH or LOW]
            }
        },
        # LoRaWAN interface commands
        "MAC": {
            "RESET_BAND": {
                "868": "mac reset 868",
                "433": "mac reset 433"
            },
            "TX": {
                "CONFIRMED": "mac tx cnf {portnumber} {data}",  # portnumber = decimal [1-223] 
                "UNCONFIRMED": "mac tx uncnf {portnumber} {data}" # data = Hexadecimal
            },
            "SAVE": "mac save",
            "PAUSE": "mac pause",
            "RESUME": "mac resume",
            # LoRaWAN settings
            "DEVADDR": {
                "GET": "mac get devaddr",
                "SET": "mac set devaddr {address}"          # address = Hexadecimal
            },
            "DEVEUI": {
                "GET": "mac get deveui",
                "SET": "mac set deveui {deveui}"            # deveui = 8-byte Hexadecimal        
            },
            "APPEUI": {
                "GET": "mac get appeui",
                "SET": "mac set appeui {appeui}"            # appeui = 8-byte Hexadecimal
            },
            "DATARATE": {
                "GET": "mac get dr",
                "SET": "mac set dr {datarate}"              # datarate = decimal [0-7]
            },
            "BAND": "mac get band",
            "POWER_INDEX": {
                "GET": "mac get pwridx",
                "SET": "mac set pwridx {powerindex}"       # powerindex = decimal [0-5]
            },
            "ADAPTIVE_DATARATE": {
                "GET": "mac get adr",
                "SET": "mac set adr {state}"                # state = on or off
            },
            "RETX": {
                "GET": "mac get retx",
                "SET": "mac set retx {retx}"                # retx = decimal [0-255]
            },
            "RXDELAY1": {
                "GET": "mac get rxdelay1",
                "SET": "mac set rxdelay1 {delay}"           # delay = decimal [milliseconds][0-65535]
            },
            "RXDELAY2": "mac get rxdelay2",
            "AUTO_REPLY": {
                "GET": "mac get ar",
                "SET": "mac set ar {reply}"                 # reply = on or off
            },
            "RX2": {
                "GET": "mac get rx2 {band}",                # decimal [868 or 433]
                "SET": "mac set rx2 {datarate} {frequency}" # datarate, frequency = decimal [0-7], [863000000-870000000] or [433050000-434790000]
            },
            "DYCLEPS": "mac get dcycleps",
            "MARGIN": "mac get mrgn",
            "GATEWAY_NUMBER": "mac get gwnb",
            "STATUS": "mac get status",
            "JOIN": "mac join {mode}",                          # mode = otaa or abp
            "NWKSKEY": "mac set nwkskey {key}",              # key = 16-byte Hexadecimal
            "APPSKEY": "mac set appskey {key}",              # key = 16-byte Hexadecimal
            "APPKEY": "mac set appkey {key}",                # key = 16-byte Hexadecimal
            "BAT": "mac set bat {level}",                       # level = decimal [0-255]
            "LINK_CKECK": "mac set linkchk {check}"             # check = decimal [0-65535]
        },
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
    def __init__(self, connection=None, debug=False):
        ''' Class init, check if serial connection is open '''
        self.connection = connection
        self.debug = debug
        if self.connection is None:
            raise ValueError("Invalid serial connection")
    # Get serial connection
    def serial_connection(self):
        ''' Serial connection info '''
        return(self.connection)
    # Close serial connection
    def close_connection(self):
        ''' Close serial connection '''
        return(self.connection.deinit())
    # Pass and Execute command to device, return device response
    def execute(self, command):
        ''' Passes and Executes command to device, returns devices response '''
        self.connection.write(bytes(str(command) + "\r\n", "utf-8"))
        response = (self.connection.readline()).decode("utf-8")
        if self.debug:
            print("Execute: {command} Response: {response}\r\n".format(command=command, response=response))
        return(response)
    # Get device version
    def version(self):
        ''' Returns RN2483 version '''
        return(self.execute(self.COMMANDS["SYSTEM"]["VERSION"]))
    # Get device voltage level
    def voltage(self):
        ''' Returns RN2483 Voltage '''
        return(self.execute(self.COMMANDS["SYSTEM"]["VOLTAGE"]))
    # Get device hardware EUI
    def hardware_eui(self):
        ''' Returns RN2483 Hardware EUI '''
        return(self.execute(self.COMMANDS["SYSTEM"]["HWEUI"]))
    # Get value at specific address (address in HEX)
    def get_value_at_address(self, address):
        ''' Returns value at memory address '''
        return(self.execute(self.COMMANDS["SYSTEM"]["NVM"]["GET"].format(address=str(address))))
    # Set a value at specific memory address (value in HEX)
    def set_value_at_address(self, address, value):
        ''' Sets value at memory address '''
        return(self.execute(self.COMMANDS["SYSTEM"]["NVM"]["SET"].format(address=str(address), value=str(value))))
    # Set device to sleep for specific duration (duration in milliseconds)
    def sleep(self, duration):
        ''' Sets device to sleep '''
        return(self.execute(self.COMMANDS["SYSTEM"]["SLEEP"].format(duration=str(duration))))
    # Set device to reset (ON OFF)
    def reset(self):
        ''' Resets RN2483 '''
        return(self.execute(self.COMMANDS["SYSTEM"]["RESET"]))
    # Factory reset device
    def factory_reset(self):
        ''' Factory resets RN2483 '''
        return(self.execute(self.COMMANDS["SYSTEM"]["FACTORY_RESET"]))
    # Change state of GPIO pin: 1 = UP, 0 = DOWN
    def set_pin(self, pin, state):
        ''' Sets state of GPIO pin '''
        return(self.execute(self.COMMANDS["SYSTEM"]["PIN"][str(pin)].format(state=str(state))))
    # Setup LoRaWAN client     
    def config_lorawan(self, auth=None, nwkskey=None, appskey=None, appkey=None, appeui=None, devaddr=None, power=14):
        ''' Configures LoRaWAN functionlity to specified autorization method '''
        if auth in ("ABP", "abp"):
            if self.debug:
                print("Initializing LoRaWAN - Authorization = ABP")
            self.execute(self.COMMANDS["SYSTEM"]["HWEUI"])
            if self.debug:
                print("Configuring Network Session Key - Key: {nwkskey}".format(nwkskey=nwkskey))
            self.execute(self.COMMANDS["MAC"]["NWKSKEY"].format(key=nwkskey))
            if self.debug:
                print("Configuring Application Session Key - Key: {appskey}".format(appskey=appskey))
            self.execute(self.COMMANDS["MAC"]["APPSKEY"].format(key=appskey))
            if self.debug:
                print("Configuring Device Address - Address: {devaddr}".format(devaddr=devaddr))
            self.execute(self.COMMANDS["MAC"]["SET"]["DEVADDR"].format(address=devaddr))
            if self.debug:
                print("Configuring Adaptive Data Rate")
            self.execute(self.COMMANDS["MAC"]["SET"]["ADAPTIVE_DATARATE"].format(state="on"))
            if self.debug:
                print("Setting transmit power to {power}".format(power=str(power)))
            self.execute(self.COMMANDS["RADIO"]["POWER"]["SET"].format(level=str(power)))
            if self.debug:
                print("Saving configuration")
            self.execute(self.COMMANDS["MAC"]["SAVE"])
            if self.debug:
                print("Joining...")
            self.execute(self.COMMANDS["MAC"]["JOIN"].format(mode="abp"))
        elif auth in ("OTAA", "otaa"):
            if self.debug:
                print("Initializing LoRaWAN - Authorization = OTAA")
            self.execute(self.COMMANDS["SYSTEM"]["HWEUI"])
            if self.debug:
                print("Configuring Application Key - Key: {appkey}".format(appkey=appkey))
            self.execute(self.COMMANDS["MAC"]["APPKEY"].format(key=appkey))
            if self.debug:
                print("Configuring Application EUI - Key: {appeui}".format(appeui=appeui))
            self.execute(self.COMMANDS["MAC"]["SET"]["APPEUI"].format(appeui=appeui))
            if self.debug:
                print("Saving configuration")
            self.execute(self.COMMANDS["MAC"]["SAVE"])
            if self.debug:
                print("Joining...")
            self.execute(self.COMMANDS["MAC"]["JOIN"].format(mode="otaa"))
        else:
            print("Error with LoRaWAN configuration")
def info():
    ''' Returns Library info '''
    return("""
{description}

By {author}
Version: {version}
Github repository can be found at {github}

{license}
    """.format(description=DESCRIPTION, author=AUTHOR, version=VERSION, github=GIT, license=LICENSE))
def main():
    ''' Main function '''
    uart = serial.Serial(PORT, BAUDRATE)
    device = RN2483(connection=uart, debug=True)
    print(info())
    print(device)
    uart.close()
if __name__ == "__main__":
    main()
    