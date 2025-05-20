# Task 1.1 - Femur & Tibia segmentation using image processing
import os
import sys
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.io_utils import save_nifti
from utils.viz_utils import show_overlay_scroll

def load_nifti(path):
    nii = nib.load(path)
    return nii.get_fdata(), nii.affine, nii.header

def show_middle_slices(volume, num_slices=3):
    z_dim = volume.shape[2]
    step = z_dim // (num_slices + 1)

    fig, axes = plt.subplots(1, num_slices, figsize=(15, 5))
    for i in range(num_slices):
        slice_idx = (i + 1) * step
        axes[i].imshow(volume[:, :, slice_idx], cmap='gray')
        axes[i].set_title(f"Slice {slice_idx}")
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

def apply_threshold(volume, lower=250, upper=3000):
    mask = np.logical_and(volume > lower, volume < upper)
    return mask.astype(np.uint8)

def show_mask_overlay(volume, mask, slice_idx):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.imshow(volume[:, :, slice_idx], cmap='gray')
    ax.imshow(mask[:, :, slice_idx], alpha=0.5, cmap='Reds')  # more vivid colormap
    ax.set_title(f"Thresholded Overlay - Slice {slice_idx}")
    ax.axis('off')
    plt.tight_layout()
    plt.show()

def clean_mask(mask, min_size=1000):
    """Remove small connected components below min_size"""
    labeled, num_features = ndimage.label(mask)
    sizes = ndimage.sum(mask, labeled, range(num_features + 1))
    
    mask_clean = np.zeros_like(mask)
    for i, size in enumerate(sizes):
        if size >= min_size:
            mask_clean[labeled == i] = 1
    return mask_clean

def extract_largest_components(mask, num_components=2):
    """Keep only the largest N connected components (e.g., femur and tibia)"""
    labeled, num_features = ndimage.label(mask)
    sizes = ndimage.sum(mask, labeled, range(num_features + 1))

    # Get indices of top N largest components
    top_indices = np.argsort(sizes)[-num_components:]
    
    output_mask = np.zeros_like(mask)
    for i in top_indices:
        output_mask[labeled == i] = 1
    return output_mask



if __name__ == "__main__":
    path = "data/left_knee.nii"
    volume, affine, header = load_nifti(path)
    print(f"Volume shape: {volume.shape}")
    
    # Step 1: Visualize CT slice
    show_middle_slices(volume)

    # Step 2: Threshold
    mask = apply_threshold(volume, lower=250, upper=3000)
    show_mask_overlay(volume, mask, slice_idx=volume.shape[2] // 2)

    # Step 3: Clean mask
    mask_clean = clean_mask(mask, min_size=1000)
    show_mask_overlay(volume, mask_clean, slice_idx=volume.shape[2] // 2)

    # Step 4: Extract femur and tibia
    final_mask = extract_largest_components(mask_clean, num_components=2)
    show_mask_overlay(volume, final_mask, slice_idx=volume.shape[2] // 2)

    # # Save final binary mask as NIfTI file
    # output_path = "results/original_mask.nii.gz"
    # save_nifti(final_mask, affine, header, output_path)

    show_overlay_scroll(volume, mask, start_slice=90, end_slice=130)


