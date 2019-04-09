#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import regex as regex
import re
import functions as fn


class Element:
  def __init__(self, type, strVal):
    self.type = type
    self.strVal = strVal


def read_flags():
    global details
    nbArgs = len(sys.argv)
    if nbArgs > 1 and sys.argv[1] == "-d":
        details = True


def read_in():
    print('PROGRAM: Type something, then hit Enter:')
    user_input = sys.stdin.readline().rstrip()
    return user_input


def checkType(str):
    if 'i' in str:
        return "complex"
    else:
        return "var"


def computeFn(func, x):
    func = fn.pol_formatLine(func)
    print(func)
    func = re.sub("([A-Z])", str(x), func, flags=re.IGNORECASE)
    print(func)
    res = eval(func)
    print(res)


def assign(line, type, elements):
    exp = line.split('=')
    key = exp[0].strip()
    value = exp[1].strip()

    if value == "?":
        if key in elements.keys():
            print(elements[key]["value"])
        else:
            print("This variable does not exist.")
    elif value in elements.keys():
        elements[key] = elements[value]
    else:
        if type is None:
            newType = checkType(value)
            if newType == "var":
                value = eval(value)
            else:
                print("type is complex")
            elements[key] = {"type": newType, "value": value}
        elif type == "fn":
            key = key[0:4]
            print(key)
            elements[key] = {"type": type, "value": value}
        print(elements[key]["value"])
    return elements


def main():
    read_flags()
    line = ""
    elements = {}
    # try:
    while line is not None:
        line = read_in()
        if len(line) == 0:
            fn.error("Empty input.")
        else:
            get = re.match(regex.get, line)
            if get:
                key = get.group(1).strip()
                if key in elements.keys():
                    print(elements[key]["value"])
                elif key[0:4] in elements.keys():
                    match = re.match(regex.fnIntParam, key)
                    if match:
                        computeFn(elements[key[0:4]]["value"], match.group(1).strip())
                    else:
                        match = re.match(regex.fnVarParam, key)
                        if match:
                            param = match.group(1).strip()
                            if param in elements.keys():
                                computeFn(elements[key[0:4]]["value"], elements[param]["value"])
                            else:
                                print("The variable " + param + " is not assigned.")
                else:
                    print("This variable is not assigned.")
            elif re.match(regex.checkFunc, line):
                print("assign func")
                elements = assign(line, "fn", elements)
            elif re.match(regex.checkAssign, line):
                elements = assign(line, None, elements)
            else:
                print("Invalid input.")


main()
