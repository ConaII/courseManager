import os, sys, copy, re
if os.name == 'nt':
    import msvcrt
else:
    import termios, atexit
    from select import select
# Installed
from sty import bg, ef, fg, rs
import pickle
# Program
from core import _vars

# Stdout redirect class.
class xLogger:
    ansi_escape = re.compile(r'\x1B (?:[@-Z\\-_] | \[ [0-?]* [-/]* [@-~])', re.VERBOSE)
    def __init__(self, stdout):
        self.c = stdout
    def write(self, obj):
        strip = self.ansi_escape.sub('', obj) # 7-bit C1 ANSI sequences
        if _vars.__COLORS__:
            self.c.write(obj)
        else:
            self.c.write(strip)
    def flush(self):
        self.c.flush()

class lxTerm:
    def start(self, perform=True):
        if os.name != 'nt' and perform:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
            # Support normal-terminal reset at exit
            atexit.register(self.reset)
    def reset(self, perform=True):
        if os.name != 'nt' and perform:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)
    def getch(self, auto=False):
        self.start(auto)
        if os.name == 'nt':
            x = msvcrt.getch()
        else:
            x = sys.stdin.read(1)
        self.reset(auto)
        return x
    def kbhit(self):
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []

# New Logging Interface system.
def IntLogger():
    if _vars.config["other"]["forceColors"]:
        _vars.__COLORS__ = _vars.config["other"]["cmdColors"]
    sys.stdout = xLogger(sys.stdout)

#def rmLast(path, name, ext, maxFiles=0):
#    from datetime import datetime, date
#    if not os.path.isdir(path):
#        os.makedirs(path, exist_ok=True) 
#    if os.path.isfile(f"{path}/latest{ext}"):
#        date = datetime.fromtimestamp(os.path.getmtime(f"{path}/latest{ext}")).strftime('%Y-%m-%d')
#        file = genFile(path, f"{name}_{date}", ext, sep=True, maxFiles=maxFiles)
#        try:
#            os.rename(f"{path}/latest{ext}", f"{path}/{file}{ext}")
#        except: 
#            return genFile(path, name, ext, day=True, sep=True, maxFiles=maxFiles)
#    return "latest"

def genFile(path, name, ext, day=False, sep=False, maxFiles=0):
    from datetime import date
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    x = "_" if sep else ""
    if day:
        x = f"_{date.today()}_"
    pattern = re.compile(r"^("+re.escape(name+x)+r")[0-9].*"+re.escape(ext)+r"$")
    pattern1 = re.compile(r"^("+re.escape(name)+"|"+re.escape(name+x)+r")[0-9].*"+re.escape(ext)+r"$")
    fileList = [f.name for f in os.scandir(path) if f.is_file() and pattern.match(f.name)]
    if date:
        pattern2 = re.compile(r"^("+re.escape(name)+r")[0-9_-][0-9].*"+re.escape(ext)+r"$")
        allList = [f.name for f in os.scandir(path) if f.is_file() and pattern2.match(f.name)]
    fileList.sort()
    indexList = [re.split('(\d+)', i)[-2] for i in fileList]
    indexList.sort()
    n = 1 if not len(indexList) else int(indexList[-1])+1
    while True:
        file = f"{name}{x}{n:02}"
        if day:
            file = f"{name}_{date.today()}_{n:02}"
        if not os.path.isfile(f"{path}/{file}{ext}"):
            break
        n += 1
    nonList = [f.name for f in os.scandir(path) if f.is_file() and not pattern1.match(f.name) and f.name.endswith(ext)]
    if ext == '.wsa':
        for i in nonList:
            os.rename(f"{path}/{i}", f"{path}/../{i}")
    if date: fileList = allList
    if len(fileList) >= maxFiles > 0:
        os.remove(f"{path}/{fileList[0]}")
    return file

def import1():
    pass

def export1():
    pass


def saveVal(data=None):
    if data is None:
        data = _vars.var
    bytecode = pickle.dumps(data)
    return bytecode

def loadVal(data, msg=False):
    from utils import alt_funcs
    try:
        fileVars = pickle.loads(data)
        if fileVars == {}:
            warn(f"Los datos del archivo estan vacios, abortando.\n", not msg)
        elif alt_funcs.isNew(fileVars):
            warn(f"Los datos del archivo son iguales que los default, abortando.\n", not msg)
        elif isinstance(fileVars, dict):
            alt_funcs.resetVars()
            for i in fileVars:
                if i in _vars.defaultVars and i not in ["version","format"]:
                    if isinstance(fileVars[i], dict):
                        _vars.var[i].update({k: v for k, v in fileVars[i].items() if k in _vars.defaultVars[i]})
                    else:
                        _vars.var[i] = fileVars[i]
            _vars.refreshVars()
            return True
    except (ValueError, pickle.UnpicklingError) as e:
        red("An error ocurred while unloading, corruption?\n")
        ExceptionCaught(e)
    except EOFError as e:
        red(f"An error ocurred while loading, data is empty.\n")
        ExceptionCaught(e)
    except NameError as e:
        red("An error ocurred, program variables not found.\n")
        ExceptionCaught(e)
    except Exception: pass

def saveData(save, path=None, ext=".wsa"):
    from utils import alt_funcs
    try:
        if path is None:
            path = "courses/"
        if not isinstance(save, str) or save == "":
            raise PermissionError
        else:
            if not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)
            while save.lower().endswith(ext):
                save = save[:-4]
            saveFile = os.path.join(f'{path}{save}{ext}')
            with open(f"{saveFile}", 'wb') as f:
                f.write(saveVal())
            green(f"Los datos se guardaron como {rs.bold_dim+fg.magenta}\"{save}{ext}\"\n")
            return True
    except FileNotFoundError:
        warn("Ese archivo no existe.")
    except (PermissionError, OSError):
        warn("Eso no es un nombre valido.")
    except NameError:
        warn("Program variables were not initiated.")
    print()

def loadData(save, path=None):
    try:
        if path is None:
            path = "courses/"
        if not isinstance(save, str) or save == "":
            raise PermissionError
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        while save.lower().endswith('.wsa'):
            save = save[:-4]
        with open(os.path.join(f'{path}{save}.wsa'), 'rb') as f:
            if loadVal(f.read()):
                green(f"Save file {save}.wsa loaded.\n")
                return True
    except FileNotFoundError:
        red("That save file doesn't exist.\n")
    except (PermissionError, OSError):
        red("That's not a valid name for your save file.\n")

def restoreConfig(key, sub_key=None, da_key=None, msg=True):
    if sub_key is None:
        _vars.config[key] = copy.deepcopy(_vars.defaultCfg[key])
        target = f"{key}"
    elif da_key is None:
        _vars.config[key][sub_key] = copy.deepcopy(_vars.defaultCfg[key][sub_key])
        target = f"{sub_key}"
    else:
        _vars.config[key][sub_key][da_key] = copy.deepcopy(_vars.defaultCfg[key][sub_key][da_key])
        target = f"{da_key} of {sub_key}"
    if msg:
        green(f"Config {target} was restored to default.\n")
    _vars.refreshCfg()

def resetConfig():
    _vars.config = copy.deepcopy(_vars.defaultCfg)
    green(f"Config was restored to default.")
    print()
    _vars.refreshCfg()

def saveConfig(msg=False):
    if _vars.opticalsRT["saveCfg"]:
        with open("config.wdc", 'wb') as f:
            pickle.dump(_vars.config, f)
        if msg:
            green(f"Current Config was saved successfully.")
            print()

def loadConfig(msg=True):
    if _vars.opticalsRT["loadCfg"]:
        try:
            with open("config.wdc", 'rb') as f:
                tempConfig = pickle.load(f)
                if not isinstance(tempConfig, dict):
                    raise TypeError
                for i in tempConfig:
                    if i in _vars.config and i not in ["version","format"]:
                        if isinstance(tempConfig[i], dict):
                            _vars.config[i].update({k: v for k, v in tempConfig[i].items() if k in _vars.defaultCfg[i]})
                        else:
                            _vars.config[i] = tempConfig[i]
                if _vars.config["other"]["forceColors"]:
                    _vars.__COLORS__ = _vars.config["other"]["cmdColors"]
                _vars.refreshCfg()
            if msg:
                green(f"Config loaded successfully.")
                print()
        except FileNotFoundError:
            if msg:
                green(f"Config created successfully.")
                print()
            saveConfig()
        except (FileNotFoundError, TypeError, EOFError) as e:
            if msg:
                if isinstance(e, TypeError):
                    ErrType = "outdated-config"
                elif isinstance(e, EOFError):
                    ErrType = "empty-file"
                else:
                    ErrType = "unknown-err"
                red(f"Config conflict detected: {ErrType}, resetting to default.")
                print()
            saveConfig()

def warn(text, cancel=False):
    if not cancel:
        print(f"{fg(230,45,78)}{text}{fg.rs}")
def red(text, cancel=False):
    if not cancel:
        print(f"{fg(196)}{ef.bold}{text}{rs.all}")
def green(text, cancel=False):
    if not cancel:
        print(f"{fg(0,200,0)}{ef.bold}{text}{rs.all}")
def yellow(text, cancel=False):
    if not cancel:
        print(f"{fg(255,236,0)}{bg.rs}{text}{rs.all}")

# Custom print function for menus.
def mPrint(num, text, menu=False):
    if None in (num, text):
        return
    color0 = fg.rs if menu else fg(116,190,245)
    value = _vars.formats["spaces"][0]
    if menu == "index":
        value = _vars.formats["spaces"][1]
    menuFormats = {
        0: "",
        1: " "
    }
    print(menuFormats[value] + f"{color0}{num} {fg.cyan}{text}{fg.rs}")

def elseval(action=False):
    if action is not None and action != "":
        warn("Operación inválida, inténtalo de nuevo.\n")

def clear(space=True):
    if sys.stdin and sys.stdin.isatty():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    if space:
        print()

def strToBool(string):
    if isinstance(string, str):
        if string.lower() in {"true","1"}:
            return True
        if string.lower() in {"false","0"}:
            return False

def absPath(string):
    return os.path.abspath(os.path.expandvars(os.path.expanduser(string)))

# function to convert to superscript
def get_super(x):
    if isinstance(x, int):
        x = str(x)
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

def intInput(replace=False, inLoop=False):
    try:
        action = xinput(False, ">>", fg(240,70,140))
        if replace:
            action = action.replace('.','_')
        return int(float(action))
    except (ValueError, OverflowError):
        if inLoop and action == "": return ""
        warn("Debes introducir un valor numerico.\n")
        

def xinput(allowCMD=True, sep=">>>", color=fg(0, 148, 255), color2=rs.all):
    try:
        try: 
            if _vars.__COLORS__:
                sys.__stdout__.write(f"{color}{sep}{color2} ")
            else:
                sys.__stdout__.write(f"{sep} ")
            cmd = input().strip()
            print()
        except EOFError:
            sys.__stdout__.write("\n")
            red("Invalid input. EOF is not supported.\n")
            return
        if _vars.options["clearMode"]:
            if allowCMD and len(cmd) >= 10 and cmd[:10] == "/clearmode":
                if len(cmd) > 10 and cmd[10:].split()[0].lower() not in {"true","1","false","0"}:
                    clear()
            else:
                clear()
        if allowCMD and len(cmd) > 0 and cmd[0] == "/":
            runCommand(cmd)
            return None
        return cmd
    except FloatingPointError:
        raise FloatingPointError
    except Exception as e:
        ExceptionCaught(e)

def ExceptionCaught(e, doTraceback=True, lines=True):
    import traceback
    msg = None
    if isinstance(e, str): msg = e
    if isinstance(e, Exception):
        e_class = e.__class__
        e_desc = ": "
        if len(e.args) > 0:
            e_desc = f": {e.args[0]}"
        msg = f"{e_class.__name__} from <'{e_class.__module__}'>{e_desc}"
    if msg is not None:
        if lines:
            print(f"{fg.rs}‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(f"{fg.li_red} [WARNING] Something awful happened!")
        print(f"{fg.da_grey} [{fg(240,190,25)}INFO{fg.da_grey}] {fg.li_blue}Exception caught! {msg}{fg.rs}")
        # Will print this message followed by traceback.
        if doTraceback and isinstance(e, Exception):
            print(f"\n{fg.red}{traceback.format_exc()}{fg.rs}", end='')
        if lines:
            print("____________________________________________________________")
        print()

def setVar(name, where, args):
    from utils import alt_funcs
    if where is not None:
        if len(args) > 0 and type(where) in {list, tuple, set, dict, frozenset}:
            key = None
            if args[0] in where:
                key = args[0]
                where = where[key]
            elif args[0][0] == "." and alt_funcs.isWhole(args[0][1:]):
                try: 
                    key = list(where)[int(float(args[0][1:]))]
                    where = where[key]
                except IndexError:
                    red("Index is out of range, try again.\n")
            if key is not None:
                name = f'{name}["{key}"]'
                if len(args) > 1 and type(where) in {list, tuple, set, dict, frozenset}:
                    name, where = setVar(name, where, args[1:])
        index = None
        lDict = {"where":where, "_vars":globals()["_vars"]}
        if len(args) == 2 and args[0] in {"=","+=","-="}:
            index = 0
        elif len(args) > 2 and args[1] in {"=","+=","-="}:
            if key is None:
                name = f'{name}["{args[0]}"]'
            index = 1
        if index is not None:
            try:
                exec(f"_vars.{name} {args[index]} {' '.join(args[index+1:])}")
                exec(f"where = _vars.{name}", lDict)
            except Exception as e: red(f"{e.__class__}: {e}\n")
            where = lDict["where"]
    return name, where

def runCommand(cmd):
    import xProgram
    from core import _vars, menus
    from utils import alt_funcs
    from shlex import split as shlex_split
    try:
        args, full_args = shlex_split(cmd), shlex_split(cmd, posix=False)
    except ValueError:
        red("Invalid input. No closing quotation.\n")
        return
    if isinstance(args, list):

#----------------#
## Help Command ##
#----------------#

        if args[0].lower() in {"/alias"}:
            warn("No fue implementado aún.\n")
        elif args[0].lower() in {"/help","/?"}:
            if len(args) == 1:
                args.append("all")
            if len(args) > 1:
                if args[1].lower() in {"menus","menu","actions","action","misc","all"} or args[1].isdecimal() and int(args[1]) in range(1,4) or args[1].lower() == "dev" and _vars.opticalsRT["allowDev"]:
                    if args[1].lower() in {"menus","menu","all"} or args[1] == "1":
                        print(f"{fg.cyan}::{fg.magenta}--{fg(240,210,40)}HELP {fg.da_grey}({fg(240,190,25)}Menus{fg.da_grey}){fg.magenta}--{fg.cyan}::")
                        print(f" {fg.li_cyan}/menu      {fg(240,190,25)}-{fg.grey} Open main menu.")
                        print(f" {fg.li_cyan}/options   {fg(240,190,25)}-{fg.grey} Open options menu.")
                        print(f" {fg.li_cyan}/manage    {fg(240,190,25)}-{fg.grey} Open manage menu.")
                        print(f" {fg.li_cyan}/search    {fg(240,190,25)}-{fg.grey} Open search menu.")
                        print(f" {fg.li_cyan}/save      {fg(240,190,25)}-{fg.grey} Open save menu.")
                        print(f" {fg.li_cyan}/load      {fg(240,190,25)}-{fg.grey} Open load menu.")
                        print()
                    if args[1].lower() in {"actions","action","all"} or args[1] == "2":
                        print(f"{fg.cyan}::{fg.magenta}--{fg(240,210,40)}HELP {fg.da_grey}({fg(70,150,45)}Actions{fg.da_grey}){fg.magenta}--{fg.cyan}::")
                        print(f" {fg.li_cyan}/addcourse  {fg(240,190,25)}-{fg.grey} Add a new course")
                        print(f" {fg.li_cyan}/selcourse  {fg(240,190,25)}-{fg.grey} Select a course.")
                        print(f" {fg.li_cyan}/modcourse  {fg(240,190,25)}-{fg.grey} Modify selected course.")
                        print(f" {fg.li_cyan}/delcourse  {fg(240,190,25)}-{fg.grey} Select and delete a course")
                        print()
                        print(f" {fg.li_cyan}/addstudent  {fg(240,190,25)}-{fg.grey} Add a new student to selected course.")
                        print(f" {fg.li_cyan}/selstudent  {fg(240,190,25)}-{fg.grey} Select a student from selected course.")
                        print(f" {fg.li_cyan}/modstudent  {fg(240,190,25)}-{fg.grey} Modify selected student from selected course.")
                        print(f" {fg.li_cyan}/delstudent  {fg(240,190,25)}-{fg.grey} Select and delete a student.")
                        print()
                    if args[1].lower() in {"misc","all"} or args[1] == "3":
                        print(f"{fg.cyan}::{fg.magenta}--{fg(240,210,40)}HELP {fg.da_grey}({fg(38,111,211)}Misc{fg.da_grey}){fg.magenta}--{fg.cyan}::")
                        print(f" {fg.li_cyan}/exit          {fg(240,190,25)}-{fg.grey} Exit the program.")
                        print(f" {fg.li_cyan}/restart       {fg(240,190,25)}-{fg.grey} Restart the program.")
                        print(f" {fg.li_cyan}/reload        {fg(240,190,25)}-{fg.grey} Reload program data.")
                        print(f" {fg.li_cyan}/exitmenus     {fg(240,190,25)}-{fg.grey} Exit from all menus.")
                        print(f" {fg.li_cyan}/exitsubmenus  {fg(240,190,25)}-{fg.grey} Exit from all submenus.")
                        print(f" {fg.li_cyan}/format        {fg(240,190,25)}-{fg.grey} Manage formats.")
                        print(f" {fg.li_cyan}/config        {fg(240,190,25)}-{fg.grey} Manage the config file.")
                        print(f" {fg.li_cyan}/clear         {fg(240,190,25)}-{fg.grey} Clear the console.")
                        print(f" {fg.li_cyan}/clearmode     {fg(240,190,25)}-{fg.grey} Change clear mode status.")
                        print(f" {fg.li_cyan}/togglecolors  {fg(240,190,25)}-{fg.grey} Toggle console colors and forceColors.")
                        print()
                    if args[1].lower() in {"dev","all"}:
                        if _vars.opticalsRT["allowDev"]:
                            print(f"{fg.cyan}::{fg.magenta}--{fg(240,210,40)}HELP {fg.da_grey}({fg(242,42,136)}Dev{fg.da_grey}){fg.magenta}--{fg.cyan}::")
                            if _vars.devMode:
                                #print(f" {fg(215,70,60)}/devmode     {fg(240,190,25)}-{fg.grey} Change developer mode status.")
                                print(f" {fg.li_cyan}/sty        {fg(240,190,25)}-{fg.grey} Parse text with sty effects.")
                                print(f" {fg.li_cyan}/exec       {fg(240,190,25)}-{fg.grey} Execute code.")
                                print(f" {fg.li_cyan}/setvar     {fg(240,190,25)}-{fg.grey} Modify a program variable.")
                                print(f" {fg.li_cyan}/tp         {fg(240,190,25)}-{fg.grey} Teleport to any menu.")
                                print(f" {fg.li_cyan}/menulist   {fg(240,190,25)}-{fg.grey} Shows the list of menus.")
                                print(f" {fg.li_cyan}/crash      {fg(240,190,25)}-{fg.grey} Crashes the program.")
                            #else:
                            #    print(f" {fg(215,70,60)}/devmode  {fg(240,190,25)}-{fg.grey} Change developer mode status.")
                            print()
                else:
                    elseval(0)

#------------------#
## Menus Commands ##
#------------------#

        elif args[0].lower() in {"/main","/menu","/mainmenu","/pause","/esc"}:
            menus.changeMenu("main")
        elif args[0].lower() == "/options":
            menus.changeMenu("options")
        elif args[0].lower() == "/manage":
            menus.changeMenu("manage")
        elif args[0].lower() == "/search":
            menus.changeMenu("search")
        elif args[0].lower() in {"/save","/s"}:
            if len(args) == 2:
                menus.fileVal("save", path="courses/", file=args[1])
            elif len(args) > 2:
                menus.fileVal("save", path=args[2], file=args[1])
            else:
                menus.saveMenu()
        elif args[0].lower() in {"/load","/l"}:
            if len(args) == 2:
                menus.fileVal("load", path="courses/", file=args[1])
            elif len(args) > 2:
                path = "courses/crash" if args[2] == "crash" else args[2]
                menus.fileVal("load", path=path, file=args[1])
            else:
                menus.loadMenu()

#-------------------#
## Action Commands ##
#-------------------#

        elif args[0].lower() == "/addcourse":
            xProgram.addCourse()
        elif args[0].lower() == "/selcourse":
            if not len(_vars.courses):
                warn("No hay ningun curso añadido.\n")
            else:
                xProgram.selCourse()
        elif args[0].lower() == "/modcourse":
            if _vars.selected[0] is None:
                warn("No hay un curso seleccionado.\n")
            else: 
                xProgram.modCourse()
        elif args[0].lower() == "/delcourse":
            if not len(_vars.courses):
                warn("No hay ningun curso añadido.\n")
            else: 
                xProgram.delCourse(xProgram.selCourse(False))

        elif args[0].lower() == "/addstudent":
            if _vars.selected[0] is None:
                warn("No hay un curso seleccionado.\n")
            else:
                xProgram.addStudent(_vars.selected[0])
        elif args[0].lower() == "/selstudent":
            if _vars.selected[0] is None:
                warn("No hay un curso seleccionado.\n")
            elif not len(_vars.courses[_vars.selected[0]]):
                warn("No hay ningun alumno añadido.\n")
            else:
                xProgram.selStudent()
        elif args[0].lower() == "/modstudent":
            if _vars.selected[0] is None:
                warn("No hay un curso seleccionado.\n")
            elif not len(_vars.courses[_vars.selected[0]]):
                warn("No hay ningun alumno añadido.\n")
            elif _vars.selected[1] is None:
                warn("No hay un alumno seleccionado.\n")
            else:
                xProgram.modStudent()
        elif args[0].lower() == "/delstudent":
            if _vars.selected[0] is None:
                warn("No hay un curso seleccionado.\n")
            elif not len(_vars.courses[_vars.selected[0]]):
                warn("No hay ningun alumno añadido.\n")
            else:
                xProgram.delCourse(xProgram.selStudent(_vars.selected[0], False))

#-----------------#
## Misc Commands ##
#-----------------#

        elif args[0].lower() in {"/exit","/quit","/leave","/close","/shutdown"}:
            _vars.exitMenu = True
            _vars.exitSubMenu = True
            _vars.keepAlive = False
        elif args[0].lower() in {"/restart","/reboot","/reset"}:
            _vars.restart = True
            _vars.exitMenu = True
            _vars.exitSubMenu = True
            _vars.keepAlive = False
        elif args[0].lower() == "/reload":
            alt_funcs.resetVars()
        elif args[0].lower() == "/exitmenus":
            _vars.exitMenu = True
        elif args[0].lower() == "/exitsubmenus":
            _vars.exitSubMenu = True
        elif args[0].lower() == "/format":
            usage, usage1 = False, False
            if len(args) > 1:
                if args[1].lower() == "menu":
                    value = _vars.formats["spaces"][0]
                    menuType = [f"{fg(215,70,60)}non-spaced",f"{fg(60,215,40)}spaced"]
                    if len(args) > 2:
                        if args[2] in {"0","1"}:
                            value = int(args[2])
                        else:
                            usage1 = True
                    else:
                        value = int(not bool(value))
                    if usage1:
                        print(f'{fg(80,140,210)}Menu format: {menuType[value]}{fg.rs}')
                        print()
                        print(f"{fg.li_grey} - See the current menu format or change the menu format.")
                        print(f"{fg.red}/format menu <0/1>")
                        print(fg.rs)
                    else:
                        _vars.formats["spaces"][0] = value
                        print(f"{fg.li_grey}Menu format changed to {menuType[value]}{fg.rs}")
                        print()
                elif args[1].lower() == "index":
                    value = _vars.formats["spaces"][1]
                    indexType = [f"{fg(215,70,60)}non-spaced",f"{fg(60,215,40)}spaced"]
                    if len(args) > 2:
                        if args[2] in {"0","1"}:
                            value = int(args[2])
                        else:
                            usage1 = True
                    else:
                        value = int(not bool(value))
                    if usage1:
                        print(f'{fg(80,140,210)}Index format: {indexType[value]}{fg.rs}')
                        print()
                        print(f"{fg.li_grey} - See the current index format or change the index format.")
                        print(f"{fg.red}/format index <0/1>")
                        print(fg.rs)
                    else:
                        _vars.formats["spaces"][1] = value
                        print(f"{fg.li_grey}Index format changed to {indexType[value]}{fg.rs}")
                        print()
                elif args[1].lower() in {"separator","sep"}:
                    value = _vars.formats["sep"]
                    sepType = [
                        f"{fg(215,70,60)}No separator",
                        f"{fg(240,190,25)}Dots separator",
                        f"{fg(60,215,40)}Comma separator" 
                    ]
                    if len(args) > 2:
                        if args[2] in {"0","1","2"}:
                            value = int(args[2])
                        else:
                            usage1 = True
                    else:
                        value = value+1 if value+1 < 3 else 0 
                    if usage1:
                        print(f'{fg(80,140,210)}Separator format: {sepType[value]}{fg.rs}')
                        print()
                        print(f"{fg.li_grey} - See the current thousand separator format or change the separator format.")
                        print(f"{fg.red}/format sep <0/1/2>")
                        print(fg.rs)
                    else:
                        _vars.formats["sep"] = value
                        print(f"{fg.li_grey}Separator format changed to {sepType[value]}{fg.rs}")
                        print()
                else:
                    usage = True
            else:
                usage = True
            if usage:
                print(f"{fg.li_grey} - See or change formats.")
                print(f"{fg.red}/format <menu/index/separator> <?>")
                print(fg.rs)
            else:
                saveConfig()
        elif args[0].lower() == "/config":
            usage = True
            if len(args) > 1:
                usage = False
                if args[1].lower() == "save":
                    saveConfig(msg=True)
                elif args[1].lower() in {"load","reload"}:
                    loadConfig()
                elif args[1].lower() == "reset":
                    resetConfig()
                else:
                    usage = True
            if usage:
                print(f"{fg.li_grey} - Manage the config file.")
                print(f"{fg.red}/config <save/load/reset>")
                print(fg.rs)
        elif args[0].lower() in {"/clear","/cls","/empty"}:
            clear()
            print(f"Console has been cleared.")
            print()
        elif args[0].lower() == "/clearmode":
            value = None
            if len(args) > 1:
                if args[1].lower() in {"true", "1", "false", "0"}:
                    value = strToBool(args[1])
            else:
                value = not _vars.options["clearMode"]
            if value is None:
                print(f'{fg(80,140,210)}clearMode: {f"{fg(60,215,40)}True" if _vars.options["clearMode"] else f"{fg(215,70,60)}False"}')
                print(f"{fg.li_grey} - Change clear mode status.")
                print(f"{fg.red}/clearmode <true/false>")
                print(fg.rs)
            else:
                _vars.options["clearMode"] = value
                if value:
                    clear()
                    print(f"{fg(60,215,40)}Enabled clear mode.")
                else:
                    print(f"{fg(215,70,60)}Disabled clear mode.")
                print(fg.rs)
                saveConfig()
        elif args[0].lower() == "/togglecolors":
            usage = False
            value = _vars.config["other"]["cmdColors"]
            value1 = _vars.config["other"]["forceColors"]
            mode = "console"
            if len(args) > 1:
                if args[1].lower() in {"true", "1", "false", "0"}:
                    value = strToBool(args[1])
                elif args[1].lower() in {"force","-f"}:
                    value1 = not value1
                    mode = "force"
                else:
                    usage = True
            else:
                value = not value
            if usage:
                print(f'{fg(80,140,210)}forceColors: {f"{fg(60,215,40)}True" if value else f"{fg(215,70,60)}False"}')
                print(f'{fg(80,140,210)}Colors: {f"{fg(60,215,40)}True" if _vars.__COLORS__ else f"{fg(215,70,60)}False"}')
                print(f"{fg.li_grey} - Toggle console colors and change forceColors.")
                print(f"{fg.red}/togglecolors <true/false/force>")
                print(fg.rs)
            else:
                _vars.config["other"]["forceColors"] = value1
                _vars.config["other"]["cmdColors"], _vars.__COLORS__ = value, value
                if mode == "console" and value or mode == "force" and value1:
                    print(f"{fg(60,215,40)}Enabled {mode} colors.{fg.rs}")
                    print()
                else:
                    print(f"{fg(215,70,60)}Disabled {mode} colors.{fg.rs}")
                    print()
                saveConfig()

#----------------------#
## Developer Commands ##
#----------------------#

        elif args[0].lower() == "/import":
            if _vars.devMode:
                import1()
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()

        elif args[0].lower() == "/export":
            if _vars.devMode:
                export1()
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        elif args[0].lower() == "/sty":
            if _vars.devMode:
                usage = True
                text = "Sample text!"
                if len(args) > 1:
                    usage = False
                    if len(args) > 2:
                        text = ' '.join(args[2:])
                if usage:
                    print(f"{fg.li_grey} - Parse text with sty effects.")
                    print(f'{fg.red}/sty <color> <text>')
                    print(fg.rs)
                else:
                    try:
                        import sty
                        exec(f'print(sty.{args[1]} + f"{text}" + fg.rs)')
                        print()
                    except Exception as e:
                        red(f"Invalid syntax: {e.__class__} {e}\n")
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        elif args[0].lower() == "/exec":
            if _vars.devMode:
                if len(args) > 1:
                    cmd = ' '.join(full_args[1:]).replace('\\n','\n')
                    try : exec(cmd)
                    except : 
                        red("Invalid syntax.\n")
                else:
                    print(f"{fg.li_grey} - Parse a command through exec().")
                    print(f"{fg.red}/exec <args>")
                    print(fg.rs)
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        elif args[0].lower() == "/setvar":
            if _vars.devMode:
                usage = True
                if len(args) > 1 and args[1] not in {"/?","?"}:
                    where = None
                    if args[1].lower() == "full" and len(args) > 2:
                        try:
                            name = full_args[2]
                            lDict = {"_vars":globals()["_vars"]}
                            exec(f"where = _vars.{name}", lDict)
                            where = lDict["where"]
                            full_args.pop(2)
                        except KeyError:
                            if len(args) > 3 and args[3] in {"=","+=","-="}:
                                try:
                                    exec(f"_vars.{name} {args[3]} {' '.join(args[4:])}")
                                    exec(f"value = _vars.{name}", lDict)
                                    print(f'{fg(80,140,210)}{name} = {lDict["value"]} | {type(lDict["value"])}{fg.rs}\n')
                                    usage = False
                                except Exception as e: red(f"{e.__class__}: {e}\n")
                            else:
                                red("Key doesn't exist, try defining a value.\n")
                        except Exception as e:
                            red(f"{e.__class__}: {e}\n")
                    else:
                        name = args[1]
                        where = getattr(_vars, args[1], None)
                    if where is not None:
                        name, value = setVar(name, where, full_args[2:])
                        if isinstance(value, str):
                            value = f'"{value}"'
                        print(f"{fg(80,140,210)}{name} = {value} | {type(value)}{fg.rs}\n")
                        usage = False
                if usage:
                    print(f"{fg.li_grey} - Set a variable to new value.")
                    print(f"{fg.red}/setvar <dict> [key] = <value>")
                    print(f"{fg.red}/setvar full <variable> = <value>")
                    print(fg.rs)
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        elif args[0].lower() in {"/tp", "/room"}:
            if _vars.devMode:
                usage = True
                if len(args) > 1:
                    name = args[1].lower()
                    menu_id = alt_funcs.lookup(_vars.codeList["menuList"], name)
                    if menu_id is not False:
                        print(f"{fg.li_blue}Teleported to menu {menu_id}{fg.rs}")
                        print()
                        menus.changeMenu(menu_id)
                        usage = False
                    else:
                        print(f'{fg.red}Unknown menu "{name}"{fg.rs}')
                        print()
                if usage:
                    print(f"{fg.li_grey} - Teleport to another menu.")
                    print(f"{fg.red}/tp <menu>")
                    print(fg.rs)
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        elif args[0].lower() in "/menulist":
            if _vars.devMode:
                print(f"{fg(68,142,235)}CONFIG:{fg.li_grey} main, options, save, load")
                print(f"{fg(54,195,54)}PROGRAM:{fg.li_grey} manage, search, modCourse, modStudent")
                print(f"{fg(189,50,205)}OTHERS: {fg(205,50,127)}nowhere")
                print(fg.rs)
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        elif args[0].lower() == "/crash":
            if _vars.devMode:
                raise FloatingPointError
            elif _vars.opticalsRT["allowDev"]:
                red("Developer mode is disabled\n")
            else:
                elseval()
        ### |<---- END ---->| ###
        else:
            elseval()