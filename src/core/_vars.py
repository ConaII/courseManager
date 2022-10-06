import copy

__VERSION__ = '1.0-rc'
__COLORS__ = True

def codeInit():
    global opticalsRT
    global keepAlive, restart, exitMenu, exitSubMenu, menu, menuFunc
    keepAlive, restart = True, False
    exitMenu, exitSubMenu = None, None
    menu, menuFunc = None, None
    opticalsRT = { # WARNING #
        "saveCfg": True,
        "loadCfg": True,
        "allowDev": True,
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
            "clearMode": True,
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
            "1º1": {},
            "2º2": {},
            "3º3": {},
            "4º4": {},
        },
        "turns": {
            "1º1": "Tarde",
            "2º2": "Tarde",
            "3º3": "Tarde",
            "4º4": "Mañana",
        },
        "turnList": ["Mañana","Tarde","Noche"],
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