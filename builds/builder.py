import os, shutil, subprocess
from sty import *
from utils.funcs import *
try:
    import config
except ModuleNotFoundError:
    from utils import config

def title():
    title = f"pyBuilder v2.1"
    if os.name == 'nt':
        import ctypes
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(title)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {title}')
        os.system('color')
    else:
        sys.stdout.write(b'\33]0;' + title + b'\a')
        sys.stdout.flush()
        os.system("")

def setup():
    clear()
    if config.modules["32Bits"]:
        try:
            subprocess.call(config.pyPaths["Ins32"], creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            warn("[WARN] Pyinstaller (x32) wasn't found:")
            config.modules["32Bits"] = False
    if config.modules["64Bits"]:
        try:
            subprocess.call(config.pyPaths["Ins64"], creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            warn("[WARN] Pyinstaller (x64) wasn't found: ")
            config.modules["64Bits"] = False

def cReload():
    import importlib
    importlib.reload(config)
    main()

def main():
    setup()
    while True:
        print(f'{fg(160,85,212)}Version: {config.options["version"]}')
        print()
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPTIONS {fg.magenta}>>-----{fg.rs}")
        mPrint(f"[1].", f"{fg(93)}Obfuscate Code")
        mPrint("[2].", f"{fg(27)}EXECompiler")
        mPrint("[3].", f"{fg(11)}EXESigner")
        mPrint("[4].", f"{fg(166)}RARCompress")
        #mPrint("[5].", f"{fg(2)}Change Version")
        print()
        mPrint("[0].", f"{fg.li_red}[EXIT]")
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            obfuscate()
        elif action == "2":
            if config.modules["64Bits"]:
                build(x64=True)
            elif config.modules["32Bits"]:
                build()
            else:
                warn("[WARN] Enable a build architecture first\n")
        elif action == "3":
            if config.modules["64Bits"]:
                signer(x64=True)
            elif config.modules["32Bits"]:
                signer()
            else:
                warn("[WARN] Enable a build architecture first\n")
        elif action == "4":
            if config.modules["64Bits"]:
                rar(x64=True)
            elif config.modules["32Bits"]:
                rar()
            else:
                warn("[WARN] Enable a build architecture first\n")
        elif action == "/reload":
            cReload()
        else:
            elseval()

def obfuscate():
    if not os.path.isfile(config.pyPaths["hyperion"]):
        warn("[WARN] Hyperion script wasn't found\n")
        return
    try:
        if os.path.isdir("obfuscated"):
            shutil.rmtree('obfuscated')
        os.mkdir("obfuscated")
    except Exception:
        pass
    for k, v in config.hyperion["folders"].items():
        scripts = [f.name for f in os.scandir(k) if f.is_file() and f.name.endswith((".py",".pyw",".pyx"))]
        for file in scripts:
            path = f"{k}/{file}"
            if file == "__init__.py":
                shutil.copy2(f"{k}/{file}", f"obfuscated/{v}")
                continue
            elif file == "_vars.py":
                with open(f"{k}/{file}", 'r') as f:
                    data = f.read()
                defaults = {
                    "devMode =": False,
                    '"allowDev":': False,
                    '"saveCfg":': True,
                    '"loadCfg":': True,
                }
                for ks, vs in defaults.items():
                    data = data.replace(f"{ks} {not vs}", f"{ks} {vs}")
                with open(f"utils/{file}", 'w') as f:
                    f.write(data)
                path = f"utils/{file}"
            cmd = [*config.pyPaths["python"].split(), config.pyPaths["hyperion"], f'--file="{path}"', f'--destiny="obfuscated/{v}"', '--rename=False', f'-sr={not config.hyperion["RenameVars"]}', f'-sc={not config.hyperion["ProtectChunks"]}', f'-auto={config.hyperion["automatic"]}', '-logo=False']
            subprocess.run(cmd)
            print(fg.rs, end='')
    if os.path.isfile("utils/Master.py"):
        os.remove("utils/Master.py")
    if os.path.isfile("utils/_vars.py"):
        os.remove("utils/_vars.py")
    if config.hyperion["doTesting"]:
        try:
            child = subprocess.Popen([*config.pyPaths["python"].split(), 'Master.py'], cwd="obfuscated", creationflags=subprocess.CREATE_NEW_CONSOLE)
            child.communicate()[0]
            if child.returncode == 1:
                red("Failed to execute Master.py, retrying...\n")
                obfuscate()
            else:
                green("Test completed successfully...\n")
        except Exception as e:
            warn(f"{e}\n")
    title()


def build(x64=False):
    fullname = f'{config.options["name"]} v{config.options["version"]}'
    if x64:
        fullname += "_x64"
    product = f'{config.pyIns["output"]}/{fullname}'
    code = []
    if config.options["noConfirm"]:
        code.append("--noConfirm")
    if config.modules["OneFile"]:
        code.append("--oneFile")
    for i in config.pyIns["file-imports"] + config.pyIns["hidden-imports"]:
        code.append(f"--hidden-import={i}")
    code.extend(['--clean', f'--icon={config.pyIns["icon"]}', f'--workpath={config.pyIns["temp"]}', f'--distpath={config.pyIns["output"]}', f'--paths={config.pyIns["imports"]}', *config.pyIns["data"]])
    try:
        print(fg.li_blue, end='')
        print("╔==============================╗")
        print("│      Building %sBits...      │" % ("64" if x64 else "32"))
        print("╚==============================╝")
        print(fg.cyan)
        if x64:
            subprocess.run([config.pyPaths["Ins64"], f'--name={fullname}', *code, config.pyIns["script"]])
        else:
            subprocess.run([config.pyPaths["Ins32"], f'--name={fullname}', *code, config.pyIns["script"]])
        if config.modules["OneLib"] and not config.modules["OneFile"]:
            if os.path.isfile(f'{product}/{fullname}.exe'):
                os.rename(f'{product}/{fullname}.exe', f'{product}/{config.options["name"]}.exe')
            if not os.path.isdir(f'{product}/{config.LIB["libDir"]}'):
                os.mkdir(f'{product}/{config.LIB["libDir"]}')
            files = [f.name for f in os.scandir(product) if f.name.endswith((".pyd",".zip",".dll")) or f.name == f'{config.options["name"]}.exe' or f.is_dir() and f.name != config.LIB["libDir"]]
            for i in files:
                if i.endswith("-info"):
                    shutil.rmtree(f'{product}/{i}')
                else:
                    shutil.move(f'{product}/{i}',f'{product}/{config.LIB["libDir"]}/{i}')
            if os.path.isfile(f'utils/wrapper/{config.LIB["Launcher"]}.exe'):
                shutil.copy(f'utils/wrapper/{config.LIB["Launcher"]}.exe', product)
        print(fg.rs)
        if config.options["CleanRoom"]:
            if os.path.isfile(f"{fullname}.spec"):
                os.remove(f"{fullname}.spec")
            if os.path.isdir(config.pyIns["temp"]):
                shutil.rmtree(config.pyIns["temp"])
        if config.hyperion["doTesting"]:
            exe = None
            if os.path.isfile(f"{product}/{fullname}.exe"):
                exe = f"{product}/{fullname}.exe"
            elif os.path.isfile(f'{product}/{config.LIB["Launcher"]}.exe'):
                exe = f'{product}/{config.LIB["Launcher"]}.exe'
            if exe is None:
                warn("Couldn't find executable to test")
            else:
                try:
                    child = subprocess.Popen(exe, cwd=product, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    child.communicate()[0]
                    if child.returncode == 1:
                        red("Failed to execute Program, retrying...\n")
                        obfuscate()
                    else:
                        green("Test completed successfully...\n")
                except Exception as e:
                    warn(f"{e}\n")
        title()
    except Exception as e:
        warn(f"{e}\n")

def signer(x64=False):
    if not os.path.isfile(config.pyPaths["signer"]):
        print("https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/")
        print("Mount the ISO and open up the [Installers] folder and install the appropriate msi for [Windows App Certification Kit]")
        print("Example: Windows App Certification Kit x64-x86_en-us.msi, which installs the executable to C:/Program Files (x86)/Windows Kits/10/App Certification Kit/signtool.exe\n")
        return
    else:
        fullname = f'{config.options["name"]} v{config.options["version"]}'
        if x64:
            fullname += "_x64"
        cmd = [config.pyPaths["signer"], 'sign', '/fd', 'SHA256', '/f', '../storage/private/certSigner.pfx', '/p', 'LAMBDACOURSE_5849']
        dirs = [
            '.exe',
            f'/{config.options["name"]}.exe',
            f'/{config.LIB["Launcher"]}.exe',
            f'/{fullname}.exe',
            f'/{config.LIB["libDir"]}/{config.options["name"]}.exe',
        ]
    try:
        print(fg(11), end='')
        print("╔=====================╗")
        print("│      EXESigner      │")
        print("╚=====================╝")
        print(fg.yellow)
        for i in dirs:
            if os.path.isfile(f'{config.pyIns["output"]}/{fullname}{i}'):
                subprocess.run([*cmd, f'{config.pyIns["output"]}/{fullname}{i}'])
                print()
    except Exception as e:
        warn(f"{e}\n")

def rar(x64=False):
    if not os.path.isdir("dist"):
        os.mkdir("dist")
    fullname = f'{config.options["name"]} v{config.options["version"]}'
    excluded = list(f"-x{i}" for i in config.rarFiles["exclude"])
    if x64:
        fullname += "_x64"
    product = f'{config.pyIns["output"]}/{fullname}'
    #if config.rarFiles["7Zip"]:
    #    cmd = [config.pyPaths["7zip"], "a"]
    if config.rarFiles["RAR"]:
        cmd = [config.pyPaths["rar"], "a", "-ep1", "-r", *excluded]
    if os.path.isfile(f"dist/{fullname}.rar"):
        os.remove(f"dist/{fullname}.rar")
    try:
        for i in config.rarFiles["empty"]:
            os.makedirs(f"utils/data/{i}", exist_ok=True)
        print(fg(166), end='')
        print("╔=======================╗")
        print("│      RARCompress      │")
        print("╚=======================╝", fg.yellow)
        if os.path.isfile(f'{product}.exe'):
            subprocess.run([*cmd, f"dist/{fullname}.rar", f'{product}.exe', *config.rarFiles["include"]])
        elif os.path.isfile(f'{product}/{config.LIB["Launcher"]}.exe') and os.path.isdir(f'{product}/{config.LIB["libDir"]}'):
            subprocess.run([*cmd, f"dist/{fullname}.rar", f'{product}/{config.LIB["Launcher"]}.exe', *config.rarFiles["include"], f'{product}/{config.LIB["libDir"]}'])
        print(fg.rs)
    except Exception as e:
        warn(f"{e}\n")

if __name__ == "__main__":
    title()
    main()