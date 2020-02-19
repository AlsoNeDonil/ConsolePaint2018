from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.core.window import Window

import msvcrt
import threading
import sys
import win32clipboard
import win32con
import write
import time
import os

width = int(sys.argv[1]) # get width 
height = int(sys.argv[2])# get height

Window.size = (width * 50, height* 50) # set window size

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', width*100)
Config.set('graphics', 'height', height*100) # also set window size and other parameters


image = []

def init_image(img): # genering array for keep data of image. On this step image is empty and consisted only gaps

	for i in range(height):
		img.append([])
		for j in range(width):
			img[i].append(0)
	return img

image = init_image(image)
		

class PaintForConsoleApp(App): # init class of application
	image_save = ''

	def get_image(self):

		for i in range(height):
			for j in range(width):
				if image[i][j] == 1:
					self.image_save += 'x'
				elif image[i][j] == 0:
					self.image_save += ' '
			self.image_save += '\n' # cycle for get image from image array
		return self.image_save

	def save(self, instance):

		self.image_save = self.get_image()

		file = open('img.txt', 'w')
		file.write(self.image_save) # write image in file
		self.image_save = '' # doing image empty for using in future
		file.close() 

	def copy(self, instance): # function for copy image in clipboard

		self.get_image()

		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, self.image_save)
		win32clipboard.CloseClipboard()

	def delete(self, instance):

		os.system('cls')
		for i in range(len(image)):
			for j in range(len(image[i])):
				image[i][j] = 0
		#self.background_color = (1,1,1,1)
			
		self.get_image()

		a = 1/0

	def get_position(self, instance): # function for get position of pressed button

		row = int(int(instance.id)/width) 
		col = int(int(instance.id)%height) 

		return row, col

	def press_func(self, instance): # function for button activity

		if instance.id[len(instance.id)-1] == 'o':

			instance.id =  instance.id.replace('o', '')
			row, col = self.get_position(instance)
			image[row][col] = 1
			instance.background_color = (0,0,0,1)
			instance.text = 'x'
			 #when button pressed


		else:

			row, col = self.get_position(instance)
			image[row][col] = 0
			instance.id += 'o'
			instance.background_color = (1,1,1,1)
			instance.text = 'o' #when button don't pressed
		os.system('cls')
		s = write.image(image)
		sys.stdout.write("\r%s" % s)
		sys.stdout.flush()

	def build(self): # render 
		#init layouts
		main = BoxLayout(orientation = 'vertical')
		ButtonRow = GridLayout(rows = 1, size_hint = (1, .05))
		gl = GridLayout(cols = width, spacing = 0)
		#add buttons on layout
		for i in range(width*height):
			gl.add_widget(Button(text = 'o', on_press = self.press_func, size_hint = (.01,.01), id = str(i) + ' o', background_color = (1, 1, 1, 1)))
		#create buttons
		saveButton = Button(text = 'save', on_press = self.save,)
		copyButton = Button(text = 'copy', on_press = self.copy,)
		delButton  = Button(text = 'delete', on_press = self.delete, )
		#add buttons on layout
		ButtonRow.add_widget(saveButton)
		ButtonRow.add_widget(copyButton)
		ButtonRow.add_widget(delButton)
		#add layouts on main layout
		main.add_widget(ButtonRow)
		main.add_widget(gl)
			
		return main
if __name__ == "__main__":
	os.system('cls')
	while True:
		try:
			PaintForConsoleApp().run()
		except ZeroDivisionError:
			print('Deleted') # start application
