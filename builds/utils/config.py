options = {
    "name": "Courses",
    "version": "2.3",
    "CleanRoom": True,
    "testProduct": False,
    "noConfirm": False
}

LIB = {
    "Launcher": "CoursesManager",
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
    "python": "py",
    "Ins32": "pyinstaller.exe",
    "Ins64": "",
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
        "../src/core": "core",
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
    ],
    "empty": [
        "courses",
    ]
}

#https://pyinstaller.org/en/stable/usage.html#options
#https://pyinstaller.org/en/stable/usage.html#what-to-bundle-where-to-search
pyIns = {
    "script": "./obfuscated/Master.py",
    "imports": "./obfuscated",
    "output": "./product",
    "temp": "./utils/temp",
    "icon": "../storage/icons/favicon.ico",
    "file-imports": [
        "xProgram",
        "core._vars",
        "core.menus",
        "utils.funcs",
        "utils.alt_funcs",
    ],
    "hidden-imports": [
        "asyncio",
        "cffi",
        "numpy",
        "et_xmlfile",
        "openpyxl",
        "sty",
        "xlsxwriter",
        "platform",
    ],
    "data": []
}