import os
import datetime
import copy
import logging
def get_l2_filepath(l1c_fullpath, version, outputdir)->str:
    """

    Args:
        l1c_fullpath: str .nc l1b full path
        version : str (eg. 1.2 or B01)
        outputdir: str
    Returns:
        l2_full_path: str
    """
    safe_file = os.path.basename(os.path.dirname(l1c_fullpath))
    if outputdir is None:
        run_directory = os.path.dirname(os.path.dirname(l1c_fullpath))
        # Output file directory
        pathout_root = run_directory.replace("l1c", "l2")
    else:
        pathout_root = outputdir

    safe_start_date = datetime.datetime.strptime(safe_file.split('_')[5],'%Y%m%dT%H%M%S')
    pathout = os.path.join(pathout_root, safe_start_date.strftime('%Y'),safe_start_date.strftime('%j'), safe_file)

    # Output filename
    l2_full_path = os.path.join(
        pathout, os.path.basename(l1c_fullpath)).replace("L1C", "L2").replace('XSP','WSP')
    # add the product ID in the SAFE  name
    basesafe = os.path.basename(os.path.dirname(l2_full_path))
    basesafe0 = copy.copy(basesafe)
    if (
        len(basesafe.split("_")) == 10
    ):  # classical ESA SLC naming #:TODO once xsarslc will be updated this case could be removed
        basesafe = basesafe.replace(".SAFE", "_" + version.upper() + ".SAFE")
    else:  # there is already a product ID in the L1B SAFE name
        lastpart = basesafe.split("_")[-1]
        basesafe = basesafe.replace(lastpart, version.upper() + ".SAFE")
    l2_full_path = l2_full_path.replace(basesafe0, basesafe)

    lastpiece = l2_full_path.split("_")[-1]

    l2_full_path = l2_full_path.replace(lastpiece, version + ".nc")

    logging.debug("File out: %s ", l2_full_path)
    if not os.path.exists(os.path.dirname(l2_full_path)):
        os.makedirs(os.path.dirname(l2_full_path), 0o0775)
    return l2_full_path
