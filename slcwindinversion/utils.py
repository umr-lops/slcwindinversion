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
    pathout_root = outputdir

    safe_start_date = datetime.datetime.strptime(safe_file.split('_')[5],'%Y%m%dT%H%M%S')
    pathout = os.path.join(pathout_root, safe_start_date.strftime('%Y'),safe_start_date.strftime('%j'))

    # SAFE part
    safe_file = safe_file.replace("L1C", "L2").replace('XSP', 'WSP')
    if (
        len(safe_file.split("_")) == 10
    ):  # classical ESA SLC naming #:TODO once xsarslc will be updated this case could be removed
        safe_file = safe_file.replace(".SAFE", "_" + version.upper() + ".SAFE")
    else:  # there is already a product ID in the L1B SAFE name
        lastpart = safe_file.split("_")[-1]
        safe_file = safe_file.replace(lastpart, version.upper() + ".SAFE")

    # measurement part
    base_measu = os.path.basename(l1c_fullpath)
    lastpiece = base_measu.split("-")[-1]

    base_measu = base_measu.replace(lastpiece, version.lower() + ".nc")
    if base_measu[0:3]=='l1c':
        base_measu = base_measu.replace('l1c-','l2-')
    else:
        base_measu = 'l2-'+base_measu
    base_measu = base_measu.replace('-xsp-','-wsp-')

    l2_full_path = os.path.join(pathout, safe_file,base_measu)
    logging.debug("File out: %s ", l2_full_path)
    if not os.path.exists(os.path.dirname(l2_full_path)):
        os.makedirs(os.path.dirname(l2_full_path), 0o0775)
    return l2_full_path
