import sys

import regex as regex
import re
import functions as fn
import matplotlib.pyplot as plt
import numpy as np

# Create the vectors X and Y
def draw():
    x = np.array(range(-100, 100))
    plt.plot(x, x**2)
    plt.show()

history = ""


def out(output):
    print("  " + str(output))

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
    if 'i' in str:
        return "complex"
    else:
        return "var"


def computeFn(func, x):
    func = fn.pol_formatLine(func)
    func = re.sub(regex.checkLetter, str(x), func)
    try:
        res = eval(func)
    except ZeroDivisionError:
        res = fn.error("Division by 0.")
    return res


def evalVar(exp, elements):
    match = re.findall("(fun[A-Z])\((\d+|[a-z]+)\)", exp)               # replace funX(y) || funX(5) by their result
    if match:
        for m in match:
            fun = m[0]
            param = m[1]
            if fun in elements.keys():
                if param.isnumeric():
                    exp = re.sub(fun + "\(" + param + "\)", str(computeFn(elements[fun]["value"], param)), exp)
                    out(exp)
                elif param in elements.keys():
                    exp = re.sub(fun + "\(" + param + "\)", str(computeFn(elements[fun]["value"], elements[param]["value"])), exp)
                else:
                    return "Variable " + param + " is not assigned"
    match = re.findall(regex.checkLetter, exp)                          # replace X || y by their result
    if match:
        for m in match:
            var = m[0]
            if var in elements.keys():
                exp = re.sub(var, elements[var]["value"], exp)
    try:
        res = eval(exp)
    except ZeroDivisionError:
        res = fn.error("Division by 0.")
    return res


def assign(line, type, elements):
    exp = line.split('=')
    key = exp[0].strip()
    value = exp[1].strip()

    if value in elements.keys():                                        # x = y     => assign x
        elements[key] = elements[value]
    else:
        if type is None:
            newType = checkType(value)
            if newType == "var":                                        # x = 3 || x = y + 3 || x = funX(2) etc.
                value = evalVar(value, elements)
            else:
                out("type is complex")
            elements[key] = {"type": newType, "value": value}           # complexes a gerer
        elif type == "fn":
            key = key[0:4]
            elements[key] = {"type": type, "value": value}              # funX(x) = ...
        out(elements[key]["value"])
    return elements


def main():
    read_flags()
    line = ""
    elements = {}
    while line is not None:
        try:
            line = read_in()
            if len(line) == 0:
                fn.error("Empty input.")
            elif line == "env":
                for e in elements:
                    out(elements[e]["type"] + " " + e + " = " + str(elements[e]["value"]))
            elif line == "q" or line == "quit" or line == "exit":
                sys.exit(1)
            else:
                get = re.match(regex.get, line)
                if get:                                                     # "... = ?"
                    key = get.group(1).strip()
                    if key in elements.keys():                              # "x = ?"
                        out(elements[key]["value"])
                    elif key[0:3] == "fun":
                        if key[0:4] in elements.keys():                       # "funX(param) = ?"
                            match = re.match(regex.func, key)
                            if match:
                                param = match.group(2).strip()
                                if param.isnumeric():
                                    out(computeFn(elements[key[0:4]]["value"], param))
                                elif param in elements.keys():                                    # "funX(x) = ?"  /!\   gerer funX(x + 5)
                                    out(computeFn(elements[key[0:4]]["value"], elements[param]["value"]))
                                else:
                                    out(fn.error("The variable " + param + " is not assigned."))
                        else:
                            out(fn.error("The function " + key[0:4] + " is not defined."))
                    elif not re.match(regex.checkLetter, key):                          # "5 + 5 = ?"
                        try:
                            res = eval(fn.pol_formatLine(get.group(1).strip()))
                        except SyntaxError:
                            res = fn.error("Bad syntax.")
                        out(res)
                    else:                                                   # x + 5 = ?
                        out(evalVar(key, elements))

                elif re.match(regex.checkFunc, line):                       # funX(x) = ....
                    # out("assign func")
                    elements = assign(line, "fn", elements)
                elif re.match(regex.checkAssign, line):                     # x = ...
                    # out("assign")
                    elements = assign(line, None, elements)
                else:
                    out("Invalid input.")
        except KeyboardInterrupt:
            sys.exit(1)


draw()
main()
