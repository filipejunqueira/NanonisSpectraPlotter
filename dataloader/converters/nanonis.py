from nanonispy.read import Grid

from dataloader.common import add_to_data_dict

IMAGE_FILE_FORMATS = ["sxm"]
SPECTRA_FILE_FORMATS = ["dat", "3ds"]
ALL_FORMATS = [IMAGE_FILE_FORMATS + SPECTRA_FILE_FORMATS]


def add_3ds(fname, resource_data_dict):
    data = Grid(fname)

    mapping = {"data_type": "spectra",
               "experiment_name": data.fname,
               "time_start": data.header["start_time"],
               "time_end": data.header["end_time"],
               "comment": data.header["comment"],

               "main_pos_xy": data.header["pos_xy"],
               "size_xy": data.header["size_xy"],
               "image_points_res": data.header["dim_px"],
               "spectra_res": data.header["num_sweep_signal"],
               "spectra_x_channels": data.header["sweep_signal"],
               "spectra_y_channels": data.header["channels"],
               "img_channels": data.header["fixed_parameters"] + data.header["experimental_parameters"],
               "spectra_x": data.signals["sweep_signal"].tolist(),
               "spectra_y": {channel: data.signals[channel].tolist() for channel in data.header["channels"]},
               "img": {"topo": data.signals["topo"].tolist(),
                       **{channel: data.signals["params"][..., i].tolist() for i, channel in enumerate(
                           data.header["fixed_parameters"] + data.header["experimental_parameters"])}
                       }
               }

    resource_data_dict = add_to_data_dict(resource_data_dict, mapping)

    return resource_data_dict


def add_dat(fname, spectra_data_dict):
    pass


def add_sxm(fname, image_data_dict):
    pass
