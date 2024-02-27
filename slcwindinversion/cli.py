"""Console script for slcwindinversion."""
import argparse
import sys
import logging
import time
import numpy as np
from slcwindinversion.mainslcwindinversion import core_inversion


def get_memory_usage():
    try:
        import resource
        memory_used_go = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000. / 1000.
    except KeyboardInterrupt:
        raise
    except:  # on windows resource is not usable
        import psutil
        memory_used_go = psutil.virtual_memory().used / 1000 / 1000 / 1000.
    str_mem = 'RAM usage: %1.1f Go' % memory_used_go
    return str_mem


def main():
    """Console script for slcwindinversion."""
    time.sleep(np.random.rand(1, 1)[0][0])  # to avoid issue with mkdir
    parser = argparse.ArgumentParser(description='L2AwindspeedProduction')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', default=False,
                        help='overwrite the existing outputs [default=False]', required=False)
    parser.add_argument('--inputsafe', required=True, help='Level-1C SAFE product full path to use as input')
    parser.add_argument('--outputdir', required=True, help='directory where to store output netCDF files')
    parser.add_argument('--version',
                        help='set the output product version (e.g. 1.4)',
                        required=True)
    parser.add_argument('--dev', action='store_true', default=False, help='dev mode stops the computation early')
    args = parser.parse_args()
    fmt = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s'
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=fmt,
                            datefmt='%d/%m/%Y %H:%M:%S', force=True)
    else:
        logging.basicConfig(level=logging.INFO, format=fmt,
                            datefmt='%d/%m/%Y %H:%M:%S', force=True)
    t0 = time.time()
    # generate_L2A_windspeed_product(input_directory=args.inputsafe, output_directory=args.outputdir)
    core_inversion(input_folder=args.inputsafe,outd=args.outputdir,overwrite=args.overwrite,version=args.version)
    logging.info('peak memory usage: %s', get_memory_usage())
    logging.info('done in %1.3f min', (time.time() - t0) / 60.)
    return 0


if __name__ == "__main__":
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    sys.exit(main())  # pragma: no cover
