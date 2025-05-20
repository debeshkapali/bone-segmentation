import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.io_utils import load_nifti
from utils.viz_utils import show_landmarks_on_slice

# Load CT volume (and optionally mask)
ct_volume, _, _ = load_nifti("masks\mask_femur_tibia_expanded_2mm.nii.gz")

# Example landmarks (replace with actual ones you detect)
# Each landmark should be a (x, y, z) tuple
landmarks = [(120, 100, 95), (110, 105, 100), (130, 115, 95)]

# Visualize on a specific slice
show_landmarks_on_slice(ct_volume, landmarks, slice_index=95)
