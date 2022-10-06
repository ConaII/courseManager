# Installed
from sty import bg, ef, fg, rs
# Program
from core import _vars
from utils import funcs, alt_funcs
from utils.funcs import *

def changeMenu(funcMenu):
    _vars.exitMenu = False
    if funcMenu != _vars.menu:
        prevFunc = _vars.menu
        menuLoop(funcMenu)
        _vars.menu = prevFunc
    else:
        red("Ya estas en este menu.\n")

def menuLoop(funcMenu):
    import xProgram
    _vars.menu = funcMenu
    while _vars.keepAlive:
        if _vars.exitMenu:
            return
        while funcMenu == "main" and not _vars.exitMenu:
            if _vars.options["menuLogo"]:
                alt_funcs.logo()
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"{fg(152,85,211)}Gestionar cursos", True)
            mPrint("[2].", f"{fg(30,222,101)}Importar datos", True)
            mPrint("[3].", f"{fg(224,75,35)}Exportar datos", True)
            mPrint("[4].", f"{fg(30,130,240)}Opciones", True)
            print()
            mPrint("[0].", f"{fg.li_red}[CERRAR]", True)
            print() 
            action = xinput()
            if action == "0":
                red("Estas seguro? Esto cerrara el programa!")
                mPrint("[1].", "Confirmar", True)
                mPrint("[2].", "Volver", True)
                print()
                action = xinput(False)
                if action == "1":
                    _vars.keepAlive = False
                    _vars.exitMenu = True
                elif action != "2":
                    elseval(action)
            elif action == "1":
                changeMenu("manage")
            elif action == "2":
                loadMenu()
            elif action == "3":
                saveMenu()
            elif action == "4":
                changeMenu("options")
            else:
                elseval(action)
        while funcMenu == "options" and not _vars.exitMenu:
            toMode = [f"{fg(215,70,60)}disabled",f"{fg(60,215,40)}enabled"]
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"Toggle clearMode", True)
            mPrint("[2].", f"Toggle menuLogo", True)
            mPrint("[3].", f"Manage Formats", True)
            mPrint("[4].", f"Manage Config", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput()
            if action == "0":
                return
            elif action == "1":
                value = not _vars.options["clearMode"]
                if value: funcs.clear()
                print(f"You {toMode[int(value)]}{fg.rs} the clear mode.")
                print()
                _vars.options["clearMode"] = value
                funcs.saveConfig()
            elif action == "2":
                value = not _vars.options["menuLogo"]
                print(f"You {toMode[int(value)]}{fg.rs} the menu logo.")
                print()
                _vars.options["menuLogo"] = value
                funcs.saveConfig()
            elif action == "3":
                _vars.exitSubMenu = False
                while not _vars.exitSubMenu:
                    toMode = [f"{fg(215,70,60)}non-spaced",f"{fg(60,215,40)}spaced"]
                    print(f"{fg.magenta}-----<< {fg(240,210,40)}OPTIONS {fg.magenta}>>-----")
                    mPrint("[1].", "Toggle menu space", True)
                    mPrint("[2].", "Toggle index space", True)
                    mPrint("[3].", "Thousand separator", True)
                    print()
                    mPrint("[0].", f"{fg.li_red}[GO BACK]", True)
                    print()
                    action = xinput()
                    if action == "0":
                        break
                    elif action == "1":
                        _vars.formats["spaces"][0] = int(not bool(_vars.formats["spaces"][0]))
                        print(f'Menu format changed to {toMode[_vars.formats["spaces"][0]]}')
                        print()
                        funcs.saveConfig()
                    elif action == "2":
                        _vars.formats["spaces"][1] = int(not bool(_vars.formats["spaces"][1]))
                        print(f'Index format changed to {toMode[_vars.formats["spaces"][1]]}')
                        print()
                        funcs.saveConfig()
                    elif action == "3":
                        sepType = [
                            f"{fg(215,70,60)}No separator",
                            f"{fg(240,190,25)}Dots separator",
                            f"{fg(60,215,40)}Comma separator" 
                        ]
                        _vars.exitSubMenu = False
                        while not _vars.exitSubMenu:
                            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPTIONS {fg.magenta}>>-----")
                            mPrint("[1].", sepType[0], True)
                            mPrint("[2].", sepType[1], True)
                            mPrint("[3].", sepType[2], True)
                            print()
                            mPrint("[0].", f"{fg.li_red}[GO BACK]", True)
                            print()
                            action1 = xinput()
                            if action1 == "0": 
                                break
                            elif action1 in {"1","2","3"}:
                                value = int(action1)-1
                                if action == "3":
                                    _vars.formats["sep"] = value 
                                elif action == "4":
                                    _vars.formats["stats"][0] = value    
                                print(f'Separator format changed to {sepType[value]}')
                                print()
                                funcs.saveConfig()
                            else:
                                elseval(action)
                    else:
                        elseval(action)
            elif action == "4":
                _vars.exitSubMenu = False
                while not _vars.exitSubMenu:
                    print(f"{fg.magenta}-----<< {fg(240,210,40)}ACTIONS {fg.magenta}>>-----")
                    mPrint("[1].", "Save config", True)
                    mPrint("[2].", "Reload config", True)
                    mPrint("[3].", "Reset config", True)
                    print()
                    mPrint("[0].", f"{fg.li_red}[GO BACK]", True)
                    print()
                    action = xinput()
                    if action == "0":
                        break
                    elif action == "1":
                        funcs.saveConfig(msg=True)
                    elif action == "2":
                        funcs.loadConfig()
                    elif action == "3":
                        funcs.resetConfig()
                    else:
                        elseval(action)
            else:
                elseval(action)
        while funcMenu == "manage" and not _vars.exitMenu:
            course = _vars.selected[0]
            if course is not None:
                print(f"{fg(58,118,238)}Curso: {fg.li_grey}{course} {fg(114,78,220)}Turno: {fg.li_grey}{_vars.turns[course]}\n")
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"{fg(85,200,90)}Añadir curso", True)
            mPrint("[2].", f"{fg(230,180,98)}Seleccionar curso", True)
            mPrint("[3].", f"{fg(152,85,211)}Modificar curso", True)
            mPrint("[4].", f"{fg(215,70,60)}Eliminar curso", True)
            print()
            mPrint("[5].", f"{fg.li_blue}Buscador", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput()
            if action == "0":
                return
            elif action == "1":
                xProgram.addCourse()
            elif action == "2":
                if not len(_vars.courses):
                    warn("No hay ningun curso añadido.\n")
                else:
                    xProgram.selCourse()
            elif action == "3":
                if course is None:
                    warn("No hay un curso seleccionado.\n")
                else: 
                    xProgram.modCourse()
            elif action == "4":
                if course is None:
                    warn("No hay un curso seleccionado.\n")
                else: 
                    xProgram.delCourse(course)
            elif action == "5":
                if not len(_vars.courses):
                    warn("No hay ningun curso añadido.\n")
                if not any(len(x) for x in _vars.courses):
                    warn("No hay ningun alumno añadido.\n")
                else:
                    changeMenu("search")
            else:
                elseval(action)
        while funcMenu == "search" and not _vars.exitMenu:
            if len(_vars.filters):
                strList = ", ".join(_vars.filters)
                print(f"Filtros: {strList}\n")
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"{fg(110,218,128)}Buscar DNI", True)
            mPrint("[2].", f"{fg(152,85,211)}Buscar Nombre", True)
            mPrint("[3].", f"{fg(235,173,98)}Filtrar por Curso", True)
            mPrint("[4].", f"{fg(228,125,50)}Filtrar por Turno", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput()
            if action == "0":
                return
            elif action == "1":
                xProgram.searchStudent("dni")
            elif action == "2":
                xProgram.searchStudent("name")
            elif action == "3":
                course = xProgram.selCourse(select=False, filters=True)
                if course is not None:
                    if course in _vars.filters:
                        warn(f"Se elimino el curso {course} del filtro.\n")
                        _vars.filters.remove(course)
                    else:
                        green(f"Se añadio el curso {course} al filtro.\n") 
                        _vars.filters.add(course)
            elif action == "4":
                turn = xProgram.selTurn(filters=True)
                if turn is not None:
                    if turn in _vars.filters:
                        warn(f"Se elimino el turno {turn} del filtro.\n")
                        _vars.filters.remove(turn)
                    else:
                        green(f"Se añadio el turno {turn} al filtro.\n")
                        _vars.filters.add(turn)
            else:
                elseval(action)

def saveMenu():
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", "Export in courses directory", True)
        mPrint("[2].", f"{fg(190,50,190)}Explore directories", True)
        mPrint("[3].", f"{fg(230,220,46)}Favorite directories", True)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            fileManager("save")
        elif action == "2":
            dirManager("save")
        elif action == "3":
            favManager("save")
        else:
            elseval(action)

def loadMenu():
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", "Importar desde curses", True)
        mPrint("[2].", f"{fg(190,50,190)}Explorar directorios", True)
        mPrint("[3].", f"{fg(230,220,46)}Favoritos", True)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            fileManager("load")
        elif action == "2":
            dirManager("load")
        elif action == "3":
            favManager("load")
        else:
            elseval(action)


def favManager(mode):
    dict_ = _vars.config["favorites"]
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        print("Remover: 'rem <index>' | Añadir path: 'add <path>'")
        print("Navegar: 'nav'")
        print()
        print(f"{fg.magenta}-----<< {fg(230,220,46)}FAVORITES {fg.magenta}>>-----\n")
        if len(dict_) > 0:
            for i, k in enumerate(dict_):
                path = dict_[k] if not dict_[k].endswith('/') else dict_[k][:-1] 
                mPrint(f"{i+1}.", f"{fg(116,190,245)}{k} {fg.li_grey}({path})", 1)
            print()
        mPrint("[0].", f"{fg.li_red}[Exit]", 1)
        print()
        action = xinput(False)
        action = alt_funcs.getByIndex(list(dict_), action)
        if action is None:
            pass
        elif action == "":
            elseval(action)
        else:
            args = action.split()
            if action == "0":
                return
            elif action in dict_:
                fileManager(mode, dict_[action])
            elif args[0] in {"nav","add"}:
                path = None
                if args[0] == "nav":
                    path = dirManager(mode, nav=True)
                elif len(args) > 1:
                    path = ' '.join(args[1:])
                else:
                    warn("Uso: add <path>\n")
                if path:
                    print("Write an alphanumeric name for prefix:\n")
                    name = xinput(False)
                    if not alt_funcs.isWhole(name) and len(name) > 0:
                        dict_[name] = path
                        funcs.saveConfig()
            elif args[0] in {"rem","del"}:
                if len(args) > 1 and len(dict_) > 0:
                    name = alt_funcs.getByIndex(list(dict_), args[1])
                    if name in dict_:
                        dict_.pop(name)
                        print(f"Removed {name} from favorites!\n")
                        funcs.saveConfig()
                    else:
                        warn("Invalid index.\n")
                elif not len(dict_):
                    warn("Add a path first\n")
                else:
                    warn("Uso: rem <index>\n")
            else:
                elseval(action)

def dirManager(mode, path0="courses", nav=False):
    dict_ = {
        "save": "save in",
        "load": "load from",
    }
    if nav:
        dict_[mode][1] = "favorite"
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        if not os.path.isdir(path0):
            os.makedirs(path0)
        dirList = [d.name for d in os.scandir(path0) if d.is_dir()]
        strList = [f"{fg(90,170,238)}{funcs.get_super(i+1)}{fg(135)}'{v}'" for i, v in enumerate(dirList)]
        strList = f"{fg(90,170,238)}, ".join(strList)
        if mode == "save":
            print(f"{fg.cyan}Introducir nombre o numero del directorio donde guardar.")
        else:
            print(f"{fg.cyan}Introducir nombre o numero del directorio donde cargar.")
        print(f"  {fg.li_grey}(Usar / como un prefijo para buscar coincidencias)\n")
        print(f"{fg.grey}  (Usar cd como un comando para navegar o moverse a carpetas)\n")
        print(f" - {strList}")
        print()
        mPrint("[0].", f"{fg.li_red}[GO BACK]", 1)
        print()
        path = xinput(False)
        path = alt_funcs.getByIndex(dirList, path)
        args = path.split()
        if path == "0":
            break
        elif path != "":
            if path.startswith("/"):
                path = alt_funcs.lookup(dirList, path[1:])
            if path is False:
                warn("No coincidences found.\n")
            elif args[0] == "cd":
                if len(args) > 1:
                    path = funcs.absPath(' '.join(args[1:])).replace('\\','/')
                    if os.path.isdir(f"{path0}/{path}"):
                        path0 = f"{path0}/{path}"
                    elif os.path.isdir(path):
                        path0 = path
                    else:
                        warn("Invalid path.\n")
                        continue
                    print(f"Path: {path0}\n") 
                else:
                    warn("Uso: cd <dir/relative/path>")
            elif os.path.isdir(f"{path0}/{path}"):
                path = path.replace('\\','/')
                if nav:
                    return f"{path0}/{path}"
                else:
                    fileManager(mode=mode, path=f"{path0}/{path}")
                    break
            elif not os.path.isdir(f"{path0}/{path}") and mode == "save":
                os.makedirs(f"{path0}/{path}", exist_ok=True)
        else:
            elseval(path)

def fileManager(mode, path="courses/", file=None):
    parse = True if isinstance(file, str) else False
    ext = ".wsa"
    if not path.endswith('/'):
        path += '/'
    #_vars.exitSubMenu = False
    #while not _vars.exitSubMenu:
    #    print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
    #    mPrint("[1].", "Utilize custom file format", True)
    #    mPrint("[2].", "Utilize excel file format", True)
    #    print()
    #    mPrint("[0].", f"{fg.li_red}[SALIR]", True)
    #    print()
    #    action = xinput()
    #    if action == "0":
    #        return
    #    elif action == "1":
    #        ext = ".wsa"
    #        break
    #    elif action == "2":
    #        ext = ".xls"
    #        break
    #    else:
    #        elseval(action)
    while not _vars.exitSubMenu:
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
            if mode != "save":
                warn(f"No hay archivos para cargar\n")
                return
        if os.listdir(path) == [] and mode != "save":
            warn(f"No hay archivos para cargar\n")
            return
        fileList = [f.name for f in os.scandir(path) if f.is_file() and f.name.endswith(ext)]
        strList = [f"{fg(90,170,238)}{funcs.get_super(i+1)}{fg(135)}'{v}'" for i, v in enumerate(fileList)]
        strList = f"{fg(90,170,238)}, ".join(strList)
        if not parse:
            if mode == "save":
                if alt_funcs.isNew():
                    warn("ALERTA: No hay datos que guardar.")
                print(f"{fg.cyan}Introducir nombre o numero de como guardar el archivo.")
                print(f"  {fg(75, 128, 162)}(Selecciona un archivo ya existente para reemplazarlo)")
            else:
                print(f"{fg.cyan}Introducir nombre o numero de que archivo cargar.")
            print(f"  {fg.li_grey}(Usar / como un prefijo para buscar coincidencias)\n")
            print(f" - {strList}")
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            file = xinput(False)
        if file == "0":
            return
        elif file != "":
            file = alt_funcs.getByIndex(fileList, file)
            if file.startswith('/'):
                file = alt_funcs.lookup(fileList, file[1:])
            if isinstance(file, str):
                while file.lower().endswith(ext):
                    file = file[:-len(ext)]
            if file is False:
                warn("No coincidences found.\n")
            elif mode == "save":
                if os.path.isfile(f"{path}{file}{ext}"):
                    while True:
                        warn(f'ALERTA: El archivo "{file}.wsa" ya existe, reemplazarlo?')
                        mPrint("[1].", "Confirmar.", True)
                        mPrint("[2].", "Salir.", True)
                        print()
                        action = xinput(False)
                        if action == "1":
                            if funcs.saveData(file, path=path):
                                return
                        if action in {"1","2"}:
                            break
                        else:
                            elseval(action)
                elif funcs.saveData(file, path=path):
                    break
            elif mode == "load":           
                if funcs.loadData(file, path=path):
                    break
        else:
            elseval(file)
        if parse: break