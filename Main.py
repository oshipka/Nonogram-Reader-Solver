from PIL import ImageGrab

import Reader

if __name__ == '__main__':
	im = ImageGrab.grabclipboard()
	im.show()
	im.save('Results/pulled.png','PNG')
	
	rows, columns = Reader.get_info_segments(im)
	
