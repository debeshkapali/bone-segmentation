# Utility functions for loading/saving NIfTI files
import nibabel as nib
import numpy as np

def load_nifti(path):
    """
    Load a NIfTI file and return volume data, affine, and header.
    """
    nifti = nib.load(path)
    volume = nifti.get_fdata()
    affine = nifti.affine
    header = nifti.header
    print(f"Loaded: {path} | Shape: {volume.shape}")
    return volume.astype(np.uint8), affine, header

def save_nifti(volume, affine, header, save_path):
    nifti = nib.Nifti1Image(volume.astype(np.uint8), affine, header)
    nib.save(nifti, save_path)
    print(f"Saved: {save_path}")
