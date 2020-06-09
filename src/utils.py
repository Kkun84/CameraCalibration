from logging import getLogger
import numpy as np
import sympy as sy
import cv2
import matplotlib.pyplot as plt
import matplotlib.colors


logger = getLogger(__name__)


def solve_epipole(F):
    u, s, v = np.linalg.svd(F)
    e = v[s.argmin()]
    return e


def solve_inside_params(F, e, p11, p12, p21, p22, target):
    # a1, a2を求める
    sy.var('a1, a2')

    if target == 'f':
        A1 = sy.Matrix([
            [a1, 0, p11],
            [0, a1, p12],
            [0, 0, 1]],
        )
        A2 = sy.Matrix([
            [a2, 0, p21],
            [0, a2, p22],
            [0, 0, 1]],
        )
    elif target == 'c1':
        A1 = sy.Matrix([
            [p11, 0, a1],
            [0, p11, a2],
            [0, 0, 1]],
        )
        A2 = sy.Matrix([
            [p12, 0, p21],
            [0, p12, p22],
            [0, 0, 1]],
        )
    elif target == 'c2':
        A1 = sy.Matrix([
            [p11, 0, p21],
            [0, p11, p22],
            [0, 0, 1]],
        )
        A2 = sy.Matrix([
            [p12, 0, a1],
            [0, p12, a2],
            [0, 0, 1]],
        )
    else:
        assert False

    sy.var('tau')

    t = sy.Matrix([1, tau, 0])
    logger.debug(f"{t=}")

    e = sy.Matrix(e)
    logger.debug(f"{e=}")

    F = sy.Matrix(F)
    logger.debug(f"{F=}")

    # (e×t)^T*A1 * A1^T*(e1×t) = 0
    eqn1 = (lambda x: sy.expand((x.transpose() * x)[0]))(A1.transpose() * e.cross(t))
    logger.debug(f"{eqn1=}")
    # (F^T*t)^T*A2 * A2^T*(F^T*t) = 0
    eqn2 = (lambda x: sy.expand((x.transpose() * x)[0]))(A2.transpose() * F.transpose() @ t)
    logger.debug(f"{eqn2=}")

    k1 = sy.Matrix([eqn1.coeff(tau, i) for i in range(3)])
    logger.debug(f"{k1=}")
    k2 = sy.Matrix([eqn2.coeff(tau, i) for i in range(3)])
    logger.debug(f"{k2=}")

    # k10*k21 - k11*k20
    expr1 = sy.expand(k1[0]*k2[1] - k1[1]*k2[0])
    logger.debug(f"{expr1=}")
    # k11*k22 - k21*k12
    expr2 = sy.expand(k1[1]*k2[2] - k2[1]*k1[2])
    logger.debug(f"{expr2=}")

    # expr1 = expr2 = 0を解く(解はa1, a2)
    solutions = sy.solve([expr1, expr2], [a1, a2])
    logger.debug(f"{solutions=}")

    return solutions
