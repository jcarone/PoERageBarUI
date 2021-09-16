import time
import sys
import cv2
import mss
import numpy
import pytesseract
from PyQt5.QtWidgets import QApplication

#screen coordinates of the data we need
mon = {'top': 830, 'left': 1818, 'width': 68, 'height': 32}

#setup pytesseract so that we can call it here
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
	
with mss.mss() as sct:
	while True:
		#get the cropped screen shot and read it in the way tesseract needs
		im = numpy.asarray(sct.grab(mon))

		#let tesseract do the heavy lifting to get text from the image
		text = pytesseract.image_to_string(im)
		print(text)

		window_name = "image"
		cv2.imshow(window_name, im)
		cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

		# Press "q" to quit
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

		# One screenshot per second
		time.sleep(0.01)
		# time.sleep(1)