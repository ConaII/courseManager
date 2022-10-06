import copy
from sty import fg

__VERSION__ = '2.3-beta'
__COLORS__ = True

def codeInit():
    global keepAlive, restart, opticalsRT
    global exitMenu, exitSubMenu, menu, menuFunc
    global devMode, codeList
    keepAlive, restart = True, False
    exitMenu, exitSubMenu = None, None
    menu, menuFunc = None, None

    devMode = True
    opticalsRT = { # WARNING #
        "saveCfg": True,
        "loadCfg": True,
        "allowDev": True,
    }
    codeList = {
        "turnList": ["Mañana", "Tarde", "Noche"],
        "menuList": ["main","options","settings","manage","search","modCourse","modStudent","nowhere"]
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
        "courses": {
        },
        "turns": {
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
    global config, formats, options, others
    formats = config["formats"]
    options = config["options"]
    others = config["other"]