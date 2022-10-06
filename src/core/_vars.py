import copy

__VERSION__ = '1.0-alpha'
__COLORS__ = True

def codeInit():
    global keepAlive, restart, exitMenu, exitSubMenu, room, prevRoom, menu, menuFunc
    keepAlive, restart = True, False
    exitMenu, exitSubMenu = None, None
    room, prevRoom, menu, menuFunc = None, None, None, None

def configInit():
    global defaultCfg, config
    defaultCfg = {}
    config = copy.deepcopy(defaultCfg)

def varsInit():
    global defaultVars, var
    defaultVars = {
        "courses": {}
    }
    var = copy.deepcopy(defaultVars)
    refreshVars()

def refreshVars():
    global var, courses
    courses = var["courses"]