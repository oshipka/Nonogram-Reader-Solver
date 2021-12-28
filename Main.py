from PIL import ImageGrab

import Reader

WIDTH = 15
HEIGHT = 15

IS_BLACK_AND_WHITE = True

if __name__ == '__main__':
	im = ImageGrab.grabclipboard()
	#im.show()
	im.save('Results/pulled.png','PNG')
	Reader.getdatafile()
	if IS_BLACK_AND_WHITE:
		rows, columns = Reader.get_info_segments_bw(WIDTH, HEIGHT)
	else:
		rows, columns = Reader.get_info_segments_coloured(WIDTH, HEIGHT)
