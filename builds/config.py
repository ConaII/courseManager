options = {
    "name": "Wood",
    "version": "2.0snap1-b4",
    "CleanRoom": True,
}

LIB = {
    "Launcher": "WoodLauncher",
    "libDir": "libraries",
    "enabled": True
}

modules = {
    "32Bits": True,
    "64Bits": False,
    "OneFile": False,
    "OneLib": True  # Requires EXE Wrapper
}

#https://github.com/adang1345/PythonWindows/blob/master/3.8.13
pyPaths = {
    "Py32": "C:/Program Files (x86)/Python38-32/python.exe",
    "Ins32": "C:/Program Files (x86)/Python38-32/Scripts/pyinstaller.exe",
    "Py64": "C:/Program Files/Python38/python.exe",
    "Ins64": "C:/Program Files/Python38/Scripts/pyinstaller.exe",
    "signer": "C:/Program Files (x86)/Windows Kits/10/App Certification Kit/signtool.exe",
    # Add to system variables or set here
    "rar": "rar",
    "7zip": "7zip",
    "hyperion": "utils/hyperion.py"
}

hyperion = {
    "doTesting": True,
    "automatic": True,
    "RenameVars": False,
    "ProtectChunks": False,
    "folders": {
        "../src": "",
        "../src/game": "game",
        "../src/utils": "utils"
    }
}

# https://www.7-zip.org/download.html
# https://www.rarlab.com/download.htm
rarFiles = {
    #"7Zip": False, [UNSUPPORTED]
    "RAR": True,
    "exclude": [
        #"utils/data/certificate", Windows only
        "*\docs",
        "*\lang",
        "*.py",
        "*.pyc",
        "*.pyw",
    ],
    "include": [
        "utils/data/*",
        "../changelog.txt",
        "../src/resources",
    ],
    "empty": [
        "mods",
        "saves",
    ]
}

#https://pyinstaller.org/en/stable/usage.html#options
#https://pyinstaller.org/en/stable/usage.html#what-to-bundle-where-to-search
pyIns = {
    "script": "./obfuscated/Master.py",
    "imports": "./obfuscated",
    "output": "./product",
    "temp": "./utils/temp",
    "icon": "../storage/icons/wood.ico",
    "file-imports": [
        "xGame",
        "game._vars",
        "game.menus",
        "game.menu_funcs",
        "utils.funcs",
        "utils.alt_funcs",
        "utils.game_funcs",
        "utils.thread_funcs"
    ],
    "hidden-imports": [
        #"windows-curses",
        #"charset-normalizer",
        "asyncio",
        "certifi",
        "cffi",
        "charset_normalizer",
        "cryptography",
        "cryptography.fernet",
        "idna",
        "inflect",
        "keyboard",
        "pycparser",
        "pygame",
        "pypresence",
        "PySimpleGUI",
        "pytz",
        "requests",
        "sty",
        "toml",
        "urllib3",
        "curses",
        "zope.interface",
    ],
    "data": []
}