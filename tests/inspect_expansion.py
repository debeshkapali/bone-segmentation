import os
import sys
import nibabel as nib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.viz_utils import show_two_masks_overlay_scroll
from utils.viz_utils import show_masks_side_by_side

# Load original volume
ct_img = nib.load("data\left_knee.nii")
ct_volume = ct_img.get_fdata()

# Load original segmentation mask
original_mask = nib.load("results\original_mask.nii.gz").get_fdata()

# Load expanded mask
expanded_mask = nib.load("masks/mask_femur_tibia_expanded_2mm.nii.gz").get_fdata()

# Visualize both masks over CT
#show_two_masks_overlay_scroll(ct_volume, original_mask, expanded_mask)

show_masks_side_by_side(ct_volume, original_mask, expanded_mask)
