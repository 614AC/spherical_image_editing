# spherical_image_editing

Editing spherical images/video using Möbius transformations

This is a fork of an original codebase by andrewmacquarrie. The droste effect he created with eleVR allowed a panorama to recurse into itself using Mobius transformations.

Here, the code is adapted to allow one panorama to transition into another panorama, via Mobius transformations. The code can generate an animation (as a series of images) that transitions from one equirectangular image to another.

To generate a single frame in the animation, call the generate_image function in sphere_transforms.py, like this:

```python
generate_image(pano_A_zoom_centre, zoom_factor, zoom_cutoff, pano_A_filename, rotated_pano_B_filename, out_x_size, zoom_loop_value, save_filename)
```

An animation can be made using the start_one_shot_generation() function in the combined.py file. It has the following signature:

```python
start_one_shot_generation(pano_A_zoom_centre, pano_B_zoom_centre, pano_folder, pano_a_short_name, pano_b_short_name)
```
