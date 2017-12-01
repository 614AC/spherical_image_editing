import os
from bubble_animation import bubble_anim
from sphere_transforms import generate_image, rotate_equirect_image
from datetime import datetime
import uuid
import sys


def one_shot(output_folder, pano_A_filename, pano_B_filename, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, image_width = 4096, num_frames = 90):
  image_height = image_width / 2
  
  # create the output folder
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  
  # rotate image B to match image A if required
  rotated_pano_B_filename = pano_B_filename
  if(pano_A_zoom_centre != pano_B_zoom_centre):
    rotated_pano_B_filename = rotate_equirect_image(pano_B_filename, pano_B_zoom_centre[0], pano_A_zoom_centre[0])
  
  # generate the droste
  print "start: " + datetime.now().strftime('%H:%M:%S')
  for i in range(0, num_frames + 1):
    zoom_loop_value = -1 * float(i) / float(num_frames)
    # TODO: send subtract amount
    generate_image(pano_A_zoom_centre, zoom_factor, zoom_cutoff, pano_A_filename, rotated_pano_B_filename, out_x_size = image_width, zoom_loop_value = zoom_loop_value, save_filename = output_folder + "/droste_anim_" + str(i).zfill(3) + ".png")
  
  # generate the bubble in anim
  pano_A_no_bubble = pano_A_filename
  pano_A_bubble = output_folder + "/droste_anim_" + str(0).zfill(3) + ".png"
  bubble_A_diam = 760.0
  
  for i in range(1,int(num_frames)):
    bubble_anim(pano_A_bubble,pano_A_no_bubble, pano_A_zoom_centre, bubble_A_diam, float(i)/num_frames, output_folder + "/in_bubble_anim_" + str(int(i)).zfill(3) + ".png")
  
  # generate the bubble out anim
  pano_B_no_bubble = rotated_pano_B_filename
  pano_B_bubble = output_folder + "/droste_anim_" + str(num_frames).zfill(3) + ".png"
  bubble_B_diam = 1808.0
  bubble_B_position = (((image_width / 2) + pano_A_zoom_centre[0]) % image_width, image_height / 2)
  print bubble_B_position

  for i in range(int(num_frames),1,-1):
    bubble_anim(pano_B_bubble,pano_B_no_bubble, bubble_B_position, bubble_B_diam, float(i)/num_frames, output_folder + "/out_bubble_anim_" + str(int(num_frames - i)).zfill(3) + ".png")


def start_one_shot_generation(pano_A_zoom_centre, pano_B_zoom_centre, pano_folder, pano_a_short_name, pano_b_short_name):
  print "Starting: " + pano_a_short_name + " to " + pano_b_short_name
  
  folder_contents = os.listdir(pano_folder)
  pano_a_filename = next(obj for obj in folder_contents if obj.startswith(pano_a_short_name) and obj.endswith("_pano.jpg"))
  pano_b_filename = next(obj for obj in folder_contents if obj.startswith(pano_b_short_name) and obj.endswith("_pano.jpg"))
  
  # presets
  zoom_factor = 4
  zoom_cutoff = 1.2
  bubble_out_diameter = 1808.0
  bubble_in_diameter = 760.0
  
  # required
  pano_A_zoom_centre = (pano_A_zoom_centre,1024)
  pano_B_zoom_centre = (pano_B_zoom_centre,1024)
  pano_A_filepath = pano_folder + pano_a_filename
  pano_B_filepath = pano_folder + pano_b_filename
  folder_name = pano_folder + 'test_one_shot_generation/' + pano_a_short_name + "_to_" + pano_b_short_name
  
  try:
    one_shot(folder_name, pano_A_filepath, pano_B_filepath, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff)
  except Exception:
    print("Unexpected error:", sys.exc_info()[0])
    print("when generating " + folder_name)

if __name__ == '__main__':
  pano_A_zoom_xcord = 2079
  pano_B_zoom_xcord = 2041
  node_A_id = '0bd07'
  node_B_id = '656d4'
  pano_folder = './buddha/'
  start_one_shot_generation(pano_A_zoom_xcord, pano_B_zoom_xcord, pano_folder, node_A_id, node_B_id)
  
  
  
  
  
