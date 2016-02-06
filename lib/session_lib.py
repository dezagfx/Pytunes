from PyQt5.QtCore import QSettings
from config import config

global settings
settings = QSettings()

def set_token(token):  
    settings.setValue('token', token)
    #settings.setValue('point_value', QPoint(10, 12))

    # This will write the setting to the platform specific storage.

def get_token():
    return settings.value('token' , type=str)



def del_token():
    settings.remove('token')