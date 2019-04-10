import sys
import re


def error(message):
    return "\033[0;31m[Error]\033[0m " + message
    # sys.exit()


def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def strIntFloat(param):
    string = str(param)
    strLen = len(string)
    if strLen > 2 and string[strLen - 2:strLen] == ".0":
        return string[:strLen - 2]
    else:
        return string


#   prints irreducitible fraction if necessary

def pol_printSolution(solution, den, div):
    solution = -solution if solution == -0 else solution
    frac = ""
    res = strIntFloat(solution)
    if '.' in res and '.' not in strIntFloat(den) and '.' not in strIntFloat(div):
        cd = pgcd(den, div)
        frac = strIntFloat(den / cd) + "/" + strIntFloat(div / cd)
    if frac != "":
        res += "   (" + frac + ")"
    print(res)


#   Handles natural input

def pol_formatLine(line):


    line = re.sub("([\+\-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*\^\s*(\d+)\s*(?=[\+\-\%\*=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)


    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*([\+\%\*\-=]|$)", r"\1 * X \2", line, flags=re.IGNORECASE)

    line = re.sub("\^", "**", line)



    return line
