""" Advent of Code 2023, Day 24
    Day 24: Never Tell Me The Odds
    Author: Chi-Kit Pao
    REMARK: Requires numpy and sympy to run this program.
"""

import copy
import itertools
import numpy as np
import os
import sympy as sp
import time


def debug(*args):
    if False:
        print(*args)


class Hailstone:
    def __init__(self, id_, pos, v):
        self.id = id_
        self.pos = pos
        self.v = v

    def __repr__(self):
        return f"Hailstone(id={self.id}, pos={self.pos}, v={self.v})"

    def __str__(self):
        return self.__repr__()


def parse_line(id_, line):
    # Example input
    # 230027994633462, 224850233272831, 164872865225455 @ 103, -57, 285
    p1, p2 = line.split(" @ ")
    pos = tuple([int(s) for s in p1.split(", ")])
    v = tuple([int(s) for s in p2.split(", ")])
    return Hailstone(id_, pos, v)


def part1(hailstones):
    total = 0
    for c in itertools.combinations(hailstones, 2):
        a = np.array([[c[0].v[0], -c[1].v[0]], [c[0].v[1], -c[1].v[1]]])
        b = np.array([c[1].pos[0] - c[0].pos[0], c[1].pos[1] - c[0].pos[1]])

        try:
            x = np.linalg.solve(a, b)
        except np.linalg.LinAlgError:
            # REMARK: Even though these velocity vectors are (anti-)parallel when projected to x-y-plane, they are skew lines
            # in 3D space.

            # Output:
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=13, pos=(416343629775116, 253022765045891, 491717629266329),
            #  v=(-92, 115, -118)) and Hailstone(id=290, pos=(365714742138785, 305827058151326, 537426018413809), v=(-44, 55, -176))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=27, pos=(406438277711560, 365452366481665, 303153811346747),
            #  v=(-99, -24, 66)) and Hailstone(id=218, pos=(344141964435022, 343951825236361, 384186561046085), v=(-33, -8, -33))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=29, pos=(310857408788602, 297796477288243, 210531244259195),
            #  v=(-31, -31, 163)) and Hailstone(id=260, pos=(298167626012347, 343890784063423, 423675682350779), v=(34, 34, -34))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=29, pos=(310857408788602, 297796477288243, 210531244259195),
            #  v=(-31, -31, 163)) and Hailstone(id=275, pos=(232442233530894, 174047813539401, 130419194940021), v=(95, 95, 411))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=67, pos=(280473885806842, 315439639491991, 204057564976545),
            #  v=(-57, -342, 160)) and Hailstone(id=150, pos=(321267288021646, 422961112834243, 399808899121358), v=(-29, -174, -103))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=166, pos=(297645490835688, 299741689345597, 267078364272051),
            #  v=(-22, -66, 57)) and Hailstone(id=287, pos=(298704283508254, 298263525225865, 296679721125221), v=(-8, -24, 27))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=255, pos=(277029989037226, 115116345756124, 187440572334869),
            #  v=(-89, 309, 220)) and Hailstone(id=269, pos=(218075316045983, 275317801447459, 264760038336981), v=(178, -618, -228))
            # numpy.linalg.LinAlgError for hailstones Hailstone(id=260, pos=(298167626012347, 343890784063423, 423675682350779),
            #  v=(34, 34, -34)) and Hailstone(id=275, pos=(232442233530894, 174047813539401, 130419194940021), v=(95, 95, 411))
            # debug(f"numpy.linalg.LinAlgError for hailstones {c[0]} and {c[1]}")
            continue

        if x[0] < 0 or x[1] < 0:
            continue
        intersection_x = c[0].pos[0] + x[0] * c[0].v[0]
        intersection_y = c[0].pos[1] + x[0] * c[0].v[1]
        if 200000000000000 <= intersection_x <= 400000000000000:
            if 200000000000000 <= intersection_y <= 400000000000000:
                total += 1
    return total


def part2(hailstones):
    # The impact of our rock with hailstone 0 are described with the following equations.
    #  rrx + t0 * vrx = r0x + t0 * v0x
    #  rry + t0 * vry = r0y + t0 * v0y
    #  rrz + t0 * vrz = r0z + t0 * v0z
    # Or:
    #  (I)   rrx - r0x = t0 * (v0x - vrx)
    #  (II)  rry - r0y = t0 * (v0y - vry)
    #  (III) rrz - r0z = t0 * (v0z - vrz)
    # 
    # Isolate t0 from the remaining equations, then we'll get:
    #  (IV) t0 = (rrx - r0x) / (v0x - vrx)
    #  (V)  t0 = (rry - r0y) / (v0y - vry)
    #  (VI) t0 = (rrz - r0z) / (v0z - vrz)
    # 
    # Substitute V into I, VI into II and IV into III, then we'll get:
    #  (VII)  (rrx - r0x)(v0y - vry) = (v0x - vrx)(rry - r0y)
    #  (VIII) (rry - r0y)(v0z - vrz) = (v0y - vry)(rrz - r0z)
    #  (IX)   (rrz - r0z)(v0x - vrx) = (v0z - vrz)(rrx - r0x)
    # 
    # When we extract the terms in VII, then we'll get:
    #  (X) rrx * v0y - rrx * vry - r0x * v0y + r0x * vry = v0x * rry - v0x * r0y - vrx * rry + vrx * r0y
    #
    # In order to get rid non-linear terms (rrx * vry) and (vrx * rry), we'll do the same for hailstone 1:
    #  (XI) rrx * v1y - rrx * vry - r1x * v1y + r1x * vry = v1x * rry - v1x * r1y - vrx * rry + vrx * r1y
    #
    # Subtract X from XI, then we'll get:
    #  rrx * (v1y - v0y) - r1x * v1y + r0x * v0y + vry * (r1x - r0x) = rry * (v1x - v0x) - v1x * r1y + v0x * r0y + vrx * (r1y - r0y)
    # Or:
    #  rrx * (v1y - v0y) - vrx * (r1y - r0y) - rry * (v1x - v0x) + vry * (r1x - r0x) = -v1x * r1y + v0x * r0y + r1x * v1y - r0x * v0y
    #
    # We will get 6 similar equations (3 pairs * 2 equations) together when combining other coordinates with totally 3 hailstones.

    r0 = hailstones[0].pos
    r1 = hailstones[1].pos
    r2 = hailstones[2].pos
    v0 = hailstones[0].v
    v1 = hailstones[1].v
    v2 = hailstones[2].v

    syr0 = sp.symbols("r0x r0y r0z")
    syr1 = sp.symbols("r1x r1y r1z")
    syr2 = sp.symbols("r2x r2y r2z")
    syrr = sp.symbols("rrx rry rrz")
    syv0 = sp.symbols("v0x v0y v0z")
    syv1 = sp.symbols("v1x v1y v1z")
    syv2 = sp.symbols("v2x v2y v2z")
    syvr = sp.symbols("vrx vry vrz")

    expr1 = sp.sympify("(rrx - r0x) * (v0y - vry) - (v0x - vrx) * (rry - r0y)")
    expr2 = sp.sympify("(rry - r0y) * (v0z - vrz) - (v0y - vry) * (rrz - r0z)")
    expr3 = sp.sympify("(rrz - r0z) * (v0x - vrx) - (v0z - vrz) * (rrx - r0x)")
    expressions = []
    expressions = [expr1, expr2, expr3]

    def replace_symbols(expr, replacement_table):
        result_expr = expr
        for sy in expr.free_symbols:
            for sub_table in replacement_table:
                if sy in sub_table[0]:
                    result_expr = result_expr.subs(sy, sub_table[1][sub_table[0].index(sy)])
                    break
        return result_expr

    def replace_values(expr):
        result_expr = expr
        for sy in expr.free_symbols:
            if sy in syr0:
                result_expr = result_expr.subs(sy, r0[syr0.index(sy)])
            elif sy in syr1:
                result_expr = result_expr.subs(sy, r1[syr1.index(sy)])
            elif sy in syr2:
                result_expr = result_expr.subs(sy, r2[syr2.index(sy)])
            elif sy in syv0:
                result_expr = result_expr.subs(sy, v0[syv0.index(sy)])
            elif sy in syv1:
                result_expr = result_expr.subs(sy, v1[syv1.index(sy)])
            elif sy in syv2:
                result_expr = result_expr.subs(sy, v2[syv2.index(sy)])
        return result_expr
    
    replacements = [[(syr0, syr1), (syv0, syv1)], [(syr0, syr2), (syv0, syv2)]]
    for i in range(6):
        new_expr = copy.deepcopy(expressions[i % 3])
        new_expr = replace_symbols(new_expr, replacements[i // 3])
        expressions.append(new_expr)
    for i in range(len(expressions)):
        expressions[i] = replace_values(expressions[i]).expand()

    expressions2 = [-expressions[0] + expressions[3], -expressions[1] + expressions[4], 
                    -expressions[2] + expressions[5], -expressions[6] + expressions[3], 
                    -expressions[7] + expressions[4], -expressions[8] + expressions[5]]
    matrix = []
    for expr in expressions2:
        symbols = [syrr[0], syvr[0], syrr[1], syvr[1], syrr[2], syvr[2]]
        coefficients = []
        for sy in symbols:
            coefficients.append(sp.collect(expr, sy).coeff(sy, 1))
        
        co_number = expr
        for sy in symbols:
            co_number = sp.collect(co_number, sy).coeff(sy, 0)
        coefficients.append(-co_number)
        matrix.append(tuple(coefficients))
    system = sp.Matrix(tuple(matrix))
    solution = sp.solve_linear_system(system, syrr[0], syvr[0], syrr[1], syvr[1], syrr[2], syvr[2])
    # Output: {rrx: 231279746486542, vrx: 99, rry: 131907658181641, vry: 240, rrz: 195227847662645, vrz: 188}
    debug(solution)
    return solution[syrr[0]] + solution[syrr[1]] + solution[syrr[2]]


def main():
    start_time = time.time()

    hailstones = []

    with open(os.path.join(os.path.dirname(__file__), "input.txt"), "r") as f:
        lines = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    for i, line in enumerate(lines, 1):
        hailstones.append(parse_line(i, line))

    result1 = part1(hailstones)
    print(
        "Question 1: Considering only the X and Y axes, check all pairs of\n"
        " hailstones' future paths for intersections. How many of these\n"
        " intersections occur within the test area?"
    )
    print(f"Answer: {result1}")

    result2 = part2(hailstones)
    print(
        "Question 2: Determine the exact position and velocity the rock needs\n"
        " to have at time 0 so that it perfectly collides with every\n"
        " hailstone. What do you get if you add up the X, Y, and Z coordinates\n"
        " of that initial position?"
    )
    print(f"Answer: {result2}")
    print(f"Time elapsed: {time.time() - start_time} s")


if __name__ == "__main__":
    main()

# Question 1: Considering only the X and Y axes, check all pairs of
#  hailstones' future paths for intersections. How many of these
#  intersections occur within the test area?
# Answer: 20361
# Question 2: Determine the exact position and velocity the rock needs
#  to have at time 0 so that it perfectly collides with every
#  hailstone. What do you get if you add up the X, Y, and Z coordinates
#  of that initial position?
# Answer: 558415252330828
# Time elapsed: 0.6540143489837646 s

