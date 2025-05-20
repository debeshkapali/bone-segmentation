import os
import sys
import numpy as np
import nibabel as nib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.io_utils import load_nifti, save_nifti
from utils.viz_utils import show_overlay_scroll
from utils.viz_utils import show_side_by_side_masks
from randomization import generate_randomized_mask

# --- Paths ---
volume_path = "data\left_knee.nii"            # CT volume
original_mask_path = "results\original_mask.nii.gz"  # Original mask (Task 1.1 output)
output_mask_path = "results/randomized_mask_2.nii.gz"       # Save randomized mask

# --- Load CT and original mask ---
volume, affine, header = load_nifti(volume_path)
original_mask, _, _ = load_nifti(original_mask_path)

# --- Generate randomized mask ---
voxel_spacing = header.get_zooms()[:3]  # (z, y, x)
randomized_mask = generate_randomized_mask(original_mask, max_distance_mm=2.0, voxel_spacing=voxel_spacing, seed=123)

# --- Save result ---
save_nifti(randomized_mask, affine, header, output_mask_path)

# --- Visualize overlay ---
show_overlay_scroll(volume, randomized_mask, start_slice=90, end_slice=130)

show_side_by_side_masks(volume, original_mask, randomized_mask, start_slice=90, end_slice=130)
