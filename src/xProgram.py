from core import _vars, menus
from utils import funcs, alt_funcs
from utils.funcs import *

class Student():
    def __init__(self, DNI, Name):
        self.DNI = DNI
        self.Name = Name

def addCourse():
    course = inputCourse(True)
    if course in _vars.courses:
        warn("Este curso ya existe!\n")
    elif course is not None:
        while True:
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"Mañana", True)
            mPrint("[2].", f"Tarde", True)
            mPrint("[3].", f"Noche", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput(False)
            if action == "0":
                break
            elif action in {"1","2","3"}:
                turn = _vars.var["turnList"][int(action)-1]
                _vars.courses[course] = {} 
                _vars.turns[course] = turn
                break
            else:
                elseval()
    else:
        warn("Selecciona un curso primero!\n")

def delCourse():
    if not len(_vars.courses):
        warn("No hay cursos que eliminar.\n")
    else:
        course = getCourse()
        if course not in {None,False}:
            _vars.courses.pop(course)
            _vars.turns.pop(course)

def modCourse():
    _vars.selected[0] = None 
    _vars.exitMenu = False  
    while not _vars.exitMenu:
        if _vars.selected[0] is not None:
            print(f"{fg(80,171,234)}Curso: {_vars.selected[0]} {fg(234,160,80)}Turno: {_vars.turns[_vars.selected[0]]}\n")
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", f"{fg(85,200,90)}Añadir alumno", True)
        mPrint("[1].", f"{fg(226,100,56)}Seleccionar alumno", True)
        mPrint("[2].", f"{fg(240,70,140)}Cambiar turno", True)
        mPrint("[3].", f"{fg(215,70,60)}Reiniciar curso", True)
        ñmPrint("[4].", f"{fg(152,85,211)}Gestionar alumnos", True)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            selCourse()
        elif action == "2": 
            while True:
                print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
                mPrint("[1].", f"Mañana", True)
                mPrint("[2].", f"Tarde", True)
                mPrint("[3].", f"Noche", True)
                print()
                mPrint("[0].", f"{fg.li_red}[SALIR]", True)
                print()
                action = xinput(False)
                if action == "0":
                    break
                elif action in {"1","2","3"}:
                    turn = _vars.var["turnList"][int(action)-1]
                    _vars.turns[_vars.selected[0]] = turn
                    print(f"Se cambio el turno del curso a {turn}\n")
                    break
                else:
                    elseval()
        elif action == "3":
            while True:
                red("Estas seguro? Esta accion no se podra deshacer.")
                mPrint("[1].", "Confirmar", True)
                mPrint("[2].", "Volver", True)
                print()
                action = xinput(False)
                if action == "1":
                    _vars.courses[_vars.selected[0]] = {}
                    print(f"Se reestablecio el curso {_vars.selected[0]}\n")
                if action in {"1","2"}:
                    break
                else:
                    elseval()
        elif action == "4":
            manageStudents()

def addStudent():
    while True:
        print(f"Introducir nombres (Separar con espacios):\n")
        name = xinput(False)
        if name == "0":
            return False
        if name is not None and len(name):
            print("Introducir DNI:\n")
            dni = intInput(True)
            if dni == 0:
                return False
            if dni is not None and dni > 0:
                if dni in _vars.courses[_vars.selected[0]]:
                    warn("Este DNI ya esta registrado!\n")
                elif not alt_funcs.validateDNI(str(dni)): 
                    warn("Este DNI es invalido!\n")
                else:
                    _vars.courses[_vars.selected[0]][dni] = [name]
                    return True
            else: elseval()
        else: elseval()

def manageStudents():
    _vars.selected[1] = None
    _vars.exitMenu = False
    while not _vars.exitMenu:
        if not len(_vars.courses[_vars.selected[0]]):
            if addStudent() is False:
                return
        elif _vars.selected[1] is None:
            if getStudent() is False:
                return
        else:
            if _vars.selected[0] is not None:
                print(f"{fg(80,171,234)}Curso: {_vars.selected[0]} {fg(234,160,80)}Turno: {_vars.turns[_vars.selected[0]]}\n")
            if _vars.selected[1] in _vars.courses[_vars.selected[0]]:
                print(f"{fg.li_blue}Alumno: {_vars.selected[1]} {_vars.courses[_vars.selected[0]][_vars.selected[1]][0]}\n")
            else:
                print(f"{fg.li_blue}Alumno: {_vars.selected[1]}\n")
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            mPrint("[1].", f"{fg(230,216,100)}Elegir alumno", True)
            mPrint("[2].", f"{fg(110,218,128)}Añadir alumno", True)
            mPrint("[3].", f"{fg(130,80,230)}Modificar alumno", True)
            mPrint("[4].", f"{fg(215,70,60)}Eliminar alumno", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput()
            if action == "0":
                return
            elif action == "1":
                getStudent()
            elif action == "2": 
                addStudent()
            elif action == "3":
                _vars.exitSubMenu = False
                while not _vars.exitSubMenu:
                    pass
            elif action == "4":
                while True:
                    red("Estas seguro? Esta accion no se podra deshacer.")
                    mPrint("[1].", "Confirmar", True)
                    mPrint("[2].", "Volver", True)
                    print()
                    action = xinput(False)
                    if action == "1":
                        _vars.courses[_vars.selected[0]].pop(_vars.selected[1])
                        print(f"Se elimino el alumno {_vars.selected[1]}\n")
                    if action in {"1","2"}:
                        break
                    else:
                        elseval()

def inputCourse(new=False):
    while True:
        print("Introducir año:\n")
        year = intInput()
        if year == 0:
            return
        if year is not None:
            print("Introducir division:\n")
            div = intInput()
            if div == 0:
                return
            if div is not None: 
                course = f"{year}º{div}"
                if new or course in _vars.courses:
                    return course
                else:
                    warn("Este curso no existe aún.\n")
                    break

def selCourse():
    indexList = list(_vars.courses)
    while True:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        for i,x in enumerate(indexList):
            mPrint(f"[{i+1}].", f"{x}")
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput(False).replace('°','º').replace('-','º')
        course = alt_funcs.getByIndex(indexList, action)
        if course is None:
            pass
        elif action == "0":
            return
        elif course in indexList:
            return course
        else:
            elseval()

def selStudents():
    indexList = list(_vars.courses[_vars.selected[0]])
    while True:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        for i,x in enumerate(indexList):
            mPrint(f"[{i+1}].", f"{x}")
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput(False)
        student = alt_funcs.getByIndex(indexList, action)
        if student is None:
            pass
        elif action == "0":
            return
        elif student in indexList:
            return student
        else:
            elseval()