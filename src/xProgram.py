from core import _vars, menus
from utils import funcs, alt_funcs
from utils.funcs import *

def addCourse():
    course = inputCourse()
    if course is not None:
        _vars.courses[course] = {}

def delCourse():
    if _vars.courses == {}:
        warn("No hay cursos para eliminar")
    course = inputCourse()
    if course in _vars.courses:
        _vars.courses.pop(course)

def manageCourse(course=None):
    print(f"{fg.magenta}-----<< {fg(240,210,40)}OPTIONS {fg.magenta}>>-----")
    mPrint("[1].", f"{fg(110,218,128)}Añadir alumno", True)
    mPrint("[2].", f"{fg(152,85,211)}Gestionar alumnos", True)
    mPrint("[3].", f"{fg(215,70,60)}Eliminar alumno", True)
    print()
    mPrint("[0].", f"{fg.li_red}[GO BACK]", True)
    print()
    action = xinput()
    if action == "0":
        return 

def inputCourse():
    print("Introducir año:")
    year = intInput()
    if year == 0:
        return
    if year is not None:
        print("Introducir division:")
        div = intInput()
        if div == 0:
            return
        if div is not None:
            return f"{year}º{div}"

def listCourses():
    pass
