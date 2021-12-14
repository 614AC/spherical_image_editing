import numpy as np
from numpy import pi
from PIL import Image, ImageDraw
from math import floor
import uuid


def rotate_pano_image(s_img, from_x, to_x):
    dist = abs(from_x - to_x)

    l_box = (0, 0, 0, 0)
    r_box = (0, 0, 0, 0)

    if (from_x < to_x):
        l_box = (0, 0, s_img.size[0] - dist, s_img.size[1])
        r_box = (s_img.size[0] - dist, 0, s_img.size[0], s_img.size[1])
    else:
        l_box = (0, 0, dist, s_img.size[1])
        r_box = (dist, 0, s_img.size[0], s_img.size[1])

    right = s_img.crop(r_box)
    left = s_img.crop(l_box)

    new_im = Image.new('RGB', s_img.size)
    new_im.paste(right, (0, 0))
    new_im.paste(left, (right.size[0], 0))

    return new_im


def bubble_anim(image_with_bubble_filename, image_without_bubble_filename,
                bubble_position, bubble_diameter, t, output_filename):
    # print t

    bubble_radius = int(floor(bubble_diameter / 2))
    bubble_size = bubble_diameter * t

    bubble_image = Image.open(image_with_bubble_filename)
    pano_image = Image.open(image_without_bubble_filename)

    need_to_shift_image = False
    move_amount = 0
    if (((bubble_position[0] + bubble_radius) > pano_image.size[0])
            or ((bubble_position[0] - bubble_radius) < 0)):
        need_to_shift_image = True
        move_to = pano_image.size[0] - bubble_radius
        move_amount = bubble_position[0] - move_to

        bubble_image = rotate_pano_image(bubble_image, bubble_position[0],
                                         move_to)
        pano_image = rotate_pano_image(pano_image, bubble_position[0], move_to)

        bubble_position = (bubble_position[0] - move_amount,
                           bubble_position[1])

    bubble_rect = (bubble_position[0] - bubble_radius,
                   bubble_position[1] - bubble_radius,
                   bubble_position[0] + bubble_radius,
                   bubble_position[1] + bubble_radius)
    bubble = bubble_image.crop(bubble_rect)

    mask = Image.new('1', bubble.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, bubble.size[0], bubble.size[1]),
                 fill='white',
                 outline='white')

    mask.thumbnail((bubble_size, bubble_size), Image.ANTIALIAS)
    bubble.thumbnail((bubble_size, bubble_size), Image.ANTIALIAS)

    new_im = Image.new('RGB', pano_image.size)
    new_im.paste(pano_image, (0, 0))
    new_im.paste(bubble, (bubble_position[0] - int(bubble_size / 2),
                          bubble_position[1] - int(bubble_size / 2)),
                 mask=mask)

    if (need_to_shift_image):
        new_im = rotate_pano_image(new_im, bubble_position[0],
                                   bubble_position[0] + move_amount)

    temp_file_name = str(uuid.uuid4()) + ".png"
    new_im.save(output_filename, "PNG")


if __name__ == '__main__':
    num_frames = 60.0
    '''
  # bubble in
  bubble_diam = 760.0
  bubble_position = (1464,1024)
  for i in range(1,int(num_frames)):
    bubble_anim('./buddha/zf4_sv1p4_zc1p2/bubble_in_anim/pano_bubble.png','./buddha/zf4_sv1p4_zc1p2/bubble_in_anim/pano_nobubble.jpg', bubble_position, bubble_diam, float(i)/num_frames, "./buddha/zf4_sv1p4_zc1p2/bubble_in_anim/in_bubble_anim_" + str(int(i)).zfill(3) + ".png")
  '''

    # bubble out
    bubble_diam = 1808.0
    bubble_position = (3485, 1024)
    for i in range(int(num_frames), 1, -1):
        bubble_anim(
            './buddha/zf4_sv1p4_zc1p2/bubble_out_anim/pano_bubble.png',
            './buddha/zf4_sv1p4_zc1p2/bubble_out_anim/pano_nobubble.png',
            bubble_position, bubble_diam,
            float(i) / num_frames,
            "./buddha/zf4_sv1p4_zc1p2/bubble_out_anim/out_bubble_anim_" +
            str(int(num_frames - i)).zfill(3) + ".png")
