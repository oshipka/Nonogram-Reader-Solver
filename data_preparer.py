import math

import cv2

READ_DIR = "data/_/"
WRITE_DIR = "data/_unsorted/"
SIZE = 15
NUM_PREFIX = "7_"
AVG_OF_EMPTY_CELL = -1
NAME_PREFIX = "test_recog_1_"


def calculate_average(image):
	h, w = image.shape[:2]
	total = h * w
	val = 0
	for i in range(0, h):
		for j in range(0, w):
			colour = image[i, j]
			
			val += colour
	
	average = val / total
	return average


if __name__ == '__main__':
	filename = NAME_PREFIX + str(SIZE) + ".png"
	img = cv2.imread(READ_DIR + filename)
	h, w = img.shape[:2]
	square_side_not_rounded = h / SIZE
	max_cells = w / square_side_not_rounded
	
	gr = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(gr)
	#cv2.imshow('l_channel', l)
	#cv2.imshow('a_channel', a)
	#cv2.imshow('b_channel', b)
	
	# -----Applying CLAHE to L-channel-------------------------------------------
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
	cl = clahe.apply(l)
	#cv2.imshow('CLAHE output', cl)
	
	# -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
	limg = cv2.merge((cl, a, b))
	#cv2.imshow('limg', limg)
	
	# -----Converting image from LAB Color model to RGB model--------------------
	gr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	gr = cv2.cvtColor(gr, cv2.COLOR_BGR2GRAY)
	#cv2.imshow('final', gr)
	img = gr
	
	avgs =[]
	
	for row_num in range(1, SIZE+1):
		start_rw = int((row_num - 1) * square_side_not_rounded)
		end_rw = int(row_num * square_side_not_rounded)
		# cv2.imshow('row '+ str(i), current_row)
		new_row = []
		# cv2.line(img, (0, end_rw), (w, end_rw), (0, 0, 255), 1)
		for col_num in range(1, int(max_cells + 1)):
			start_col = w - int(col_num * square_side_not_rounded)
			end_col = w - int((col_num - 1) * square_side_not_rounded)
			current_cell = img[start_rw:end_rw, start_col:end_col]
			# cv2.line(img, (start_col, 0), (start_col, h), (0, 0, 255), 1)
			avg = calculate_average(current_cell);
			if avg < 200 :
				cv2.imwrite(WRITE_DIR + NUM_PREFIX +str(row_num)+"_"+str(col_num)+".png", current_cell)
	
	cv2.imshow("01", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


