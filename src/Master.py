# Python imports
import os, sys, traceback
# Set environment variables
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
# Installed
from sty import bg, ef, fg, rs
# Wood imports
from utils import funcs, alt_funcs
from core import _vars, menus
import xProgram


def title(text=None):
    if text is None: text = f"Gestion Cursos - {_vars.__VERSION__}"
    if os.name == 'nt':
        import platform, ctypes
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(text)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {text}')
        os.system('color')
        if platform.release() in {"XP","7"}:
            _vars.__COLORS__ = False
    else:
        sys.stdout.write(b'\33]0;' + text + b'\a')
        sys.stdout.flush()
        os.system("")

def setup():
    funcs.clear(False)  # Clear any ansi escape characters.
    alt_funcs.resetVars() # Reset data vars.
    funcs.loadConfig() # Load config and do setup.

def start():
    setup()
    while _vars.keepAlive:
        menus.changeMenu("main") # Start menu.

def main():
    lx = funcs.lxTerm()
    try:
        start()
        if not alt_funcs.isNew():
            while True:
                print(f'{fg(240,190,25)}Do you want to save your current data?')
                funcs.mPrint(f"[1].", "Yes", True)
                funcs.mPrint(f"[2].", "No", True)
                print()
                action = funcs.xinput(False)
                if action == "1":
                    menus.saveMenu()
                if action in {"1","2"}:
                    break
        if _vars.restart:
            print(f"{fg.li_red}Press any key to restart the program.{fg.rs}")
            lx.getch(True)
            print()
            funcs.saveConfig()
            main()
        else:
            print(f"{fg.li_red}Press any key to exit the program.{fg.rs}")
            lx.getch(True)
            print()
    except Exception:
        print(f"{fg.rs}\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(f"{fg.li_red} --- [WARNING] Something awful happened! ---")
        print()
        # Will print this message followed by traceback.
        print(f"{fg.red}{traceback.format_exc()}", end='')
        print(f"{fg.rs}____________________________________________________________\n")
        # Will dump a crash report
#log = funcs.genFile("logs/crash", "report", ".txt", day=True)
#with open(f"logs/crash/{log}.txt", 'w', encoding="utf-8") as f:
#    f.write("\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n")
#    f.write("--- [WARNING] Something awful happened! ---\n")
#    f.write(traceback.format_exc())
#    f.write("____________________________________________________________\n")
        # Prevent the console window from closing.
        print(f"{fg.li_red}Press any key to exit the program.{fg.rs}")
        lx.getch(True)
        print()
        raise
    try:
        funcs.saveConfig()
        funcs.saveData()
    except Exception: pass


if __name__ == "__main__":
    title()
    main()