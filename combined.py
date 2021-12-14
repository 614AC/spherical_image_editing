import os
from typing import List
from bubble_animation import bubble_anim
from sphere_transforms import generate_image, rotate_equirect_image
from datetime import datetime
import uuid
import imageio
from threading import Thread
from tqdm import trange
from multiprocessing import Pool
from config import mapping_dict


def loop_generate_image(s, t, zoom_center_pixel_coords, zoom_factor,
                        zoom_cutoff, source_image_filename_A,
                        source_image_filename_B, out_x_size, num_frames,
                        save_filename_prefix):
    for i in trange(s, t + 1):
        zoom_loop_value = -1 * float(i) / float(num_frames)
        generate_image(zoom_center_pixel_coords, zoom_factor, zoom_cutoff,
                       source_image_filename_A, source_image_filename_B,
                       out_x_size, zoom_loop_value,
                       save_filename_prefix + str(i).zfill(3) + ".png")


def loop_bubble_in_anim(s, t, image_with_bubble_filename,
                        image_without_bubble_filename, bubble_position,
                        bubble_diameter, num_frames, output_filename_prefix):
    for i in trange(s, t + 1):
        bubble_anim(image_with_bubble_filename, image_without_bubble_filename,
                    bubble_position, bubble_diameter,
                    float(i) / num_frames,
                    output_filename_prefix + str(i).zfill(3) + ".png")


def loop_bubble_out_anim(s, t, image_with_bubble_filename,
                         image_without_bubble_filename, bubble_position,
                         bubble_diameter, num_frames, output_filename_prefix):
    for i in trange(s, t + 1, step=-1):
        bubble_anim(
            image_with_bubble_filename, image_without_bubble_filename,
            bubble_position, bubble_diameter,
            float(i) / num_frames, output_filename_prefix +
            str(int(num_frames - i)).zfill(3) + ".png")


def generate(output_folder,
             pano_A_filename,
             pano_B_filename,
             pano_A_zoom_centre,
             pano_B_zoom_centre,
             bubble_in_diameter,
             bubble_out_diameter,
             zoom_factor,
             zoom_cutoff,
             image_width=2048,
             num_frames=120,
             bubble_num_frames=30):
    image_height = image_width / 2

    # create the output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # rotate image B to match image A if required
    rotated_pano_B_filename = pano_B_filename
    if (pano_A_zoom_centre != pano_B_zoom_centre):
        rotated_pano_B_filename = rotate_equirect_image(
            pano_B_filename, pano_B_zoom_centre[0], pano_A_zoom_centre[0])

    # generate the droste
    print("start: " + datetime.now().strftime('%H:%M:%S'))

    for _ in trange(1):
        args = list()
        for i in range(num_frames + 1):
            zoom_loop_value = -1 * float(i) / float(num_frames)
            args.append(
                (pano_A_zoom_centre, zoom_factor, zoom_cutoff, pano_A_filename,
                 rotated_pano_B_filename, zoom_loop_value,
                 output_folder + "\\droste_anim_" + str(i).zfill(3) + ".png"))

        with Pool(processes=4) as pool:
            pool.starmap(generate_image, args)

    # generate the bubble in anim
    pano_A_no_bubble = pano_A_filename
    pano_A_bubble = output_folder + "\\droste_anim_" + str(0).zfill(3) + ".png"
    bubble_A_diam = 760.0

    for i in trange(1, bubble_num_frames):
        bubble_anim(
            pano_A_bubble, pano_A_no_bubble, pano_A_zoom_centre, bubble_A_diam,
            float(i) / float(bubble_num_frames),
            output_folder + "\\in_bubble_anim_" + str(i).zfill(3) + ".png")

    # generate the bubble out anim
    pano_B_no_bubble = rotated_pano_B_filename
    pano_B_bubble = output_folder + "\\droste_anim_" + str(
        bubble_num_frames).zfill(3) + ".png"
    bubble_B_diam = 760.0
    bubble_B_position = (int(
        ((image_width / 2) + pano_A_zoom_centre[0]) % image_width),
                         int(image_height / 2))

    for i in trange(bubble_num_frames, 1, -1):
        bubble_anim(
            pano_B_bubble, pano_B_no_bubble, bubble_B_position, bubble_B_diam,
            float(i) / bubble_num_frames,
            output_folder + "\\out_bubble_anim_" +
            str(int(bubble_num_frames - i)).zfill(3) + ".png")


def start_one_shot_generation(pano_A_zoom_centre, pano_B_zoom_centre,
                              pano_folder, pano_a_short_name,
                              pano_b_short_name):
    print("Starting: " + pano_a_short_name + " to " + pano_b_short_name)

    pano_a_filename = pano_a_short_name + "_pano.jpg"
    pano_b_filename = pano_b_short_name + "_pano.jpg"

    # presets
    zoom_factor = 4
    zoom_cutoff = 1.2
    bubble_out_diameter = 760.0
    bubble_in_diameter = 760.0

    # required
    pano_A_filepath = pano_folder + pano_a_filename
    pano_B_filepath = pano_folder + pano_b_filename
    folder_name = '.\\test_one_shot_generation\\' + \
        pano_a_short_name + "_to_" + pano_b_short_name

    num_frames = 120
    bubble_num_frames = 30

    generate(folder_name,
             pano_A_filepath,
             pano_B_filepath,
             pano_A_zoom_centre,
             pano_B_zoom_centre,
             bubble_in_diameter,
             bubble_out_diameter,
             zoom_factor,
             zoom_cutoff,
             num_frames=num_frames,
             bubble_num_frames=bubble_num_frames)

    imgs = []
    for i in range(1, bubble_num_frames):
        imgs.append(
            imageio.imread(folder_name + "\\in_bubble_anim_" +
                           str(i).zfill(3) + ".png"))
    for i in range(num_frames + 1):
        imgs.append(
            imageio.imread(folder_name + "\\droste_anim_" + str(i).zfill(3) +
                           ".png"))
    for i in range(bubble_num_frames - 1):
        imgs.append(
            imageio.imread(folder_name + "\\out_bubble_anim_" +
                           str(i).zfill(3) + ".png"))
    imageio.mimsave(".\\video\\" + pano_a_short_name.split('_')[0] + "_" +
                    pano_b_short_name.split('_')[0] + ".mp4",
                    imgs,
                    fps=30)


if __name__ == '__main__':
    pano_folder = '.\\matterport_pano_images\\'
    defualt_height = 535

    for key in mapping_dict.keys():
        node_A_id = key
        children = mapping_dict[key]
        for keyy in children.keys():
            node_B_id = keyy
            pano_A_zoom_xcord = (children[keyy][0], defualt_height)
            pano_B_zoom_xcord = (children[keyy][1], defualt_height)

            print("Error generating " + node_A_id + " to " + node_B_id)

            try:
                start_one_shot_generation(pano_A_zoom_xcord, pano_B_zoom_xcord,
                                          pano_folder, node_A_id, node_B_id)
            except Exception:
                print("Error generating " + node_A_id + " to " + node_B_id)
