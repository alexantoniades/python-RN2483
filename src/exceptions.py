class LoRaException(Exception):
    '''Parent exception class for all module exceptions'''

class HostError(LoRaException):
    '''Error connecting to host device'''

class ConfigurationError(LoRaException):
    '''Error configuring host device'''

class TransmissionError(LoRaException):
    '''Error during LoRa transmission'''

class ReceptionError(LoRaException):
    '''Error during LoRa reception'''

class FileImportError(LoRaException):
    '''Error during file import'''