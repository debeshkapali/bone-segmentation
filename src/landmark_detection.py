# Task 1.4 - Detect medial and lateral lowest points on tibia
import numpy as np
import nibabel as nib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.io_utils import save_nifti, load_nifti
from utils.viz_utils import show_landmarks_on_slice


def detect_lowest_medial_lateral_points(tibia_mask):
    z_dim = tibia_mask.shape[2]
    
    for z in range(z_dim - 1, -1, -1):
        slice_mask = tibia_mask[:, :, z]
        coords = np.column_stack(np.where(slice_mask > 0))
        if len(coords) > 0:
            print(f"Lowest slice with tibia pixels found at z = {z}, number of pixels = {len(coords)}")
            break

    if len(coords) == 0:
        raise ValueError("No tibia pixels found in any slice.")

    center_x = int(np.mean(coords[:, 0]))
    print(f"Using center_x = {center_x} for splitting")

    medial = coords[coords[:, 0] < center_x]
    lateral = coords[coords[:, 0] >= center_x]

    print(f"Medial pixels: {len(medial)}, Lateral pixels: {len(lateral)}")

    if len(medial) == 0 or len(lateral) == 0:
        raise ValueError("Could not find both medial and lateral points.")

    medial_point = medial[np.argmax(medial[:, 1])]
    lateral_point = lateral[np.argmax(lateral[:, 1])]

    return tuple(medial_point) + (z,), tuple(lateral_point) + (z,)


if __name__ == "__main__":
    import csv
    import os

    # Paths
    ct_path = "data/left_knee.nii"
    mask_files = {
        "original_mask": "results\original_mask.nii.gz",
        "expanded_mask_2mm": "results\mask_femur_tibia_expanded_2mm.nii.gz",
        "expanded_mask_4mm": "results\mask_femur_tibia_expanded_4mm.nii.gz",
        "randomized_mask_1": "results\Randomized_mask.nii.gz",
        "randomized_mask_2": "results\Randomized_mask_2.nii.gz"
    }

    # Load CT once
    ct_volume, _, _ = load_nifti(ct_path)

    # To store results
    results = []

    for mask_name, mask_path in mask_files.items():
        print(f"\nProcessing {mask_name}...")
        tibia_mask, _, _ = load_nifti(mask_path)
        print(f"Mask shape: {tibia_mask.shape}, unique values: {np.unique(tibia_mask)}")

        try:
            medial, lateral = detect_lowest_medial_lateral_points(tibia_mask)

            print("  Medial Point:", medial)
            print("  Lateral Point:", lateral)

            # Visualize
            slice_index = medial[2]
            show_landmarks_on_slice(ct_volume, [medial, lateral], slice_index,
                                    title=f"Landmarks - {mask_name}")

            # Save for CSV
            results.append([mask_name, *medial, *lateral])

        except Exception as e:
            print(f"  Failed to detect landmarks: {e}")
            results.append([mask_name, "Error", "Error", "Error", "Error", "Error", "Error"])

    # Save CSV
    os.makedirs("results", exist_ok=True)
    csv_path = "results/landmark_coordinates.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Mask", "Medial_X", "Medial_Y", "Medial_Z", "Lateral_X", "Lateral_Y", "Lateral_Z"])
        writer.writerows(results)

    print(f"\n✅ Landmark coordinates saved to: {csv_path}")




