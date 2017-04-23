import os
from bubble_animation import bubble_anim
from sphere_transforms import droste_effect, rotate_equirect_image


def one_shot(output_folder, pano_A_filename, pano_B_filename, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, subtract_amount):
  num_frames = 10
  image_width = 400 # 4096
  
  # create the output folder
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)
  
  # rotate image B to match image A if required
  rotated_pano_B_filename = pano_B_filename
  if(pano_A_zoom_centre != pano_B_zoom_centre):
    rotated_pano_B_filename = rotate_equirect_image(pano_B_filename, pano_B_zoom_centre[0], pano_A_zoom_centre[0])
  
  # generate the droste
  print "start: " + datetime.now().strftime('%H:%M:%S')
  for i in rangeWithEnd(0, num_frames + 1):
    zoom_loop_value = -1 * float(i) / float(num_frames)
    # TODO: send subtract amount
    droste_effect(zoom_point_A, zoom_factor, zoom_cutoff, pano_A_filename, rotated_pano_B_filename, out_x_size = image_width, zoom_loop_value = zoom_loop_value, save_filename = output_folder + "/droste_anim_" + str(i).zfill(3) + ".png")
  
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
  bubble_B_position = (((image_width / 2) + pano_A_zoom_centre) % image_width, image_height / 2)

  for i in range(int(num_frames),1,-1):
    bubble_anim(pano_B_bubble,pano_B_no_bubble, bubble_B_position, bubble_B_diam, float(i)/num_frames, output_folder + "/out_bubble_anim_" + str(int(num_frames - i)).zfill(3) + ".png")
    

if __name__ == '__main__':
  zoom_factor = 4
  zoom_cutoff = 1.2
  subtract_amount = 1.4
  
  pano_A_zoom_centre = (1464,1024)
  pano_B_zoom_centre = (3485,1024)

  bubble_out_diam = 1808.0
  bubble_in_diam = 760.0
  
  pano_A_filename = './buddha/37e2e38392994f83b67c96a6c9e71e1f_pano.jpg'
  pano_B_filename = './buddha/7c79262fda81415fa384036bd04b30b3_pano.jpg'
  
  one_shot('./123to456', pano_A_filename, pano_B_filename, pano_A_zoom_centre, pano_B_zoom_centre, bubble_in_diameter, bubble_out_diameter, zoom_factor, zoom_cutoff, subtract_amount)