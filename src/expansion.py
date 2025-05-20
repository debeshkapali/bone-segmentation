# Task 1.2 - Expand segmented mask by 2mm
import os
import sys
import numpy as np
import nibabel as nib
from scipy.ndimage import binary_dilation, generate_binary_structure, zoom
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.io_utils import save_nifti


def get_voxel_radius(expand_mm, spacing):
    """
    Convert expansion in mm to voxel units per axis.
    """
    voxel_radius = [int(np.ceil(expand_mm / s)) for s in spacing]
    return voxel_radius


def create_ellipsoid_kernel(radius):
    """
    Create a 3D ellipsoidal kernel for dilation based on the voxel radius.
    """
    zz, yy, xx = np.ogrid[
        -radius[0]:radius[0] + 1,
        -radius[1]:radius[1] + 1,
        -radius[2]:radius[2] + 1
    ]
    mask = ((zz / radius[0]) ** 2 +
            (yy / radius[1]) ** 2 +
            (xx / radius[2]) ** 2) <= 1.0
    return mask


def expand_mask(mask, spacing, expand_mm=4.0):
    """
    Expand the mask using morphological dilation with a 3D ellipsoidal structuring element.
    """
    voxel_radius = get_voxel_radius(expand_mm, spacing)
    kernel = create_ellipsoid_kernel(voxel_radius)
    expanded = binary_dilation(mask, structure=kernel).astype(np.uint8)
    return expanded


def main():
    input_mask_path = "results\original_mask.nii.gz"
    #output_mask_path = "masks/mask_femur_tibia_expanded_2mm.nii.gz"
    output_mask_path = "results/mask_femur_tibia_expanded_4mm.nii.gz"
    expand_mm = 4.0

    # Load original mask
    mask_nii = nib.load(input_mask_path)
    mask_data = mask_nii.get_fdata().astype(np.uint8)
    spacing = mask_nii.header.get_zooms()

    # Expand the mask
    expanded_mask = expand_mask(mask_data, spacing, expand_mm)

    # Save using your save_nifti (which needs affine & header)
    save_nifti(expanded_mask, mask_nii.affine, mask_nii.header, output_mask_path)


if __name__ == "__main__":
    main()
