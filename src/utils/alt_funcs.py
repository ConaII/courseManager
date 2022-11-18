import re
# Installed
from sty import bg, ef, fg, rs
# Program
from core import _vars

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

def isWhole(string):
    try:
        int(float(string))
        return True
    except (TypeError, ValueError, OverflowError):
        pass

def isBool(string):
    if isinstance(string, str) and string.lower() in {"true", "1", "false", "0"}:
        return True

def getByIndex(list_, string, negative=True):
    if isWhole(string):
        n = int(float(string))
        index = n-1 if n > 0 else n
        if len(list_) > index >= -len(list_) and n != 0:
            if negative is False and index < 0:
                return string
            return list_[index]
    return string

def lookup0(where, string):
    if string is None:
        return False
    for k in where:
        if any(string.lower() == f"{x}".lower() for x in k):
            return k
    for k in where:        
        if any(f' {string.lower()}' in f' {f"{x}".lower()}' for x in k):
            if len(string) > 1:
                return k
    return False

# Search coincidences of items in dict/list.
def lookup(where, string):
    if string is None:
        return False
    for k in where:
        if string.lower() == f"{k}".lower():
            return k
    for k in where:
        if f" {string.lower()}" in f" {f'{k}'.lower()}":
            if len(string) > 1:
                return k
    return False

def formatDNI(dni):
    if type(dni) in (int, float):
        return f"{dni:,}".replace(',','.')
    return dni

#def formatAmount(amount, sep=None):
#    amount = int(amount)
#    if sep is None:
#        sep = _vars.formats["sep"]
#    style = {
#        0: amount,
#        1: f"{amount:,}".replace(",","|").replace(".",",").replace("|","."),
#        2: f"{amount:,}"
#    }
#    return style[sep]

def validateDNI(dni: str) -> bool:
    REGEXP = "[0-9]{8}[A-Z]"
    CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
    INVALID = {"00000000T", "00000001R", "99999999R"}
    if not dni[-1].isalpha():
        dni += CONTROL[int(dni[0:8]) % 23]
    return (dni not in INVALID
            and re.match(REGEXP, dni) is not None 
            and dni[8] == CONTROL[int(dni[0:8]) % 23])

def logo():
    x, y = fg(110,102,132), fg(89,75,128)
    print(fg(132,121,101) + "━"*59)
    print(f"  {x}█{y}█████  {x}█{y}█████  {x}█{y}█    {x}█{y}█ {x}█{y}█████  {x}█{y}██████ {x}█{y}██████ {x}█{y}██████ ")
    print(f" {x}█{y}█      {x}█{y}█    {x}█{y}█ {x}█{y}█    {x}█{y}█ {x}█{y}█   {x}█{y}█ {x}█{y}█      {x}█{y}█      {x}█{y}█      ")
    print(f" {x}█{y}█      {x}█{y}█    {x}█{y}█ {x}█{y}█    {x}█{y}█ {x}█{y}█████  {x}█{y}██████ {x}█{y}████   {x}█{y}██████ ")
    print(f" {x}█{y}█      {x}█{y}█    {x}█{y}█ {x}█{y}█    {x}█{y}█ {x}█{y}█   {x}█{y}█      {x}█{y}█ {x}█{y}█           {x}█{y}█ ")
    print(f"  {x}█{y}█████  {x}█{y}█████   {x}█{y}█████  {x}█{y}█   {x}█{y}█ {x}█{y}██████ {x}█{y}██████ {x}█{y}██████ ")
    print(fg(132,121,101) + "━"*59)
    print()