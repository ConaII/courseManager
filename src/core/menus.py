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
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"{fg(152,85,211)}Gestionar cursos", True)
            mPrint("[2].", f"{fg(85,200,168)}Importar datos", True)
            mPrint("[3].", f"{fg(216,84,22)}Exportar datos", True)
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
                changeMenu("manageCourses")
            elif action == "2":
                warn("Aún no implementado\n")
            elif action == "3":
                warn("Aún no implementado\n")
            elif action == "4":
                warn("Aún no implementado\n")
            else:
                elseval(action)
        while funcMenu == "manageCourses" and not _vars.exitMenu:
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
            try:
                if filters is not None:
                    pass
            except NameError:
                filters = set()
            if len(filters):
                strList = ", ".join(filters)
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
                xProgram.searchStudent("dni", filters)
            elif action == "2":
                xProgram.searchStudent("name", filters)
            elif action == "3":
                course = xProgram.selCourse(select=False, filters=filters)
                if course is not None:
                    if course in filters:
                        warn(f"Se elimino el curso {course} del filtro.\n")
                        filters.remove(course)
                    else:
                        green(f"Se añadio el curso {course} al filtro.\n") 
                        filters.add(course)
            elif action == "4":
                turn = xProgram.selTurn(filters=filters)
                if turn is not None:
                    if turn in filters:
                        warn(f"Se elimino el turno {turn} del filtro.\n")
                        filters.remove(turn)
                    else:
                        green(f"Se añadio el turno {turn} al filtro.\n")
                        filters.add(turn)
            else:
                elseval()
        while funcMenu == "export" and not _vars.exitMenu:
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", "Export in courses directory", 1)
            mPrint("[2].", f"{fg(190,50,190)}Export in custom directory.", 1)
            mPrint("[3].", f"{fg(230,220,46)}Favorite directories.", 1)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", 1)
            print()
            action = xinput()
            if action == "0":
                return
            elif action == "1":
                fileVal("save")
            elif action == "2":
                dirVal("save")
            elif action == "3":
                favDirs("save")
        while funcMenu == "import" and not _vars.exitMenu:
            pass
        while funcMenu == "options" and not _vars.exitMenu:
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"{fg(218,145,30)}Test", True)
            mPrint("[2].", f"{fg(78,226,178)}Word", True)
            mPrint("[3].", f"{fg(80,118,222)}Moment", True)
            mPrint("[4].", f"{fg(116,90,202)}Settings", True)
            mPrint("[5].", f"{fg(110,218,128)}Testing", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput()
            if action == "0":
                return

def exportFile():
    pass

def importFile():
    print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
    mPrint("[1].", "Export in courses directory", 1)
    mPrint("[2].", f"{fg(190,50,190)}Export in custom directory.", 1)
    mPrint("[3].", f"{fg(230,220,46)}Favorite directories.", 1)
    print()
    mPrint("[0].", f"{fg.li_red}[SALIR]", 1)
    print()
    action = xinput()
    if action == "0":
        return
    elif action == "1":
        fileVal("save")
    elif action == "2":
        dirVal("save")
    elif action == "3":
        favDirs("save")

def fileManager(mode, path="courses/", file=None):
    parse = True if isinstance(file, str) else False
    dict_ = {
        "save": "import",
        "load": "export",
    }
    if not path.endswith('/'):
        path += '/'
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", "Export in courses directory", 1)
        mPrint("[2].", f"{fg(190,50,190)}Export in custom directory.", 1)
        mPrint("[3].", f"{fg(230,220,46)}Favorite directories.", 1)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", 1)
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            fileVal("save")
        elif action == "2":
            dirVal("save")
        elif action == "3":
            favDirs("save")
    while not _vars.exitSubMenu:
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
            if mode != "save":
                red(f"No hay archivos para cargar\n")
                return
        if os.listdir(path) == [] and mode != "save":
            red(f"No hay archivos para cargar\n")
            return
        fileList = [f.name for f in os.scandir(path) if f.is_file() and f.name.endswith(('.wsa','.xls'))]
        strList = [f"{fg(90,170,238)}{funcs.get_super(i+1)}{fg(135)}'{v}'" for i, v in enumerate(fileList)]
        strList = f"{fg(90,170,238)}, ".join(strList)
        if not parse:
            if mode == "save":
                if alt_funcs.isNew():
                    red("ALERTA: No hay datos que guardar.")
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
                while file.lower().endswith(dict_[mode][2]):
                    file = file[:-len(dict_[mode][2])]
            if file is False:
                warn("No coincidences found.\n")
            elif mode == "save":
                if os.path.isfile(f"{path}{file}{dict_[mode][2]}"):
                    while True:
                        red(f'ALERTA: El archivo "{file}.wsa" ya existe, reemplazarlo?')
                        mPrint("[1].", "Confirmar.", True)
                        mPrint("[2].", "Salir.", True)
                        print()
                        action = xinput(False)
                        if action == "1":
                            if funcs.saveGame(file, path=path):
                                return
                        if action in {"1","2"}:
                            break
                        else:
                            elseval(action)
                elif funcs.saveGame(file, path=path):
                    break
            elif mode == "load":           
                if funcs.loadGame(file, path=path):
                    break
            elif mode == "mod":
                if funcs.loadMod(file, path=path):
                    break
        else:
            elseval()
        if parse: break