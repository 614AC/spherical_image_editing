import os
from typing import List
from bubble_animation import bubble_anim
from sphere_transforms import generate_image, rotate_equirect_image
from datetime import datetime
import uuid
import imageio
from threading import Thread
from tqdm import trange


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


def one_shot(output_folder,
             pano_A_filename,
             pano_B_filename,
             pano_A_zoom_centre,
             pano_B_zoom_centre,
             bubble_in_diameter,
             bubble_out_diameter,
             zoom_factor,
             zoom_cutoff,
             image_width=2048,
             num_frames=120):
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
    NUM_THREADS = 4
    threads = []
    loop_per_threads = int((num_frames + 1) / NUM_THREADS)
    for i in range(NUM_THREADS):
        # zoom_loop_value = -1 * float(i) / float(num_frames)
        # TODO: send subtract amount
        threads.append(
            Thread(target=loop_generate_image,
                   args=(i * loop_per_threads, (i + 1) * loop_per_threads if
                         (i + 1) * loop_per_threads <= num_frames + 1 else
                         num_frames + 1, pano_A_zoom_centre, zoom_factor,
                         zoom_cutoff, pano_A_filename, rotated_pano_B_filename,
                         image_width, num_frames,
                         output_folder + "\\droste_anim_")))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        # generate_image(pano_A_zoom_centre,
        #                zoom_factor,
        #                zoom_cutoff,
        #                pano_A_filename,
        #                rotated_pano_B_filename,
        #                out_x_size=image_width,
        #                zoom_loop_value=zoom_loop_value,
        #                save_filename=output_folder + "\\droste_anim_" +
        #                str(i).zfill(3) + ".png")

    bubble_num_frames = 30

    # generate the bubble in anim
    pano_A_no_bubble = pano_A_filename
    pano_A_bubble = output_folder + "\\droste_anim_" + str(0).zfill(3) + ".png"
    bubble_A_diam = 760.0

    threads.clear()
    loop_per_threads = int((bubble_num_frames - 1) / NUM_THREADS)
    for i in range(NUM_THREADS):
        threads.append(
            Thread(target=loop_bubble_in_anim,
                   args=(1 + i * loop_per_threads,
                         1 + (i + 1) * loop_per_threads if 1 +
                         (i + 1) * loop_per_threads <= bubble_num_frames else
                         bubble_num_frames, pano_A_bubble, pano_A_no_bubble,
                         pano_A_zoom_centre, bubble_A_diam, bubble_num_frames,
                         output_folder + "\\in_bubble_anim_")))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # generate the bubble out anim
    pano_B_no_bubble = rotated_pano_B_filename
    pano_B_bubble = output_folder + "\\droste_anim_" + str(
        bubble_num_frames).zfill(3) + ".png"
    bubble_B_diam = 760.0
    bubble_B_position = (int(
        ((image_width / 2) + pano_A_zoom_centre[0]) % image_width),
                         int(image_height / 2))
    print(bubble_B_position)

    threads.clear()
    loop_per_threads = int((bubble_num_frames - 1) / NUM_THREADS)
    for i in range(NUM_THREADS):
        threads.append(
            Thread(target=loop_bubble_out_anim,
                   args=(bubble_num_frames - i * loop_per_threads,
                         bubble_num_frames -
                         (i + 1) * loop_per_threads if bubble_num_frames -
                         (i + 1) * loop_per_threads >= 1 else 1, pano_B_bubble,
                         pano_B_no_bubble, bubble_B_position, bubble_B_diam,
                         bubble_num_frames,
                         output_folder + "\\out_bubble_anim_")))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    imgs = []
    for i in range(1, bubble_num_frames):
        imgs.append(
            imageio.imread(output_folder + "\\in_bubble_anim_" +
                           str(i).zfill(3) + ".png"))
    for i in range(num_frames + 1):
        imgs.append(
            imageio.imread(output_folder + "\\droste_anim_" + str(i).zfill(3) +
                           ".png"))
    for i in range(bubble_num_frames - 1):
        imgs.append(
            imageio.imread(output_folder + "\\out_bubble_anim_" +
                           str(i).zfill(3) + ".png"))
    imageio.mimsave(output_folder + "\\" + pano_A_filename.split('_')[0] +
                    "_" + pano_B_filename.split('_')[0] + ".mp4",
                    imgs,
                    fps=30)


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
    folder_name = pano_folder + 'test_one_shot_generation\\' + pano_a_short_name + "_to_" + pano_b_short_name

    # try:
    one_shot(folder_name, pano_A_filepath, pano_B_filepath, pano_A_zoom_centre,
             pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter,
             zoom_factor, zoom_cutoff)
    # except Exception:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     print("when generating " + folder_name)


if __name__ == '__main__':
    pano_A_zoom_xcord = (1610, 535)
    pano_B_zoom_xcord = (787, 535)
    node_A_id = '00ebbf3782c64d74aaf7dd39cd561175_skybox'
    node_B_id = 'ee59d6b5e5da4def9fe85a8ba94ecf25_skybox'
    pano_folder = '.\\matterport_pano_images\\'
    start_one_shot_generation(pano_A_zoom_xcord, pano_B_zoom_xcord,
                              pano_folder, node_A_id, node_B_id)
