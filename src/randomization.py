# Task 1.3 - Generate randomized masks between original and expanded
import numpy as np
from scipy.ndimage import distance_transform_edt

def generate_randomized_mask(original_mask, max_distance_mm=2.0, voxel_spacing=(1.0, 1.0, 1.0), seed=None):
    """
    Generate a randomized mask between the original and expanded mask.
    
    Parameters:
        original_mask (ndarray): Binary mask (1 for bone, 0 for background).
        max_distance_mm (float): Maximum distance to expand (default 2.0 mm).
        voxel_spacing (tuple): Spacing of voxels in mm (z, y, x).
        seed (int): Random seed for reproducibility.
    
    Returns:
        randomized_mask (ndarray): Randomized binary mask.
    """
    if seed is not None:
        np.random.seed(seed)

    # Step 1: Compute distance from the original mask (outside region only)
    distance = distance_transform_edt(~original_mask, sampling=voxel_spacing)

    # Step 2: Generate random thresholds (same shape as volume)
    random_threshold = np.random.uniform(low=0.0, high=max_distance_mm, size=original_mask.shape)

    # Step 3: Generate randomized region
    # A voxel is added if its distance from original mask is less than the random threshold
    randomized_region = (distance > 0) & (distance <= random_threshold)

    # Step 4: Combine with original mask
    randomized_mask = original_mask | randomized_region

    return randomized_mask.astype(np.uint8)