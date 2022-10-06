def getStudent():
    if not len(_vars.courses[_vars.selected[0]]):
        warn("No hay alumnos registrados\n")
        return
    student = None
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        if _vars.selected[1] in _vars.courses[_vars.selected[0]]:
            print(f"{fg.li_blue}Alumno: {_vars.selected[1]} {_vars.courses[_vars.selected[0]][_vars.selected[1]][0]}\n")
        else:
            print(f"{fg.li_blue}Alumno: {_vars.selected[1]}\n")
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", f"{fg.cyan}Seleccionar alumno", True)
        mPrint("[2].", f"{fg.yellow}Introducir DNI", True)
        mPrint("[3].", f"{fg.green}Confirmar curso", True)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput()
        if action == "0":
            return False
        elif action == "1":
            student = listStudents()
            if student is not None:
                _vars.selected[1] = student
        elif action == "2":
            print("Introducir DNI:\n")
            dni = intInput(True)
            if dni is not None and dni > 0:
                if dni not in _vars.courses[_vars.selected[0]]:
                    warn("Este DNI no esta registrado!\n")
                elif not alt_funcs.validateDNI(dni):
                    warn("Este DNI es invalido!\n")
                else:
                    student = dni
            else: elseval()
            if student is not None:
                _vars.selected[1] = student
        elif action == "3":
            return student
        else:
            elseval()

def getCourse():
    course = None
    _vars.exitSubMenu = False
    while not _vars.exitSubMenu:
        if _vars.selected[0] is not None:
            print(f"{fg(80,171,234)}Curso: {_vars.selected[0]} {fg(234,160,80)}Turno: {_vars.turns[_vars.selected[0]]}\n")
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPCIONES {fg.magenta}>>-----")
        mPrint("[1].", f"{fg.cyan}Seleccionar curso", True)
        mPrint("[2].", f"{fg.yellow}Introducir curso", True)
        mPrint("[3].", f"{fg.green}Confirmar curso", True)
        print()
        mPrint("[0].", f"{fg.li_red}[SALIR]", True)
        print()
        action = xinput()
        if action == "0":
            return False
        elif action == "1":
            course = listCourses()
            if course is not None:
                _vars.selected[0] = course
        elif action == "2":
            course = inputCourse()
            if course is not None:
                _vars.selected[0] = course
        elif action == "3":
            if course is None:
                warn("Debes seleccionar un curso primero\n")
            else:
                return course
        else:
            elseval()