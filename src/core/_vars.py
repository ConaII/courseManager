import copy

__VERSION__ = '2.3-pre1'
__COLORS__ = True

def codeInit():
    global keepAlive, restart, opticalsRT
    global exitMenu, exitSubMenu, menu, menuFunc
    global devMode, turnList, menuList
    keepAlive, restart = True, False
    exitMenu, exitSubMenu = None, None
    menu, menuFunc = None, None

    devMode = True
    turnList = ["Mañana", "Tarde", "Noche"]
    menuList = ["main","options","settings","manage","search","modCourse","modStudent","nowhere"]
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
            "spaces": [1, 1], #Menu | Index
        },
        "options": {
            "menuLogo": True,
            "clearMode": True,
        },
        "other": {
            "cmdColors": True,
            "forceColors": False,
        },
        "favorites": {
            "Cursos": "courses/",
            "Recovery": "courses/crash/",
            "Documentos": "%USERPROFILE%/Documents/Courses/"
        },
        "version": 1.0
    }
    config = copy.deepcopy(defaultCfg)
    refreshCfg()

def varsInit():
    global defaultVars, var, selected, filters
    selected = [None, None]
    filters = set()
    defaultVars = {
        "courses": {},
        "turns": {},
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
    global config, formats, options, others
    formats = config["formats"]
    options = config["options"]
    others = config["other"]

def loadTest():
    global var
    var = {
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
            "3º5": {
                88_239_594: ["Carson Tano"],
                33_282_393: ["Jonna Cena"],
            },
            "4º14": {
                88_239_593: ["John Doe"],
                33_282_392: ["Janne Doe"],
            }
        },
        "turns": {
            "1º2": "Mañana",
            "2º1": "Tarde",
            "3º5": "Noche",
            "4º14": "Noche",
        },
        "mats": {
            "Matematicas": ""
        },
        "format": 1.1,
        "version": __VERSION__
    }