import re
from includes import cpv1_functions as fn, utils as u

regex_pattern = re.compile(r"(-?\s*\d+(?:\.\d+)?)\s*\*\s*X\^(\d+)")
details = True


def compute(line, elements, side):
    if details:
        print("\n\033[0;32m[details]\033[0m natural parsing : " + line + "\n")
    line_split = line.split('=')
    reduced = "Reduced form: "
    detail_string = "\n\033[0;32m[details]\033[0m Simplified form : "
    res = 0
    first = True
    detail_first = True
    degree = 0
    count = 0

    while side < 2:
        exp = re.findall(regex_pattern, line_split[side])
        for i in range(len(exp)):
            pwr = int(exp[i][1].replace(' ', ''))
            num = float(exp[i][0].replace(' ', ''))
            try:
                if elements[pwr] is None:
                    elements[pwr] = 0
                elements[pwr] += num if side == 0 else -num
            except KeyError:
                elements[pwr] = num if side == 0 else -num
        side += 1

    for key, value in elements.items():
        if value is not None:
            if value == 0:
                count += 1
            else:
                if key > degree:
                    degree = key

            if first:
                reduced += fn.str_int_float(value) + " * X^" + str(key)
                first = False
            else:
                reduced += (" + " + fn.str_int_float(value) if value >= 0 else " - " + fn.str_int_float(-value)) \
                           + " * X^" + str(key)
            if detail_first:
                value_str = fn.str_int_float(value)
                if key != 0:
                    detail_first = False
            else:
                value_str = (" + " + fn.str_int_float(value) if value >= 0 else " - " + fn.str_int_float(-value))

            if key == 0:
                res -= value
            if key == 1:
                detail_string += value_str + "X"
            if key > 1:
                detail_string += value_str + "X^" + str(key)
        else:
            count += 1
            elements[key] = 0

    if degree == 0:
        if elements[0] == 0:
            print(reduced + " = 0")
            print("This equation accepts all real numbers as solution.")
        else:
            u.warn("Invalid input.", "SyntaxError")
    elif count == len(elements):
        print(reduced + " = 0")
        print("This equation accepts all real numbers as solution.")
    else:
        print(reduced + " = 0")
        print("Polynomial degree: " + str(degree))
        if degree < 3 and details:
            print(detail_string + " = " + fn.str_int_float(res))

        if degree <= 2:
            b = elements[1]
            c = elements[0]
            if degree == 1:
                if b == 0:
                    u.warn("Division by 0.", "ComputeError")
                else:
                    x = -c / b
                    if details:
                        print("\033[0;32m[details]\033[0m X = " + fn.str_int_float(-c)
                              + "/" + fn.str_int_float(b) + "\n")
                    print("The solution is:")
                    fn.print_solution(x, -c, b)

            elif degree == 2:
                a = elements[2]
                delta = b * b - 4 * a * c
                if details:
                    print("\033[0;32m[details]\033[0m Calculating discriminant : " + fn.str_int_float(b) + "^2 - 4 * "
                          + fn.str_int_float(a)+" * "+fn.str_int_float(c) + " = " + fn.str_int_float(delta)+"\n")
                if delta > 0:
                    x1 = (-b - delta ** 0.5) / (2 * a)
                    x2 = (-b + delta ** 0.5) / (2 * a)
                    print("Discriminant is strictly positive, the two solutions are:")
                    if details:
                        print("\n\033[0;32m[details]\033[0m Calculating solution 1 : ("+fn.str_int_float(-b)+" - "
                              + fn.str_int_float(delta)+"^0.5) / "+fn.str_int_float(2 * a))
                        print("\033[0;32m[details]\033[0m Calculating solution 2 : ("+fn.str_int_float(-b)+" + "
                              + fn.str_int_float(delta) + "^0.5) / "+fn.str_int_float(2 * a)+"\n")
                    fn.print_solution(x1, (-b - delta ** 0.5), (2 * a))
                    fn.print_solution(x2, (-b + delta ** 0.5), (2 * a))

                elif delta < 0:
                    print("The discriminant is strictly negative, the equation has no real solution,"
                          + "only 2 complex solutions:")
                    print("("+fn.str_int_float(-b)+" − i√"+fn.str_int_float(-delta)+") / "+fn.str_int_float(2 * a))
                    print("("+fn.str_int_float(-b)+" + i√"+fn.str_int_float(-delta)+") / "+fn.str_int_float(2 * a))

                else:
                    if a == 0:
                        u.warn("Division by 0.", "ComputeError")
                    x = -b / (2 * a)
                    print("The discriminant is 0, the equation has one solution:")
                    if details:
                        print("\033[0;32m\n[details]\033[0m Calculating solution : " + fn.str_int_float(-b)
                              + "/" + fn.str_int_float(2 * a)+"\n")
                    fn.print_solution(x, -b, c)
        else:
            u.warn("The polynomial degree is strictly greater than 2, I can't solve.", "ComputeError")
    return True


def try_polynomial(line):
    elements = {0: None, 1: None, 2: None}
    try:
        compute(fn.format_line(line), elements, 0)
    except Exception:
        u.warn("Invalid input.", "SyntaxError")
