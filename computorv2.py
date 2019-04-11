import sys
import regex
import re
import utils as u
from .types import Matrice

history = ""

def read_flags():
    global details
    nbArgs = len(sys.argv)
    if nbArgs > 1 and sys.argv[1] == "-d":
        details = True


def read_in():
    global history
    user_input = input("> ")
    history += user_input + "\n"
    return user_input.strip()


def checkType(str):
    match = re.findall(regex.checkMatrice, str)
    if match:
        return "matrice"
    elif 'i' in str:
        return "complex"
    else:
        return "var"


def computeFn(func, x):
    func = u.formatLine(func)
    try:
        res = eval(func)
    except ZeroDivisionError:
        res = u.error("Division by 0.")
    return res


def evalVar(exp, data):
    match = re.findall("(fun[A-Z])\((\d+|[a-z]+)\)", exp)               # replace funX(y) || funX(5) by their result
    if match:
        for m in match:
            fun = m[0]
            param = m[1]
            if fun in data.keys():
                if param.isnumeric():
                    exp = re.sub(fun + "\(" + param + "\)", str(computeFn(data[fun]["value"], param)), exp)
                    u.out(exp)
                elif param in data.keys():
                    exp = re.sub(fun + "\(" + param + "\)", str(computeFn(data[fun]["value"], data[param]["value"])), exp)
                else:
                    return "Variable " + param + " is not assigned"
    match = re.findall(regex.checkLetter, exp)                          # replace X || y by their result
    if match:
        for m in match:
            var = m[0]
            if var in data.keys():
                exp = re.sub(var, data[var]["value"], exp)
    try:
        res = eval(exp)
    except ZeroDivisionError:
        res = u.error("Division by 0.")
    return res


def assign(line, type, data):
    exp = line.split('=')
    key = exp[0].strip()
    value = exp[1].strip()

    if value in data.keys():                                        # x = y     => assign x
        data[key] = data[value]
    else:
        if type is None:
            newType = checkType(value)
            if newType == "var":                                        # x = 3 || x = y + 3 || x = funX(2) etc.
                value = evalVar(value, data)
            elif newType == "matrice":
                mat = Matrice()
                value = Matrice.parse(mat, value)
                if value == None:
                    u.out(u.error("Matrice not well formated"))
                    return data
            else:
                u.out("type is complex")
            data[key] = {"type": newType, "value": value}           # complexes a gerer
        elif type == "fn":
            key = key[0:4]
            data[key] = {"type": type, "value": value}              # funX(x) = ...
        if data[key]["type"] == "matrice":
            data[key]["value"].print()
        else:
            u.out(data[key]["value"])
    return data


def main():
    read_flags()
    line = ""
    data = {}
    while line is not None:
        try:
            line = read_in()
            if len(line) == 0:
                u.out(u.error("Empty input."))
            elif line == "env":
                for e in data:
                    u.out(data[e]["type"] + " " + e + " = " + str(data[e]["value"]))
            elif line[0:4] == "draw":
                match = re.match(regex.draw, line)
                if match and match.group(1).strip() in data.keys():
                    u.draw(data[match.group(1).strip()]["value"], -100, 100)
                else:
                    u.out(u.error("The function " + match.group(1).strip() + " is not assigned"))
            elif line == "q" or line == "quit" or line == "exit":
                sys.exit(1)
            else:
                get = re.match(regex.get, line)
                if get:                                                     # "... = ?"
                    key = get.group(1).strip()
                    if key in data.keys():                              # "x = ?"
                        u.out(data[key]["value"])
                    elif key[0:3] == "fun":
                        if key[0:4] in data.keys():                       # "funX(param) = ?"
                            match = re.match(regex.func, key)
                            if match:
                                param = match.group(2).strip()
                                if param.isnumeric():
                                    u.out(computeFn(data[key[0:4]]["value"], param))
                                elif param in data.keys():                                    # "funX(x) = ?"  /!\   gerer funX(x + 5)
                                    u.out(computeFn(data[key[0:4]]["value"], data[param]["value"]))
                                else:
                                    u.out(u.error("The variable " + param + " is not assigned."))
                        else:
                            u.out(u.error("The function " + key[0:4] + " is not defined."))
                    elif not re.match(regex.checkLetter, key):                          # "5 + 5 = ?"
                        try:
                            res = eval(u.formatLine(get.group(1).strip()))
                        except SyntaxError:
                            res = u.error("Bad syntax.")
                        u.out(res)
                    else:                                                   # x + 5 = ?
                        u.out(evalVar(key, data))

                elif re.match(regex.checkFunc, line):                       # funX(x) = ....
                    data = assign(line, "fn", data)
                elif re.match(regex.checkAssign, line):                     # x = ...
                    data = assign(line, None, data)
                else:
                    print(re.match(regex.checkAssign, line))
                    u.out(u.error("Invalid input."))
        except KeyboardInterrupt:
            sys.exit()

main()
