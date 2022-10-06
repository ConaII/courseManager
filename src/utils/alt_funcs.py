from core import _vars
import re

def isNew(where=None):
    if where is None:
        where = _vars.var
    data = {k: v for k, v in where.items() if k in _vars.defaultVars}
    if _vars.defaultVars == data:
        return True

def resetVars():
    _vars.codeInit()
    _vars.varsInit()

def checkAnyIn(string, list_):
    for i in list_:
        if string in i:
            return True

# Check if string is a whole integer.
def isWhole(string):
    if isinstance(string, str) and string != "":
        if string.isdecimal() or string[0] in ['-','+'] and string[1:].isdecimal():
            return True

def isBool(string):
    if isinstance(string, str) and string.lower() in {"true", "1", "false", "0"}:
        return True

def indexVal(list_, string):
    if isWhole(string):
        n = int(float(string))
        if len(list_) > n-1 and n > 0:
            return n-1
    return False

def getByIndex(list_, string, negative=True):
    if isWhole(string):
        n = int(float(string))
        index = n-1 if n > 0 else n
        if len(list_) > index >= -len(list_) and n != 0:
            if negative is False and index < 0:
                return string
            return list_[index]
    return string

def validateDNI(dni: str) -> bool:
    REGEXP = "[0-9]{8}[A-Z]"
    DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
    INVALIDOS = {"00000000T", "00000001R", "99999999R"}
    if not dni[-1].isalpha():
        dni += DIGITO_CONTROL[int(dni[0:8]) % 23]
    return (dni not in INVALIDOS
            and re.match(REGEXP, dni) is not None 
            and dni[8] == DIGITO_CONTROL[int(dni[0:8]) % 23])