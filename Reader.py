import time
import sys
import numpy as np
import cv2


# rows - information about horizontal lines
# columns - information about vertical lines

def get_info_segments_bw(width, height):
	rows_img, columns_img = crop_numbers()
	rw_data = get_row_data(rows_img, height)
	cl_data = get_column_data(columns_img, width)

	return 0, 0


def crop_numbers():
	img = cv2.imread('Results/pulled.png')
	x = 15
	y = 10

	gr = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(gr)
	cv2.imshow('l_channel', l)
	cv2.imshow('a_channel', a)
	cv2.imshow('b_channel', b)

	# -----Applying CLAHE to L-channel-------------------------------------------
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
	cl = clahe.apply(l)
	cv2.imshow('CLAHE output', cl)

	# -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
	limg = cv2.merge((cl, a, b))
	cv2.imshow('limg', limg)

	# -----Converting image from LAB Color model to RGB model--------------------
	gr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	cv2.imshow('final', gr)

	colour = gr[x, y]
	while colour[0] > 70:
		x += 1
		colour = gr[x, y]

	lower_bound = x
	x -= 5
	colour = gr[x, y]
	while colour[0] > 70:
		y += 1
		colour = gr[x, y]

	right_bound = y
	height, width = img.shape[:2]
	# cropped = img[start_row:end_row, start_col:end_col]
	column_info = img[0:lower_bound, right_bound:width]
	row_info = img[lower_bound:height, 0:right_bound]
	cv2.imwrite('Results/columns.png', column_info)
	cv2.imwrite('Results/rows.png', row_info)
	return row_info, column_info


# data is pulled from each row
# mowing top-to-bottom
# and right-to-left
# resulting list has all numbers mirrored horizontally
def get_row_data(rows_img, number_of_rows):
	height, width = rows_img.shape[:2]
	square_side_len = height / number_of_rows
	max_cells = width / square_side_len
	rows = []
	for i in range(1, number_of_rows):
		start_rw = int((i - 1) * square_side_len)
		end_rw = int(i * square_side_len)
		current_row = rows_img[start_rw:end_rw, 0:width]
		# cv2.imshow('row '+ str(i), current_row)
		new_row = []
		for j in range(1, int(max_cells)):
			start_col = width - int(j * square_side_len)
			end_col = width - int((j - 1) * square_side_len)
			current_cell = current_row[0:int(square_side_len), start_col:end_col]
			number = get_number_from_cell(current_cell)
			if number is not None:
				new_row.append(number)
			else:
				continue
		# cv2.imshow('cell ' + str(i)+ str(j), current_cell)

		rows.append(new_row)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	pass


def get_column_data(columns_img, number_of_columns):
	pass


def get_number_from_cell(cell_img):



	return None

def getdatafile():
	im = cv2.imread('Results/pulled.png')
	im3 = im.copy()

	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

	#################      Now finding Contours         ###################

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	samples = np.empty((0, 100))
	responses = []
	keys = [i for i in range(48, 58)]

	for cnt in contours:
		if cv2.contourArea(cnt) > 50:
			[x, y, w, h] = cv2.boundingRect(cnt)

			if h > 28:
				cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
				roi = thresh[y:y + h, x:x + w]
				roismall = cv2.resize(roi, (10, 10))
				cv2.imshow('norm', im)
				key = cv2.waitKey(0)

				if key == 27:  # (escape to quit)
					sys.exit()
				elif key in keys:
					responses.append(int(chr(key)))
					sample = roismall.reshape((1, 100))
					samples = np.append(samples, sample, 0)

	responses = np.array(responses, np.float32)
	responses = responses.reshape((responses.size, 1))
	print("training complete")

	np.savetxt('generalsamples.data', samples)
	np.savetxt('generalresponses.data', responses)



def get_info_segments_coloured(width, height):
	return None
