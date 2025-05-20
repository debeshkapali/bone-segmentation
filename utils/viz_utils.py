# Utility functions for visualization and plotting
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def show_overlay_scroll(volume, mask, start_slice=90, end_slice=130):
    slice_idx = start_slice

    # Initial plot
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.2)

    ct_slice = ax.imshow(volume[:, :, slice_idx], cmap='gray')
    mask_overlay = ax.imshow(mask[:, :, slice_idx], cmap='Reds', alpha=0.3)
    ax.set_title(f"Slice {slice_idx}")
    ax.axis('off')

    # Slider
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Slice', start_slice, end_slice - 1, valinit=slice_idx, valstep=1)

    def update(val):
        i = int(slider.val)
        ct_slice.set_data(volume[:, :, i])
        mask_overlay.set_data(mask[:, :, i])
        ax.set_title(f"Slice {i}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def show_two_masks_overlay_scroll(volume, mask1, mask2, 
                                  mask1_cmap='Reds', mask2_cmap='Blues', 
                                  mask1_alpha=0.5, mask2_alpha=0.3,
                                  start_slice=90, end_slice=130):
    slice_idx = start_slice

    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.2)

    ct_slice = ax.imshow(volume[:, :, slice_idx], cmap='gray')
    mask1_overlay = ax.imshow(np.ma.masked_where(mask1[:, :, slice_idx] == 0, mask1[:, :, slice_idx]),
                             cmap=mask1_cmap, alpha=mask1_alpha)
    mask2_overlay = ax.imshow(np.ma.masked_where(mask2[:, :, slice_idx] == 0, mask2[:, :, slice_idx]),
                             cmap=mask2_cmap, alpha=mask2_alpha)
    ax.set_title(f"Slice {slice_idx}")
    ax.axis('off')

    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Slice', start_slice, end_slice - 1, valinit=slice_idx, valstep=1)

    def update(val):
        i = int(slider.val)
        ct_slice.set_data(volume[:, :, i])
        mask1_overlay.set_data(np.ma.masked_where(mask1[:, :, i] == 0, mask1[:, :, i]))
        mask2_overlay.set_data(np.ma.masked_where(mask2[:, :, i] == 0, mask2[:, :, i]))
        ax.set_title(f"Slice {i}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def show_masks_side_by_side(volume, mask1, mask2, start_slice=90, end_slice=130):
    slice_idx = start_slice

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(bottom=0.2)

    im1 = ax1.imshow(volume[:, :, slice_idx], cmap='gray')
    overlay1 = ax1.imshow(mask1[:, :, slice_idx], cmap='Reds', alpha=0.3)
    ax1.set_title("Original Mask")
    ax1.axis('off')

    im2 = ax2.imshow(volume[:, :, slice_idx], cmap='gray')
    overlay2 = ax2.imshow(mask2[:, :, slice_idx], cmap='Blues', alpha=0.3)
    ax2.set_title("Expanded Mask")
    ax2.axis('off')

    ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
    slider = Slider(ax_slider, 'Slice', start_slice, end_slice - 1, valinit=slice_idx, valstep=1)

    def update(val):
        i = int(slider.val)
        im1.set_data(volume[:, :, i])
        overlay1.set_data(mask1[:, :, i])
        im2.set_data(volume[:, :, i])
        overlay2.set_data(mask2[:, :, i])
        ax1.set_title(f"Original Mask - Slice {i}")
        ax2.set_title(f"Expanded Mask - Slice {i}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()


def show_side_by_side_masks(ct_volume, original_mask, randomized_mask, start_slice=90, end_slice=130):
    """
    View original and randomized masks side by side overlaid on CT slices.
    """
    slice_idx = start_slice

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(bottom=0.2)

    # Left: original mask overlay
    ct_left = axes[0].imshow(ct_volume[:, :, slice_idx], cmap='gray')
    mask_left = axes[0].imshow(original_mask[:, :, slice_idx], cmap='Reds', alpha=0.3)
    axes[0].set_title(f"Original Mask - Slice {slice_idx}")
    axes[0].axis('off')

    # Right: randomized mask overlay
    ct_right = axes[1].imshow(ct_volume[:, :, slice_idx], cmap='gray')
    mask_right = axes[1].imshow(randomized_mask[:, :, slice_idx], cmap='Reds', alpha=0.3)
    axes[1].set_title(f"Randomized Mask - Slice {slice_idx}")
    axes[1].axis('off')

    # Slider
    ax_slider = plt.axes([0.25, 0.05, 0.5, 0.03])
    slider = Slider(ax_slider, 'Slice', start_slice, end_slice - 1, valinit=slice_idx, valstep=1)

    def update(val):
        i = int(slider.val)
        ct_left.set_data(ct_volume[:, :, i])
        mask_left.set_data(original_mask[:, :, i])
        axes[0].set_title(f"Original Mask - Slice {i}")

        ct_right.set_data(ct_volume[:, :, i])
        mask_right.set_data(randomized_mask[:, :, i])
        axes[1].set_title(f"Randomized Mask - Slice {i}")

        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def show_landmarks_on_slice(volume, landmarks, slice_index, title="Landmarks on CT Slice", radius=3):
    """
    Visualizes a single CT slice with landmarks overlaid.

    Parameters:
        volume (numpy.ndarray): The 3D CT volume (H, W, D).
        landmarks (list of tuples): List of (x, y, z) coordinates of landmarks.
        slice_index (int): The axial slice to show (z-axis).
        title (str): Title of the plot.
        radius (int): Size of the landmark dot.
    """
    import matplotlib.patches as patches

    slice_img = volume[:, :, slice_index]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(slice_img, cmap='gray')
    ax.set_title(f"{title} - Slice {slice_index}")
    ax.axis('off')

    for (x, y, z) in landmarks:
        if int(round(z)) == slice_index:
            circ = patches.Circle((x, y), radius=radius, color='red')
            ax.add_patch(circ)

    plt.show()


