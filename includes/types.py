import re
from includes import regex, utils as u
import matplotlib.pyplot as plt
import numpy as np


class Function:

    def __init__(self, function, param):
        self.function = u.formatLine(function)
        self.param = param

    def compute(self, param):
        try:
            res = eval(self.function.replace('X', str(param)))
        except ZeroDivisionError:
            res = u.error("Division by 0.")
        return res

    def draw(self, xMin, xMax):
        X = np.array(range(xMin, xMax))
        y = eval(self.function)
        plt.plot(X, y)
        plt.show()


class Matrice:

    def __init__(self):
        self.array = None
        self.height = 0
        self.width = 0

    def calc(self, operation, obj):
        matrice = self.array
        if obj["type"] == "var":
            var = obj["value"]
            print(var)
            print(operation)
            for i in range(len(matrice)):
                for j in range(len(matrice[i])):
                    # matrice[i][j] = u.intFloatCast(eval(str(matrice[i][j]) + operation + var))
                    if operation == "+":
                        print('+')
                        matrice[i][j] += var
                    elif operation == "*":
                        matrice[i][j] *= var
                    elif operation == "/":
                        matrice[i][j] /= var
                    elif operation == "-":
                        matrice[i][j] -= var
                    else:
                        matrice[i][j] %= var
                    print(matrice[i][j])
        elif obj["type"] == "matrice":
            if obj["value"].height == self.height and obj["value"].width == self.width:
                m = obj["value"].array
                for i in range(len(matrice)):
                    for j in range(len(matrice[i])):
                            if operation == "+":
                                matrice[i][j] += m[i][j]
                            elif operation == "*":
                                matrice[i][j] *= m[i][j]
                            elif operation == "/":
                                matrice[i][j] /= m[i][j]
                            elif operation == "-":
                                matrice[i][j] -= m[i][j]
                            else:
                                matrice[i][j] %= m[i][j]
            else:
                u.out(u.error("Impossible d'effectuer un calcul matriciel avec deux matrices de tailles différentes."))
                return None
        else:
            u.out(u.error("complex or funx ope with matrice"))
            return None
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
