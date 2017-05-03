import os
from bubble_animation import bubble_anim
from sphere_transforms import droste_effect, rotate_equirect_image
from datetime import datetime
import uuid
import sys


def one_shot(output_folder, pano_A_filename, pano_B_filename, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, subtract_amount, image_width = 4096, num_frames = 90):
  image_height = image_width / 2
  subtract_amount_1 = subtract_amount
  subtract_amount_2 = subtract_amount * 2
  
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
    droste_effect(pano_A_zoom_centre, zoom_factor, zoom_cutoff, pano_A_filename, rotated_pano_B_filename, out_x_size = image_width, zoom_loop_value = zoom_loop_value, save_filename = output_folder + "/droste_anim_" + str(i).zfill(3) + ".png")
  
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
  subtract_amount = 1.4
  bubble_out_diameter = 1808.0
  bubble_in_diameter = 760.0
  
  # required
  pano_A_zoom_centre = (pano_A_zoom_centre,1024)
  pano_B_zoom_centre = (pano_B_zoom_centre,1024)
  pano_A_filepath = pano_folder + pano_a_filename
  pano_B_filepath = pano_folder + pano_b_filename
  folder_name = pano_folder + 'test_one_shot_generation/' + pano_a_short_name + "_to_" + pano_b_short_name
  
  try:
    one_shot(folder_name, pano_A_filepath, pano_B_filepath, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, subtract_amount)
  except Exception:
    print("Unexpected error:", sys.exc_info()[0])
    print("when generating " + folder_name)

def one_shot_with_zc_zf(pano_A_zoom_centre, pano_B_zoom_centre, pano_folder, pano_a_short_name, pano_b_short_name, zoom_cutoff, zoom_factor, subtract_amount, bubble_out_diameter, bubble_in_diameter, outputsize, num_frames):
  print "Starting: " + pano_a_short_name + " to " + pano_b_short_name
  
  folder_contents = os.listdir(pano_folder)
  pano_a_filename = next(obj for obj in folder_contents if obj.startswith(pano_a_short_name) and obj.endswith("_pano.jpg"))
  pano_b_filename = next(obj for obj in folder_contents if obj.startswith(pano_b_short_name) and obj.endswith("_pano.jpg"))
  
  # required
  pano_A_zoom_centre = (pano_A_zoom_centre,1024)
  pano_B_zoom_centre = (pano_B_zoom_centre,1024)
  pano_A_filepath = pano_folder + pano_a_filename
  pano_B_filepath = pano_folder + pano_b_filename
  folder_name = pano_folder + 'zf_zc_one_shot_generation/_zf_' + str(zoom_factor) + "_zc_" + str(zoom_cutoff) + "/" + pano_a_short_name + "_to_" + pano_b_short_name
  
  one_shot(folder_name, pano_A_filepath, pano_B_filepath, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, subtract_amount, image_width = outputsize, num_frames = num_frames)
  
  
  '''
  try:
    one_shot(folder_name, pano_A_filepath, pano_B_filepath, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, subtract_amount, 1808.0, 760.0, image_width = outputsize, num_frames = num_frames)
  except Exception:
    print("Unexpected error:", sys.exc_info()[0])
    print("when generating " + folder_name)
  '''


if __name__ == '__main__':
  '''
  # Buddha - first 5 nodes
  start_one_shot_generation(2079, 2041, './buddha/', '0bd07', '656d4')
  start_one_shot_generation(4089, 31, './buddha/', '656d4', '0bd07')
  start_one_shot_generation(1237, 1223, './buddha/', '656d4', '37e2e')
  start_one_shot_generation(3271, 3285, './buddha/', '37e2e', '656d4')
  start_one_shot_generation(1510, 3943, './buddha/', '37e2e', '7c792')
  start_one_shot_generation(1895, 3558, './buddha/', '7c792', '37e2e')
  start_one_shot_generation(3406, 2076, './buddha/', '7c792', '4efda') '''
  '''
  # blanford upstairs section 1
  start_one_shot_generation(603, 3857, './blanford/', '53d54', '2754e')
  start_one_shot_generation(1809, 2651, './blanford/', '2754e', '53d54')
  start_one_shot_generation(3807, 753, './blanford/', '2754e', '4bb76')
  start_one_shot_generation(708, 2706, './blanford/', '2754e', 'b8e48')
  start_one_shot_generation(2777, 1891, './blanford/', '2754e', '27869')
  start_one_shot_generation(2801, 1759, './blanford/', '4bb76', '2754e')
  start_one_shot_generation(1582, 1733, './blanford/', '12bce', 'b8e48')
  start_one_shot_generation(29, 1358, './buddha/', '4efda', '7c792')'''
  '''
  # blanford upstairs section 2
  start_one_shot_generation(987, 543, './blanford/', 'dcced', 'b8e48')

  # blanford upstairs section 3
  start_one_shot_generation(864, 3007, './blanford/', 'd97de', '39b5e')
  start_one_shot_generation(3939, 730, './blanford/', '27869', '2754e')
  start_one_shot_generation(658, 2756, './blanford/', 'b8e48', '2754e')
  start_one_shot_generation(3782, 3630, './blanford/', 'b8e48', '12bce')
  start_one_shot_generation(2591, 3035, './blanford/', 'b8e48', 'dcced')

  # unfinished:
  start_one_shot_generation(2777, 1891, './blanford/', '2754e', '27869')
  start_one_shot_generation(2801, 1759, './blanford/', '4bb76', '2754e')
  start_one_shot_generation(1582, 1733, './blanford/', '12bce', 'b8e48')

  start_one_shot_generation(708, 2706, './blanford/', '2754e', 'b8e48')
  start_one_shot_generation(3257, 2315, './blanford/', 'dcced', '0c2a9')
  start_one_shot_generation(266, 1208, './blanford/', '0c2a9', 'dcced')
 
  start_one_shot_generation(2793, 3738, './blanford/', '39b5e', 'b8e48')
  start_one_shot_generation(1795, 526, './blanford/', '39b5e', '6fbfa')
  start_one_shot_generation(959, 2912, './blanford/', '39b5e', 'd97de')
  
  start_one_shot_generation(2574, 3843, './blanford/', '6fbfa', '39b5e')
  start_one_shot_generation(1690, 745, './blanford/', 'b8e48', '39b5e')
  '''
  
  zoom_factor = 4.0
  subtract_amount = 2.3
  
  zoom_cutoff = 1.2
  bubble_out_diameter = 1808.0
  bubble_in_diameter = 760.0
  outputsize = 500
  frames = 2
  
  one_shot_with_zc_zf(2079, 2041, './buddha/', '0bd07', '656d4', zoom_cutoff, zoom_factor, subtract_amount, bubble_out_diameter, bubble_in_diameter, outputsize, frames)
  
  
  
  
  
  
  
  