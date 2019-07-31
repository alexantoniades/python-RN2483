class LoRaException(Exception):
    '''Parent exception class for all module exceptions'''
    pass


class ConnectionError(LoRaException):
    '''Error connecting to host device'''
    pass

class ConfigurationError(LoRaException):
    '''Error configuring host device'''
    pass

class TransmissionError(LoRaException):
    '''Error during LoRa transmission'''
    pass


class ReceptionError(LoRaException):
    '''Error during LoRa reception'''
    pass


class TimeoutError(LoRaException):
    '''LoRa module reception timeout error'''
    pass

class FileImportError(LoRaException):
    '''Error during file import'''
    pass
