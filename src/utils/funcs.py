import os, sys, copy
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
                        if isinstance(tempConfig[i], dict) :
                                _vars.config[i].update({k: v for k, v in tempConfig[i].items() if k in _vars.defaultCfg[i]})
                        else:
                            _vars.config[i] = tempConfig[i]
                if _vars.config["other"]["forceColors"]:
                    _vars.__COLORS__ = _vars.config["other"]["cmdColors"]
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
        _vars.refreshCfg()

def warn(text, cancel=False):
    if not cancel:
        print(f"{fg.li_red}{text}{fg.rs}")
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

# Clear console function.
def clear(space=True):
    if sys.stdin and sys.stdin.isatty():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    if space:
        print()

# Misc function to convert str to bool
def strToBool(string):
    if isinstance(string, str):
        if string.lower() in {"true","1"}:
            return True
        if string.lower() in {"false","0"}:
            return False

def intInput(replace=False):
    try:
        action = xinput(False, ">>", fg(240,70,140))
        if replace:
            action = action.replace('.','_')
        return int(float(action))
    except (ValueError, OverflowError):
        if action == "":
            print("Puedes salir de este menu introduciendo '0'\n")
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
        if _vars.OPCIONES["clearMode"]:
            if allowCMD and len(cmd) >= 10 and cmd[:10] == "/clearmode":
                if len(cmd) > 10 and cmd[10:].split()[0].lower() not in {"true","1","false","0"}:
                    clear()
            else:
                clear()
        if allowCMD and len(cmd) > 0 and cmd[0] == "/":
            runCommand(cmd)
            return None
        return cmd
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

def runCommand(cmd):
    from core import _vars, menus
    from utils import alt_funcs
    from shlex import split as shlex_split
    try:
        args, full_args = shlex_split(cmd), shlex_split(cmd, posix=False)
    except ValueError:
        red("Invalid input. No closing quotation.\n")
        return
    if isinstance(args, list):
        if args[0].lower() in {"/exit","/quit","/leave","/close","/shutdown"}:
            _vars.exitMenu = True
            _vars.exitSubMenu = True
            _vars.keepAlive = False
        elif args[0].lower() in {"/restart","/reboot","/reset"}:
            _vars.restart = True
            _vars.exitMenu = True
            _vars.exitSubMenu = True
            _vars.keepAlive = False
        elif args[0].lower() == "/reload":
            alt_funcs.valsVal()
        elif args[0].lower() == "/exitmenus":
            _vars.exitMenu = True
        elif args[0].lower() == "/exitsubmenus":
            _vars.exitSubMenu = True