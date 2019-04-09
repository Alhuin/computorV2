import sys
import re


def error(message):
    print("\033[0;31m[Error]\033[0m " + message)
    sys.exit()


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

    # replace 6x^2 | 6*x^2  by 6 * X^2

    line = re.sub("([\+\-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*\^\s*(\d+)\s*(?=[\+\-\*=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)

    # replace 6x | 6*x      by 6 * X^1

    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*([\+\*\-=]|$)", r"\1 * X \2", line, flags=re.IGNORECASE)

    # replace ^ by **

    line = re.sub("\^", "**", line)

    # line = re.sub("([\+\-=]|^)\s*X\s*(?=[\+\-=]|$)", r"\1 1 * X^1 ", line, flags=re.IGNORECASE)

    # replace X^5           by 1 * X^5

    # line = re.sub("([\+\-=]|^)\s*X\s*\^\s*(\d+)\s*(?=[\+\-=]|$)", r"\1 1 * X^\2 ", line, flags=re.IGNORECASE)

    # replace 6             by 6 * X^0

    # line = re.sub("(?<![\^\d])\s*(\d+(?:\.\d+)?)\s*(?=[\+\-=]|$)", r" \1 * X^0 ", line, flags=re.IGNORECASE)


    return line
