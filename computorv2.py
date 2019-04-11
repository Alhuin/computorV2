# -*- coding: utf-8 -*-

import sys
import re
from includes import regex, utils as u
from includes.types import Matrice, Function


def evalVar(exp, data):
    match = re.findall("(fun[A-Z])\((\d+|[a-z]+)\)", exp)               # replace funX(y) || funX(5) by their result
    if match:
        for m in match:
            fun = m[0]
            param = m[1]
            if fun in data.keys():
                fn = data[fun]["value"]
                if param.isnumeric():
                    exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(param)), exp)
                    u.out(exp)
                elif param in data.keys():
                    exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(data[param]["value"])), exp)
                else:
                    return "Variable " + param + " is not assigned"
    match = re.findall(regex.checkLetter, exp)        # replace X || y by their result
    matrice = []
    if match:
        for m in match:
            var = m[0]
            if var in data.keys():
                if data[var]["type"] == "var":
                    exp = re.sub(var, str(data[var]["value"]), exp)
                elif data[var]["type"] == "matrice":
                    matrice.append(var)
    if len(matrice) == 0:
        try:
            res = eval(exp)
        except ZeroDivisionError:
            res = u.error("Division by 0.")
        return res
    else:
        i = 0
        prior = True
        matrices = {}
        while prior:
            prior = re.search("(\d+|[a-zA-Z])\s*([\*\/\%])\s*(\d+|[a-zA-Z])", exp)
            if prior:
                string = prior.group(0)
                nb1 = prior.group(1)
                ope = prior.group(2)
                nb2 = prior.group(3)
                if nb1.isnumeric() and nb2.isnumeric():
                    exp = exp.replace(string, str(eval(string)))
                else:
                    m = Matrice()
                    if nb1.isnumeric() and not nb2.isnumeric():
                        if ope == '/' or ope == '%':
                            return u.error("Can't resolve 'Real " + ope + " Matrice.")
                        if nb2 in data.keys():
                            m = data[nb2]["value"].calc(ope, {"type": "var", "value": u.intFloatCast(nb1)})
                    elif not nb1.isnumeric() and not nb2.isnumeric():
                        if nb2 in data.keys() and nb1 in data.keys():
                            m = data[nb2]["value"].calc(ope, data[nb1])
                    else:
                        if nb2 in data.keys():
                            m = data[nb1]["value"].calc(ope, {"type": "var", "value": u.intFloatCast(nb2)})
                    exp = exp.replace(string, "mat")
                    matrices[i] = m
                    i += 1
        print(exp)
        second = True
        i = 0
        print(matrices)
        while second:
            second = re.search("(\d+|mat)\s*([\+\-])\s*(\d+|mat)", exp)
            if second :
                string = second.group(0)
                nb1 = second.group(1)
                ope = second.group(2)
                nb2 = second.group(3)
                if nb1.isnumeric() and nb2.isnumeric():
                    exp = exp.replace(string, str(eval(string)))
                else:
                    m = Matrice()
                    if nb1 == "mat" and nb2 == "mat":
                        m = matrices[i]
                        m.calc(ope, {"type": "matrice", "value": matrices[i+1]})
                        matrices.pop(i)
                        matrices.pop(i)
                        # i += 2
                    elif nb1.isnumeric() and nb2 == "mat":
                        if ope == '-':
                            return u.error("Can't resolve 'Real - Matrice.")
                        m = m.parse(str(matrices[i]))
                        m.print()
                        m = m.calc('+', {"type": "var", "value": u.intFloatCast(nb1)})
                        # matrices.pop(i)
                        # i += 1
                    else:
                        m = matrices[i].calc(ope, {"type": "var", "value": u.intFloatCast(nb2)})
                        print(m.parse(str(matrices[i])))
                        matrices.pop(i)
                        # i += 1
                    exp = exp.replace(string, "mat")
                    matrices[i] = m
                    i += 1
                    print(matrices)







def assign(line, type, data):
    exp = line.split('=')
    key = exp[0].strip()
    value = exp[1].strip()

    if value in data.keys():                                        # x = y     => assign x
        data[key] = data[value]
    else:
        if type is None:
            newType = u.checkType(value)
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
            match = re.match(regex.func, key)
            fn = Function(value, match.group(2))
            key = match.group(1)
            data[key] = {"type": type, "value": fn}              # funX(x) = ...
        if data[key]["type"] == "matrice":
            data[key]["value"].print()
        elif data[key]["type"] == "fn":
            u.out(data[key]["value"].function)
        else:
            u.out(data[key]["value"])
    return data


def main():
    u.read_flags()
    line = ""
    data = {}
    while line is not None:
        try:
            line = u.read_in()
            if len(line) == 0:
                u.out(u.error("Empty input."))
            elif line == "env":
                for e in data:
                    u.out(data[e]["type"] + " " + e + " = " + str(data[e]["value"]))
            elif line[0:4] == "draw":
                match = re.match(regex.draw, line)
                if match:
                    key = match.group(1).strip()
                    if key in data.keys():
                        fn = data[key]["value"]
                        fn.draw(-100, 100)
                    else:
                        u.out(u.error("The function " + key + " is not assigned."))
            elif line == "q" or line == "quit" or line == "exit":
                sys.exit()
            else:
                get = re.match(regex.get, line)
                if get:                                                     # "... = ?"
                    key = get.group(1).strip()
                    if key in data.keys():                              # "x = ?"
                        if data[key]["type"] == "matrice":
                            data[key]["value"].print()
                        else:
                            u.out(data[key]["value"])
                    elif key[0:3] == "fun":
                        if key[0:4] in data.keys():                       # "funX(param) = ?"
                            match = re.match(regex.func, key)
                            if match:
                                param = match.group(2).strip()
                                fn = data[key[0:4]]["value"]
                                if param.isnumeric():
                                    u.out(fn.compute(param))
                                elif param in data.keys():              # "funX(x) = ?"  /!\   gerer funX(x + 5)
                                    if data[param]["type"] != "matrice":
                                        u.out(fn.compute(data[param]["value"]))
                                    else:
                                        u.out(u.error("Cannot apply a function to a matrice."))
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
