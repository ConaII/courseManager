import copy
from sty import fg

__VERSION__ = '2.0-beta'
__COLORS__ = True

def codeInit():
    global opticalsRT, codeList
    global keepAlive, restart, exitMenu, exitSubMenu, menu, menuFunc
    keepAlive, restart = True, False
    exitMenu, exitSubMenu = None, None
    menu, menuFunc = None, None
    opticalsRT = { # WARNING #
        "saveCfg": True,
        "loadCfg": True,
        "allowDev": True,
    }
    codeList = {
        "turnList": ["Mañana", "Tarde", "Noche"]
    }
    configInit()

def configInit():
    global defaultCfg, config
    defaultCfg = {
        "formats": {
            "sep": 1, # Thousands Separator
            "spaces": [1, 0], #Menu | Index
        },
        "OPCIONES": {
            "menuLogo": True,
            "debugMode": False,
            "clearMode": False,
        },
        "other": {
            "cmdColors": True,
            "forceColors": False,
        },
        "version": 1.0
    }
    config = copy.deepcopy(defaultCfg)
    refreshCfg()

def varsInit():
    global defaultVars, var, selected
    selected = [None, None]
    defaultVars = {
        "courses": {
            "1º2": {
                88_239_597: ["Barca Doe"],
                88_239_595: ["Beta Dami"],
                33_282_395: ["Randal Monroe"],
            },
            "2º1": {
                88_239_596: ["Alaba Doe"],
                33_282_394: ["Delta Mar"],
            },
            "3º2": {
                88_239_594: ["Carson Tano"],
                33_282_393: ["Jonna Cena"],
            },
            "4º14": {
                88_239_593: ["John Doe"],
                33_282_392: ["Janne Doe"],
            }
        },
        "turns": {
            "1º2": "Tarde",
            "2º1": "Mañana",
            "3º2": "Tarde",
            "4º14": "Noche",
        },
        "format": 1.0,
        "version": __VERSION__
    }
    var = copy.deepcopy(defaultVars)
    refreshVars()

def refreshVars():
    global var, courses, turns
    courses = var["courses"]
    turns = var["turns"]

def refreshCfg():
    global config, formats, OPCIONES
    formats = config["formats"]
    OPCIONES = config["OPCIONES"]