from includes import utils as u
import re


def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def str_int_float(param):
    string = str(param)
    str_len = len(string)
    if str_len > 2 and string[str_len - 2:str_len] == ".0":
        return string[:str_len - 2]
    else:
        return string


#   prints irreducitible fraction if necessary

def print_solution(solution, den, div):
    solution = -solution if solution == -0 or solution == -0.0 else solution
    frac = ""
    res = str_int_float(solution)
    if res == "-0":
        res = "0"
    if '.' in res and '.' not in str_int_float(den) and '.' not in str_int_float(div):
        cd = pgcd(den, div)
        frac = str_int_float(den / cd) + "/" + str_int_float(div / cd)
    if frac != "":
        res += "   (" + frac + ")"
    u.out(res)


#   Handles natural input

def format_line(line):

    # replace 6^2 | 6*2 | 6/2 by the result

    match = True
    while match:
        match = re.search(r"(?:[+-=]|^)\s*((\d+(?:\.\d+)?)\s*[\^*/]\s*(\d+(?:\.\d+)?))\s*(?=[+-=]|$)",
                          line, flags=re.IGNORECASE)
        if match:
            exp = match.group(1).replace('^', '**')
            res = eval(exp)
            line = line.replace(match.group(1), str(res))
    print(line)

    # replace 6x^2 | 6*x^2  by 6 * X^2

    line = re.sub(r"([+-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*X\s*\^\s*(\d+)\s*(?=[+-=]|$)",
                  r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)

    # replace 6x | 6*x      by 6 * X^1

    line = re.sub(r"(\d+(?:\.\d+)?)\s*\*?\s*X\s*([+-=]|$)", r"\1 * X^1 \2", line, flags=re.IGNORECASE)

    # replace X             by 1 * X^1

    line = re.sub(r"([+-=]|^)\s*X\s*(?=[+-=]|$)", r"\1 1 * X^1 ", line, flags=re.IGNORECASE)

    # replace X^5           by 1 * X^5

    line = re.sub(r"([+-=]|^)\s*X\s*\^\s*(\d+)\s*(?=[+-=]|$)", r"\1 1 * X^\2 ", line, flags=re.IGNORECASE)

    # replace 6             by 6 * X^0

    line = re.sub(r"(?<![\^\d])\s*(\d+(?:\.\d+)?)\s*(?=[+-=]|$)", r" \1 * X^0 ", line, flags=re.IGNORECASE)

    return line
