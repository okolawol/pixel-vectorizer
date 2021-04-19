import numpy as np
import cv2
from skimage.util import img_as_float, img_as_uint

def step_filter(image):
	imageC = np.copy(image)
	alpha_mask = imageC[:,:,3]
	image_rgb = imageC[:,:,:3]
	image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

	image_gray_norm = img_as_float(image_gray)
	filtered_rgb = triple_step_filter(img_as_float(image_rgb),image_gray_norm,alpha_mask)
	imageC[:,:,:3] = img_as_uint(filtered_rgb)

	return eliminate_mid_transparencies(imageC,alpha_mask)

def triple_step_filter(original_image,monochrome,alpha_mask):
	(bound_rows, bound_cols, channels) = original_image.shape
	output = np.zeros(original_image.shape)
	kernel_size = 3
	for row in range(bound_rows):
		for col in range(bound_cols):
			region = get_region(monochrome,kernel_size,row,col,alpha_mask)
			output[row,col] = compute_middle(region,original_image,row,col)
	return output

def get_region(monochrome,kernel_size,center_row,center_col,alpha_mask):
	bound_cols = monochrome.shape[1]
	region = np.zeros(kernel_size)

	left = -1
	center = monochrome[center_row,center_col]
	right = -1

	if center_col > 0 and alpha_mask[center_row,center_col-1] == 255:
		left = monochrome[center_row,center_col-1]
	if center_col < bound_cols-1 and alpha_mask[center_row,center_col+1] == 255:
		right = monochrome[center_row,center_col+1]

	region[0] = left
	region[1] = center
	region[2] = right

	return region

def compute_middle(region,original_image,center_row,center_col):
	center_pixel = original_image[center_row,center_col]
	if -1 in region:
		return center_pixel
	else:
		sorted_idx = np.argsort(region,axis=0)
		sorted_pixels = region[sorted_idx]
		if sorted_pixels[1] == region[1] and no_dupes(region):
			return compute_new_pixel(sorted_idx,original_image,center_row,center_col)
		else:
			return center_pixel


def is_half_intensity(value):
	return value >= 0.49 and value <= 0.59

def no_dupes(region):
	diff_threshold = 0.019
	color_diff_left = abs(region[0] - region[1])
	color_diff_right = abs(region[1] - region[2])
	if (color_diff_left < diff_threshold) or (color_diff_right < diff_threshold):
		return False
	else:
		unique_items = np.unique(region)
		return unique_items.size == region.size

def compute_new_pixel(idx,original_image,center_row,center_col):
	center_pixel = original_image[center_row,center_col]
	full_alpha = np.ones(3)
	if idx[0] > idx[1]:
		dark_pixel = original_image[center_row,center_col+1]
		light_pixel = original_image[center_row,center_col-1]
	else:
		dark_pixel = original_image[center_row,center_col-1]
		light_pixel = original_image[center_row,center_col+1]
	alpha = (center_pixel - light_pixel) / (dark_pixel - light_pixel)

	no_alpha = np.isinf(alpha)
	high_value = alpha > 1
	if (True in no_alpha) or (True in high_value):
		return center_pixel
	else:
		alpha[ np.isnan(alpha) ] = 0
		dist_from_1 = np.linalg.norm(full_alpha - alpha)
		if dist_from_1 > 0:
			return (full_alpha * dark_pixel) + (1 - full_alpha) * light_pixel
		else:
			return center_pixel
		

def eliminate_mid_transparencies(image,alpha_mask):
	alpha_mask[ alpha_mask == 1 ] = 0
	alpha_mask[ alpha_mask > 0 ] = 255
	image[:,:,3] = alpha_mask
	return image