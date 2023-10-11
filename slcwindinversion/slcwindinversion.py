"""Main module."""
import numpy as np
import xarray as xr
import glob
import os
from xsarsea import windspeed
from scipy.ndimage import binary_dilation
import logging


def get_vv_vh(folder, subswath_number):
    """

    :param folder: str SAFE L1C or L1B products
    :param subswath_number: int 1 2 or 3
    :return:
    """
    vvs = glob.glob(os.path.join(folder, "*" + os.path.basename(folder)[0:6].lower().replace("_", "-") + str(
        subswath_number) + "-slc-vv-*.nc"))
    vhs = glob.glob(os.path.join(folder, "*" + os.path.basename(folder)[0:6].lower().replace("_", "-") + str(
        subswath_number) + "-slc-vh-*.nc"))
    if (len(vvs) != 1) | (len(vhs) != 1):
        return []
    else:
        return vvs[0], vhs[0]


def core_inversion(folder, outd, overwrite=False):
    """
    args:
        folder: str input L1C or L1B SAFE full path containing .nc files with sigma0,incidence,ground_heading,nesz variables
        outd: str: output directory where to store the L2A WSP .nc files
        overwrite: bool
    """

    out_folder = os.path.join(outd, os.path.basename(folder))
    out_folder = out_folder.replace('XSP', 'WPS')
    logging.info(out_folder)
    os.makedirs(out_folder, exist_ok=True)
    if '1SDV' in folder or '1SDH' in folder:

        test_all_measu = len(glob.glob(out_folder + "/*.nc")) == 6
    else:
        test_all_measu = len(glob.glob(out_folder + "/*.nc")) == 3
    if os.path.exists(folder) and test_all_measu and overwrite is False:
        logging.info("out_folder %s exists" % out_folder)
        return out_folder

    subswath_numbers = [1, 2, 3]  # for IW
    for subswath_number in subswath_numbers:
        logging.info("subswath_number %d" % subswath_number)
        try:
            path_vv, path_vh = get_vv_vh(folder, subswath_number)
        except Exception as e:
            return None

        for burst_type in ["intra", "inter"]:
            logging.info("burst %s" % burst_type)

            """
            vv_ds = xr.open_dataset(path_vv,group=burst_type+'burst')
            vh_ds = xr.open_dataset(path_vh,group=burst_type+'burst')

            ancillary_wind = (vv_ds.U10 + 1j * vv_ds.V10) * np.exp(1j * np.deg2rad(vv_ds.ground_heading))
            dsig_cr = windspeed.get_dsig("gmf_s1_v2",vv_ds.incidence,vh_ds.sigma0,vh_ds.nesz)
            """
            vv_ds = xr.open_dataset(path_vv, group=burst_type + 'burst')
            vh_ds = xr.open_dataset(path_vh, group=burst_type + 'burst')

            mask_flag = binary_dilation(vv_ds.land_flag.values.astype('uint8'),
                                        structure=np.ones((3, 3, 3), np.uint8), iterations=3)
            ancillary_wind = (vv_ds.U10 + 1j * vv_ds.V10) * np.exp(1j * np.deg2rad(vv_ds.ground_heading))
            ancillary_wind = xr.where(mask_flag, np.nan, ancillary_wind.compute()).transpose(*ancillary_wind.dims)

            dsig_cr = windspeed.get_dsig("gmf_s1_v2", vv_ds.incidence, vh_ds.sigma0, vh_ds.nesz)

            sigma_0_vv = xr.where(mask_flag, np.nan, vv_ds.sigma0.compute()).transpose(*vv_ds.sigma0.dims)
            sigma_0_vh = xr.where(mask_flag, np.nan, vh_ds.sigma0.compute()).transpose(*vh_ds.sigma0.dims)

            dsig_cr = windspeed.get_dsig("gmf_s1_v2", vv_ds.incidence, sigma_0_vh, vh_ds.nesz)

            # co & dual inversion
            wind_speed_co, wind_speed_dual = windspeed.invert_from_model(
                vv_ds.incidence,
                sigma_0_vv,
                sigma_0_vh,
                # ancillary_wind=-np.conj(xsar_obj_1000m.dataset['ancillary_wind']),
                ancillary_wind=-ancillary_wind,
                dsig_cr=dsig_cr,
                model=("cmod5n", "gmf_s1_v2"))
            wind_speed_co = np.abs(wind_speed_co)
            wind_speed_dual = np.abs(wind_speed_dual)

            wind_speed_cr = windspeed.invert_from_model(
                vv_ds.incidence.values,
                sigma_0_vh.values,
                # ancillary_wind=-np.conj(xsar_obj_1000m.dataset['ancillary_wind']),
                dsig_cr=dsig_cr.values,
                model="gmf_s1_v2")

            wind_speed_cr = np.abs(wind_speed_cr)

            out_ds = xr.Dataset()
            out_ds.attrs = vv_ds.attrs
            out_ds.attrs['product'] = 'WSP'
            out_ds["wind_speed_co"] = wind_speed_co
            out_ds["wind_speed_dual"] = wind_speed_dual
            out_ds["wind_speed_co"].attrs["comment"] = out_ds["wind_speed_co"].attrs["comment"].replace(
                "wind speed and direction", "wind speed")
            out_ds["wind_speed_dual"].attrs["comment"] = out_ds["wind_speed_dual"].attrs["comment"].replace(
                "wind speed and direction", "wind speed")

            out_ds = out_ds.assign(wind_speed_cr=(['burst', 'line', 'sample'], wind_speed_cr))
            out_ds.wind_speed_cr.attrs['comment'] = "wind speed inverted from model %s (%s)" % ("gmf_s1_v2", "VH")
            out_ds.wind_speed_cr.attrs['model'] = "gmf_s1_v2"
            out_ds.wind_speed_cr.attrs['units'] = 'm/s'

            #             vh_ds["wind_speed_co"] = wind_speed_co
            #             vh_ds["wind_speed_dual"] = wind_speed_dual
            #             vh_ds["wind_speed_co"].attrs["comment"] = vh_ds["wind_speed_co"].attrs["comment"].replace("wind speed and direction","wind speed")
            #             vh_ds["wind_speed_dual"].attrs["comment"] = vh_ds["wind_speed_dual"].attrs["comment"].replace("wind speed and direction","wind speed")

            #             vh_ds=vh_ds.assign(wind_speed_cr=(['burst','line','sample'],wind_speed_cr))
            #             vh_ds.wind_speed_cr.attrs['comment'] = "wind speed inverted from model %s (%s)" % ("gmf_s1_v2", "VH")
            #             vh_ds.wind_speed_cr.attrs['model'] = "gmf_s1_v2"
            #             vh_ds.wind_speed_cr.attrs['units'] = 'm/s'

            path_final = os.path.basename(path_vv).replace('-vv-', '-dualpol-')
            # SAVE
            out_ds.to_netcdf(os.path.join(out_folder, path_final), group=burst_type + 'burst', mode='a')
            # vh_ds.to_netcdf(os.path.join(out_folder,os.path.basename(path_vh)),group=burst_type+'burst',mode='a')

            out_ds.close()
            # vh_ds.close()
    return out_folder


def generate_L2A_windspeed_product(input_directory, output_directory):
    folders = glob.glob(os.path.join(input_directory, "*SAFE"))
    for folder in folders:
        core_inversion(folder, output_directory, overwrite=True)
