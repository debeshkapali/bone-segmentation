# 🦴 Bone Segmentation and Tibial Landmark Detection from Knee CT Scans

This project focuses on segmenting the tibia bone from 3D knee CT scans and identifying the **medial** and **lateral lowest surface points** on the tibia, following a series of preprocessing, morphological expansion, and mask randomization steps.

---

## 🎯 Objective

The primary goal is to identify consistent anatomical tibial landmarks across multiple mask variations derived from a single 3D CT scan of a left knee. These variations include morphological expansions and randomized perturbations. The process aims to support reproducibility and robustness testing in medical imaging workflows.

---

## 📁 Project Structure

<pre> <code> ``` bone-segmentation-knee/ ├── data/ # Input CT data (left_knee.nii), not included in github since the data size exceeds the limit(100 MB) ├── results/ # Output masks and landmark CSVs ├── report/ # Final report in .pdf ├── src/ # Core scripts for processing ├── tests/ # Debug/testing scripts ├── utils/ # IO and visualization utilities ├── requirements.txt # Python dependencies └── README.md # Project overview ``` </code> </pre>


---

## 📌 Key Steps Performed

1. **Original Tibia Segmentation**  
   - Loaded CT volume and binary tibial mask.

2. **Morphological Expansion**  
   - Performed 3D dilation to generate 2 mm and 4 mm expanded masks.

3. **Randomized Masks**  
   - Generated two versions of randomized masks by slightly perturbing the tibial boundary surface.

4. **Landmark Detection**  
   - Detected **medial** and **lateral lowest tibial surface points** in the axial slice with maximum tibial extent.

5. **CSV Export**  
   - Stored landmark coordinates for each mask in `results/tibia_landmarks.csv`.

---

## 🧠 Methodology

- The tibia region is first isolated using binary masks.
- For expanded masks, 3D morphological dilation is applied using a kernel size proportional to the desired physical distance (2mm, 4mm).
- Randomized masks are created by applying controlled random perturbations within a 2mm neighborhood using binary erosion and dilation.
- For landmark detection:
  - The lowest axial slice containing tibia is located.
  - The tibial region is split medially and laterally at the centroid.
  - Bottom-most nonzero voxels are identified in both regions and returned as landmark coordinates.

---

## 📂 Scripts Overview

| Script                  | Description |
|-------------------------|-------------|
| `expansion.py`        | Creates expanded versions of the tibial mask (2mm & 4mm) |
| `randomization.py`     | Generates randomized tibial masks using morphological noise |
| `landmark_detection.py` | Main script to detect tibial landmarks for a given mask |
| `segmentation.py` | Script to segment tibia and femur |
| `utils/io_utils.py`           | Load/save NIfTI images using nibabel |
| `utils/viz_utils.py`    | Overlay landmarks on CT slices for visualization |
| `tests/*.py`            | Test and debug scripts (e.g., `test_landmarks.py`, `inspect_expansion.py`) |

---

## 📎 Input

- **CT Scan**: `left_knee.nii` — A volumetric DICOM-to-NIfTI converted file (e.g., 512×512×216)
- **Tibial Mask**: `original_mask.nii.gz` — Binary mask of the tibia extracted from CT

---

## 📤 Output

Located in the `results/` folder:

- `original_mask.nii.gz`
- `mask_femur_tibia_expanded_2mm.nii.gz`
- `mask_femur_tibia_expanded_4mm.nii.gz`
- `Randomized_mask_1.nii.gz`
- `Randomized_mask_2.nii.gz`
- `landmark_coordinates.csv` — CSV containing medial and lateral landmark coordinates for each mask

---

## 🚀 How to Run

Ensure Python 3.7+ is installed and dependencies are satisfied:

```bash
pip install -r requirements.txt
```

---

## 📬 Submission
This repository includes:

- Python scripts for mask preprocessing and landmark detection (src/)

- Utility functions (utils/)

- Final report (report/)

- Processed masks and landmark outputs (results/)

- README.md with instructions and overview