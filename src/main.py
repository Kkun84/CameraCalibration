from logging import getLogger
import hydra
import numpy as np
import cv2

import utils


logger = getLogger(__name__)


@hydra.main(config_path='../conf/config.yaml')
def main(cfg):
    logger.info('\n' + str(cfg.pretty()))
    # Load
    F = np.array(cfg.F)
    assert F.shape == (3, 3)

    e = utils.solve_epipole(F.T)
    logger.info(f"{e=}")
    logger.info(f"{e @ F=}")
    # center1 = np.array(cfg.images[0].size) // 2
    # center2 = np.array(cfg.images[1].size) // 2
    center1 = cfg.images[0].center
    center2 = cfg.images[1].center
    logger.info(f"{center1=}, {center2=}")

    f_list = utils.solve_inside_params(F, e, *center1, *center2, target='f')
    logger.info(f"{f_list=}")

    f1 = 2400
    f2 = 2400
    c1 = utils.solve_inside_params(F, e, f1, f2, *center2, target='c1')
    logger.info(f"{c1=}")

    c2 = utils.solve_inside_params(F, e, f1, f2, *center2, target='c2')
    logger.info(f"{c2=}")
    return


if __name__ == "__main__":
    main()
