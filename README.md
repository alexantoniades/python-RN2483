![pylint Score](https://mperlet.github.io/pybadge/badges/10.00.svg)
# Python library and tools for using RN2483 LoRaWAN Transceiver

| Compatible devices | Build Status |
| ------------------ | ------------ |
| Raspberry Pi 3B+   | [![Build Status](https://travis-ci.org/alexantoniades/python-RN2483.svg?branch=master)](https://travis-ci.org/alexantoniades/python-RN2483) |

## RN2483 to Raspberry Pi GPIO connection
| Pin | RN2483 | to | Pin | Raspberry Pi 3B+ |
| --- | ------ | -- | --- | ---------------- |
| [7] | UART_RX | -> | [14] | UART_TX0 |
| [6] | UART_TX | -> | [15] | UART_RX0 |

## How to use
When importing library as module, import pyserial and initialize a connection using your assigned serial interface (e.g /dev/ttyUSB0 - in ubuntu)
First, install pyserial
`pip3 install pyserial`
Import and initialize the module
```python
import pyserial
import rn2483

#define serial port and baudrate for rn2583 transceiver
PORT = "/dev/ttyUSB0"
BAUDRATE = 57600

# Initialize serial connection
uart = serial.Serial(PORT, BAUDRATE)
# Initialize transceiver
device = rn2483(connection=uart, debug=True)
# Check of device is initialized
print(device.connection.isOpen())
# Check hardware eui
print(device.hardware_eui())
```
Configure LoRaWAN - Authentication By Personalization
```python
device.config_lorawan(
    auth="abp", 
    nwskey=NetworkSessionKey, 
    appskey=ApplicationSessionKey, 
    devaddr=DeviceAddress)
```
Configure LoRaWAN - Over The Air Authentication
```python
device.config_lorawan(
    auth="otaa",
    appkey=ApplicationKey,
    appeui=ApplicationEUI)
```
Close connection
```python
device.close_connection()
```

