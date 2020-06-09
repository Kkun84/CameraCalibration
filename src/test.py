from logging import getLogger
import hydra
import numpy as np
import cv2

import utils


logger = getLogger(__name__)


@hydra.main()
def test(cfg):
    f1 = 2.3
    f2 = 3.4

    A1 = np.array([
        [f1, 0, 0],
        [0, f1, 0],
        [0, 0, 1],
    ])
    A2 = np.array([
        [f2, 0, 0],
        [0, f2, 0],
        [0, 0, 1],
    ])
    E = None

    A1 = np.array([
        [2.3, 0, 0],
        [0, 2.3, 0],
        [0, 0, 1],
    ])
    A2 = np.array([
        [3.4, 0, 0],
        [0, 3.4, 0],
        [0, 0, 1],
    ])
    rot_x = (lambda r: np.array([
        [1, 0, 0],
        [0, np.cos(r), -np.sin(r)],
        [0, np.sin(r), np.cos(r)]]))(0.1)
    rot_y = (lambda r: np.array([
        [np.cos(r), 0, np.sin(r)],
        [0, 1, 0],
        [-np.sin(r), 0, np.cos(r)]]))(0.2)
    rot_z = (lambda r: np.array([
        [np.cos(r), -np.sin(r), 0],
        [np.sin(r), np.cos(r), 0],
        [0, 0, 1]]))(0.1)
    test_R = rot_x @ rot_y @ rot_z
    test_T = np.array([0.5, 0.05, 0.03])
    r1, r2, r3 = test_R.T

    test_E = np.array([np.cross(test_T, r1), np.cross(test_T, r2), np.cross(test_T, r3)]).T
    logger.info(f"{test_E=}")

    test_F = np.dot(np.dot(np.linalg.inv(A1.T), test_E), np.linalg.inv(A2))
    logger.info(f"{test_F=}")

    test_e = utils.solve_epipole(test_F.T)
    logger.info(f"{test_e=}")
    logger.info(f"{test_e @ test_F=}")

    f_list = utils.solve_inside_params(test_F, test_e, *[0]*4, target='f')
    logger.info(f"{f_list=}")
    return


if __name__ == "__main__":
    test()
