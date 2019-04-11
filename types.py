import utils as u
import re
import regex


class Matrice:

    def __init__(self):
        self.array = None
        self.height = 0
        self.width = 0

    def calc(self, operation, exp, expIsMatrice):
        matrice = self.array
        if not expIsMatrice:
            for line in matrice:
                for elem in line:
                    if operation == "+":
                        elem += exp
                    elif operation == "*":
                        elem *= exp
                    elif operation == "/":
                        elem /= exp
                    elif operation == "-":
                        elem -= exp
                    else:
                        elem %= exp
        return matrice

    def parse(self, exp):
        width = None
        height = 0
        match = re.findall(regex.parseMatrice, exp)
        matrice = [[] for _ in range(len(match))]
        for m in match:
            elems = m.split(',')
            if width is None:
                width = len(elems)
            elif width != len(elems):
                return None
            for e in elems:
                matrice[height].append(u.intFloatCast(e))
            height += 1
        self.height = height
        self.width = width
        self.array = matrice
        return self

    def print(self):
        for m in self.array:
            first = True
            output = '[ '
            for e in m:
                if not first:
                    output += ", "
                output += str(e)
                first = False
            u.out(output + ' ]')
