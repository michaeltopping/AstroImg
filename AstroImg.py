import numpy as np
import pyfits
import math
import pylab as plt
import time

#class for an image that will be imported
#takes arguments:
#  > filename:  location of the file to be imported
#  > channel:   color channel for the image.  Default is luminosity.
#  > imagetype: type of image.  e.g. light, dark, flat, bias...
class FitsImage():

	def __init__(self, filename,  imagetype, channel):
	
		#read in the file	
		print "Reading in data"
		self.data = pyfits.getdata(filename)
		
		
class PlotImage(object):

	def __init__(self, figure, image):
		self.image = image
		self.fig = figure

	def figConnect(self):
		self.cidButtonPress  = self.fig.patch.figure.canvas.mpl_connect('key_press_event', self.keyPress)
		print "Connected"
		
	def keyPress(self, event):
		if event.key == '1':
			print "1 key pressed"
		
		
		
class MovableColorbar(object):
	
	def __init__(self, cBar, image):
		self.cBar = cBar
		self.press = None
		self.sceme = 'gray'
		self.range = [0, 10000]
		self.image = image
		self.cBar.norm.vmin, self.cBar.norm.vmax = self.range
		self.cBar.draw_all()
		self.image.set_norm(self.cBar.norm)
		self.cBar.patch.figure.canvas.draw()
		
		
	def figConnect(self):
		#connect the mouse clicks to the image
		self.cidMouseClick = self.cBar.patch.figure.canvas.mpl_connect('button_press_event', self.buttonPress)
		self.cidButtonPress = self.cBar.patch.figure.canvas.mpl_connect('key_press_event', self.keyPress)
		
	def buttonPress(self, event):
		if event.inaxes == self.cBar.ax:
			if event.button==1:
				self.press = event.xdata, event.ydata
				newmax = self.range[0] + (self.range[1]-self.range[0])*event.ydata
				self.range[1] = newmax
				self.cBar.norm.vmax = newmax
				self.cBar.draw_all()
				self.image.set_norm(self.cBar.norm)
				self.cBar.patch.figure.canvas.draw()
			if event.button==3:
				self.press = event.xdata, event.ydata
				newmin = self.range[0] + (self.range[1]-self.range[0])*event.ydata
				self.range[0] = newmin
				self.cBar.norm.vmin = newmin
				self.cBar.draw_all()
				self.image.set_norm(self.cBar.norm)
				self.cBar.patch.figure.canvas.draw()	
				
	def keyPress(self, event):
		if event.key == 'backspace':
			if self.cBar.norm.vmin < 1000:
				self.cBar.norm.vmin = 0
			else:
				self.cBar.norm.vmin -=1000
			self.cBar.norm.vmax +=1000
			self.cBar.draw_all()
			self.image.set_norm(self.cBar.norm)
			self.cBar.patch.figure.canvas.draw()

	def disconnect(self):
		#disconnect the keyboard from the plot
		self.cBar.patch.figure.canvas.mpl_disconnect(self.cidMouseClick)





if __name__ == "__main__":
	
	figure = plt.figure()

	imageR = FitsImage("testImages/M33/M33_600s_R_3.fit", "light", "R")
	
	image = plt.imshow(imageR.data, cmap = plt.cm.gray)
	print image
	cbar = plt.colorbar(format='%05.2f')
	
	mainImage = PlotImage(figure, image)
	mainImage.figConnect()
	
	cbar = MovableColorbar(cbar,image)
	cbar.figConnect()
	

	plt.show()

	
	