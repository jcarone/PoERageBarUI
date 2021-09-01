import time
import sys
import cv2
import mss
import numpy
import pytesseract
import re
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

mon = {'top': 830, 'left': 1818, 'width': 68, 'height': 32}
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
	
previousRageValue = -1
maxRage = 90
	
with mss.mss() as sct:	
	class Window(QMainWindow):
		def __init__(self):
			super().__init__()
			self.setWindowFlag(Qt.FramelessWindowHint)
			self.setWindowFlag(Qt.WindowStaysOnTopHint)
			self.setWindowTitle("")
			self.setGeometry(800, 340, 10, 200)
			self.show()
												
			layout = QGridLayout()
			
			widgets = [ RageBarWidget  ]
			for w in widgets:
				layout.addWidget(w())
				
			layout.setContentsMargins(0,0,0,0)	
			widget = QWidget()
			widget.setLayout(layout)
			self.setCentralWidget(widget)
			
		def mousePressEvent(self, QMouseEvent):
			if QMouseEvent.button() == Qt.RightButton:
				print("Right Button Clicked")

	class SoulGainTimerWidget(QWidget):
		def __init__(self):
			super().__init__()
			self.text = QLabel(self)
			self.text.setGeometry(0, 0, 10, 50)
			#self.text.setText("<font color=black>0.6</font>")
			labelText = "<div><font color='#ff0000' size=9>.6</font></div>";
			self.text.setText(labelText)

			self.layout = QVBoxLayout(self)
			self.layout.addWidget(self.text)
			self.layout.setContentsMargins(0,0,0,0)	
			self.setLayout(self.layout)
			
			#setup the timer to update the UI every 100ms
			self.timer = QTimer()
			self.timer.timeout.connect(self.Tick)
			self.timer.start(50)
		
		def Tick(self):
			labelText = "<div><font color='#ff0000' size=9>.4</font></div>";
			self.text.setText(labelText)
			
	class QProgressBar2(QProgressBar):
		def __init__(self):
			super(QProgressBar2, self).__init__()
	
		def paintEvent(self, event):
			super().paintEvent(event)
			#add a tick mark for where the 25 rage threshold is
			painter = QtGui.QPainter()
			painter.begin(self)
			painter.setPen(Qt.black)
			painter.drawLine(0,145,25,145)
			painter.end() 		
			
	class RageBarWidget(QWidget):
		def __init__(self):
			super().__init__()
			self.layout = QVBoxLayout(self)

			self.bar = QProgressBar2()
			self.bar.setGeometry(0, 0, 10, 200)
			self.bar.setMaximum(maxRage)
			self.bar.setMinimum(0)
			self.bar.setOrientation(QtCore.Qt.Vertical)
			self.bar.setFormat("")
			self.bar.setStyleSheet("""
			 QProgressBar::chunk {
				 background-color: #a83232;
				 height: 1px;
			 } """)
			self.layout.addWidget(self.bar)
			self.layout.setContentsMargins(0,0,0,0)	
			self.setLayout(self.layout)
			
			#setup the timer to update the UI every 17ms
			self.timer = QTimer()
			self.timer.timeout.connect(self.Tick)
			self.timer.start(17)	
			
		def Tick(self):
			global previousRageValue
		
			im = numpy.asarray(sct.grab(mon))
			text = pytesseract.image_to_string(im)
			#print(text)
			parsedRage = re.findall(r'\d+', text)
			
			
			if len(parsedRage) == 2 and int(parsedRage[1]) == int(maxRage):		
		
				print(text)
		
				noPreviousValue = previousRageValue == -1 
				gainedRage = int(parsedRage[0]) > 84
				previousAboveTwenty = int(previousRageValue) > 20
				droppedDigit = len(str(previousRageValue)) == 2 and str(previousRageValue)[0] == str(parsedRage)[0]
				#brokenParse = previousAboveTwenty and (int(parsedRage[0]) < 10)
				brokenParse = previousAboveTwenty and droppedDigit
		
				#keep track of the most recent reading, sometimes the parsing messes up and goes 30, 30, 3, 30
				if noPreviousValue or gainedRage or not brokenParse:
					previousRageValue = parsedRage[0]
					progress = float(parsedRage[0]) / float(parsedRage[1]) * 100.0
					print(int(progress))
					self.bar.setValue(int(parsedRage[0]))
					QApplication.processEvents()

	# create pyqt5 app
	App = QApplication(sys.argv)
	App.setStyle('windowsvista')
	
	# create the instance of our Window
	window = Window()

	# start the app
	sys.exit(App.exec())