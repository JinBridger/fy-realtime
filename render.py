"""Render image from L1 data"""

import cv2
import h5py
import numpy as np

class Render:
    """Render image from L1 data"""

    @staticmethod
    def render(l1_path: str, output_path: str):
        """Render image from L1 data"""
        print("START RENDER IMAGE...")
        hdf_data = h5py.File(l1_path, "r")
        original_c01_data = hdf_data['Data']["NOMChannel01"][:]
        original_c02_data = hdf_data['Data']["NOMChannel02"][:]
        original_c03_data = hdf_data['Data']["NOMChannel03"][:]

        c01_data = (original_c01_data / 4095).astype(np.float32)
        c02_data = (original_c02_data / 4095).astype(np.float32)
        c03_data = (original_c03_data / 4095).astype(np.float32)

        # set background to black
        c01_data[c01_data >= 1] = 0
        c02_data[c02_data >= 1] = 0
        c03_data[c03_data >= 1] = 0

        # from SegerYU@Bilibili
        r_data = 1.16 * c02_data - 0.16 * c03_data
        g_data = 0.6 * c01_data + 0.33 * c02_data + 0.07 * c03_data
        b_data = c01_data

        r_data = (r_data * 255).astype(np.uint8)
        g_data = (g_data * 255).astype(np.uint8)
        b_data = (b_data * 255).astype(np.uint8)

        img = cv2.merge([b_data, g_data, r_data]) # pylint: disable=no-member
        cv2.imwrite(output_path, img) # pylint: disable=no-member
