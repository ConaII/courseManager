# Installed
from sty import bg, ef, fg, rs
# Program
from core import _vars, menus
from utils import funcs, alt_funcs
from utils.funcs import *

#class Student():
#    def __init__(self, DNI, Name):
#        self.DNI = DNI
#        self.Name = Name

def selTurn(filters=set()):
    c1 = fg(228,78,56) if "Mañana" in filters else fg.cyan
    c2 = fg(228,78,56) if "Tarde" in filters else fg.cyan
    c3 = fg(228,78,56) if "Noche" in filters else fg.cyan
    while True:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", f"{c1}Mañana", True)
        mPrint("[2].", f"{c2}Tarde", True)
        mPrint("[3].", f"{c3}Noche", True)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput(False)
        if action == "0":
            break
        elif action in {"1","2","3"}:
            return _vars.codeList["turnList"][int(action)-1]
        else:
            elseval(action)

def addCourse():
    course = None
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
    if course in _vars.courses:
        warn("Este curso ya existe!\n")
    elif course is not None:
        turn = selTurn()
        if turn is not None:
            _vars.courses[course] = {} 
            _vars.turns[course] = turn

def delCourse(course):
    while True:
        red("Estas seguro? Esta accion no se podra deshacer.")
        mPrint("[1].", "Confirmar", True)
        mPrint("[2].", "Volver", True)
        print()
        action = xinput(False)
        if action == "1":
            if course in _vars.courses:
                _vars.courses.pop(course)
            if course in _vars.turns:
                _vars.turns.pop(course)
            _vars.selected = [None, None]
            print(f"Se elimino el curso {course}.\n")
        if action in {"1","2"}:
            break
        else:
            elseval(action)


def selCourse(select=True, filters=set()):
    indexList = list(_vars.courses)
    while True:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        for i,x in enumerate(indexList):
            if x in filters:
                mPrint(f"[{i+1}].", f"{fg(228,78,56)}{x}")
            else:
                mPrint(f"[{i+1}].", x)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput(False).replace('°','º').replace('-','º')
        course = alt_funcs.getByIndex(indexList, action)
        if course is None:
            pass
        elif action == "0":
            #_vars.selected[0] = None
            return
        elif course in indexList:
            if not select:
                return course
            else:
                _vars.selected[0] = course
                return
        else:
            elseval(action)

def modCourse():
    _vars.exitMenu = False  
    while not _vars.exitMenu:
        course, student = _vars.selected
        if course is None:
            return
        print(f"{fg(58,118,238)}Curso: {fg.li_grey}{course} {fg(114,78,220)}Turno: {fg.li_grey}{_vars.turns[course]}\n")
        if student in _vars.courses[course]:
            print(f"{fg.li_blue}Alumno: {fg.li_grey}{_vars.courses[course][student][0]} {fg.li_grey}{alt_funcs.formatAmount(student, 1)}\n")
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", f"{fg(85,200,90)}Añadir alumno", True)
        mPrint("[2].", f"{fg(230,180,98)}Seleccionar alumno", True)
        mPrint("[3].", f"{fg(152,85,211)}Modificar alumno", True)
        mPrint("[4].", f"{fg(215,70,60)}Eliminar alumno", True)
        print()
        mPrint("[5].", f"{fg(240,70,140)}Cambiar turno del curso", True)
        print()
        mPrint("[0].", f"{fg.li_red}[VOLVER]", True)
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            addStudent(course)
        elif action == "2":
            if not len(_vars.courses[course]):
                warn("No hay ningun alumno añadido.\n")
            else:
                selStudent(course)
        elif action == "3":
            if student is None:
                warn("No hay un alumno seleccionado\n")
            else:
                modStudent()
        elif action == "4":
            if student is None:
                warn("No hay un alumno seleccionado\n")
            else:
                delStudent(course, student)
        elif action == "5":
            turn = selTurn()
            if turn is not None:
                _vars.turns[course] = turn
                print(f"Se cambio el turno del curso a {turn}\n")
        else:
            elseval(action)

def addStudent(course):
    name, dni = None
    while True:
        if name is None:
            print(f"Introducir nombres (Separar con espacios):\n")
            name = xinput(False)
            if name == "0":
                break
            elif name == "":
                print("Puedes salir de este menu introduciendo '0'\n")
                name = None
        elif len(name):
            print("Introducir DNI:\n")
            dni = intInput(True)
            if dni == 0:
                break
            elif dni is not None and dni > 0:
                if dni in _vars.courses[course]:
                    warn("El DNI introducido ya esta registrado.\n")
                elif not alt_funcs.validateDNI(str(dni)): 
                    warn("El DNI introducido es invalido.\n")
                else:
                    _vars.courses[course][dni] = [name]
                    break
        else: elseval(name)

def delStudent(course, student):
    while True:
        red("Estas seguro? Esta accion no se podra deshacer.")
        mPrint("[1].", "Confirmar", True)
        mPrint("[2].", "Volver", True)
        print()
        action = xinput(False)
        if action == "1":
            if student in _vars.courses[course]:
                _vars.courses[course].pop(student)
                _vars.selected[1] = None
                print(f"Se elimino el alumno {student} del curso {course}.\n")
        if action in {"1","2"}:
            break
        else:
            elseval(action)

def selStudent(course):
    indexList = list(_vars.courses[course])
    while True:
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        for i,x in enumerate(indexList):
            mPrint(f"[{i+1}].", f"{_vars.courses[course][x][0]} {fg.li_grey}{alt_funcs.formatAmount(x, 1)}")
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
            _vars.selected[1] = student
            return
        else:
            elseval(student)

def modStudent():
    _vars.exitMenu = False
    while not _vars.exitSubMenu:
        course, student = _vars.selected
        if None in {course, student}:
            return
        print(f"{fg(58,118,238)}Curso: {fg.li_grey}{course} {fg(114,78,220)}Turno: {fg.li_grey}{_vars.turns[course]}\n")
        if student in _vars.courses[course]:
            print(f"{fg.li_blue}Alumno: {fg.li_grey}{_vars.courses[course][student][0]} {fg.li_grey}{alt_funcs.formatAmount(student, 1)}\n")
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", f"{fg(110,218,128)}Cambiar Curso", True)
        mPrint("[2].", f"{fg(130,80,230)}Modificar Nombre", True)
        mPrint("[3].", f"{fg(215,70,60)}Modificar DNI", True)
        print()
        mPrint("[0].", f"{fg.li_red}[VOLVER]", True)
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            newCourse = selCourse()
            if newCourse is not None:
                _vars.courses[newCourse][student] = _vars.courses[course][student]
                _vars.courses[course].pop(student)
                _vars.selected[0] = newCourse  
        elif action == "2":
            print(f"Introducir nombres (Separar con espacios):\n")
            name = xinput(False)
            if name == "0":
                pass
            elif name is not None and len(name):
                _vars.courses[course][student][0] = name
                green("El nombre fue modificado correctamente.")
            else:
                elseval(name)
        elif action == "3": 
            print("Introducir DNI:\n")
            dni = intInput(True)
            if dni == 0:
                pass
            elif dni is not None and dni > 0:
                if dni in _vars.courses[course]:
                    warn("El DNI introducido ya esta registrado.\n")
                elif not alt_funcs.validateDNI(str(dni)): 
                    warn("El DNI introducido es invalido.\n")
                else:
                    _vars.courses[course][dni] = _vars.courses[course][student]
                    _vars.courses[course].pop(student)
                    _vars.selected[1] = dni
                    green("El DNI fue modificado correctamente.")
            else: elseval(dni)
        else:
            elseval(action)

def filterList(filters=set()):
    dict_ = {}
    for course, students in _vars.courses.items():
        dict_.update({student:course for student in students})
    dict_ = {k:v for k, v in sorted(dict_.items(), key=lambda data: _vars.courses[data[1]][data[0]][0])}
    if len(filters):
        turns = []
        courses = [] 
        for i in filters:
            if i in _vars.codeList["turnList"]: turns.append(i)
            elif i in _vars.courses: courses.append(i)
        if len(turns):
            dict_ = {k:c for k, c in dict_.items() if _vars.turns[c] in turns}
        if len(courses):
            dict_ = {k:c for k, c in dict_.items() if c in courses}
    return dict_

def searchStudent(type_, filters=set()):
    dict_, search = filterList(filters), None
    while True:
        if search is None:
            if type_ == "name":
                print(f"Introducir nombres (Separar con espacios):\n")
                name = xinput(False)
                if name == "0":
                    return
                elif name == "":
                    print("Puedes salir de este menu introduciendo '0'\n")
                elif name is not None and len(name):
                    search = name
                else:
                    elseval(name)
            if type_ == "dni":
                print("Introducir DNI:\n")
                dni = intInput(True)
                if dni == 0:
                    return
                elif dni is not None and dni > 0:
                    search = dni
                else: elseval(dni)
        else:
            indexDict = {}
            if type_ == "name":
                indexDict = {student:course for student,course in dict_.items() if any(x in search.split() for x in _vars.courses[course][student][0].split())}
            elif type_ == "dni":
                indexDict = {student:course for student,course in dict_.items() if  f"{search}" in f"{student}"}
            if not len(indexDict):
                warn("No se encontraron resultados.\n")
            print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
            for i, (student, course) in enumerate(indexDict.items()):
                mPrint(f"[{i+1}].", f"{_vars.courses[course][student][0]} {fg.li_grey}{alt_funcs.formatAmount(student, 1)}")
            print()
            mPrint("[1].", f"{fg(230,180,98)}Cambiar", True)
            print()
            mPrint("[0].", f"{fg.li_red}[SALIR]", True)
            print()
            action = xinput(False).replace('.','_')
            student = alt_funcs.getByIndex(list(indexDict), action)
            if student is None:
                pass
            elif action == "0":
                return
            elif action == "1":
                search = None
            elif student in indexDict:
                _vars.selected[1] = student
                return
            elif alt_funcs.isWhole(action) and int(float(action)) in indexDict:
                _vars.selected[1] = int(float(action))
                return
            else:
                elseval(action)
