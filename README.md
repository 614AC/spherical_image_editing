# spherical_image_editing
Editing spherical images/video using Möbius transformations


This is a fork of an original codebase by Henry Segerman. The droste effect he created with eleVR allowed a panorama to recurse into itself using Mobius transformations.

Here, the code is adapted to allow one panorama to transition into another panorama, via Mobius transformations. The code can generate an animation (as a series of images) that transitions from one equirectangular image to another.

To generate a single frame in the animation, call the generate_image function in sphere_transforms.py, like this:

```python
generate_image(pano_A_zoom_centre, zoom_factor, zoom_cutoff, pano_A_filename, rotated_pano_B_filename, out_x_size, zoom_loop_value, save_filename)
```

The parameters are:
* pano_A_zoom_centre: the x position (in pixels) on the origin panoramic image where you want the destination panorama to appear (usually, where in virtual space the destination is from your current location)
* zoom_factor: how zoomed in you want the destination panorama to start
* zoom_cutoff: how big you want the destination panorama to start (as a circle at the destination point)
* pano_A_filename: file name of the origin panoramic image (equirectangular)
* rotated_pano_B_filename: the file name of the destination panoramic image. Note that this panorama must be rotated so the "forward" direction in both panoramas align (if this isn't the case, use rotate_equirect_image() in sphere_transforms.py to rotate the panorama to align)
* out_x_size: how big you want the output image to be
* zoom_loop_value: a value from 0 to 1 that specifies how far through the animation you are. A value of 0 means you're fully in the origin panorama, a value of 1 means you're fully in the destination panorama. During animation, this value ranges from 0 to 1, increasing 1/numFrames per frame.
* save_filename: the file where you want the generated frame to go

Note that it is assumed that the vertical point at which the new panorama is going to appear is in the vertical centre of the image.

An animation can be made using the start_one_shot_generation() function in the combined.py file. It has the following signature:

```python
start_one_shot_generation(pano_A_zoom_centre, pano_B_zoom_centre, pano_folder, pano_a_short_name, pano_b_short_name)
```

Note that this function relies on several assumptions:

* that your files are called '<pano_a_short_name>_pano.jpg', and are stored in the pano_folder
* that you want 90 frames in total output
* that you want an output frame size of 4096
* that your input images are 4096 * 2048

This function also generated bubble in and bubble out animations. The bubble in animation animates the destination panorama into the origin panorama, while the bubble out animation animated the origin panorama out of the destination panorama. The bubble in animation can be used at the beginning of the animation to visually explain where the destination panorama has come from, while the bubble out animation can be used at the end to visually explain where the origin panorama went.

These images can then be turned into a video via ffmpeg.