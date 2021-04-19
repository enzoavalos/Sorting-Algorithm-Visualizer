from numpy import linspace
from random import shuffle
import pygame as pg

class Arreglo:
	def __init__(self):
		self.status = ""
		self.duration = 0
		self.exe_speed = {"Fast":0,"Slow":0.005}
		self.cur_speed = "Fast"
		self.visualize = True

		self.values = self.__generateValues()
		self.scrambleValues()

	def __generateValues(self):
		"""
		Generates an array of integer with values ranging between 40 and 160
		"""
		array = linspace(40,160,121)
		array = array.astype(int)
		return array

	def visualizeAlgorithms(self):
		self.visualize = False if self.visualize == True else True
		self.cur_speed = "Fast"

	def scrambleValues(self):
		"""
		Scrambles the elements of the array randomly
		"""
		shuffle(self.values)
		self.status,self.duration = "Scrambled",0

	def showSortingTime(self,screen):
		"""
		Show the execution time of the algorithm once this is done
		"""
		attribute_list =  ["Duration: {} seg.".format(self.duration,2),400,290]

		if self.status == "Sorted":
			fuente = pg.font.SysFont("Arial",18)
			text = fuente.render(attribute_list[0],True,(80,80,80))
			required_size = text.get_rect()
			screen.blit(text,(attribute_list[1]-(required_size[2]/2) ,attribute_list[2]-(required_size[3]/2)))
	
	def changeExecutionSpeed(self,new_speed):
		if self.visualize != False: self.cur_speed = new_speed

class Botones:
	def __init__(self):
		self.positions = {}

	def buttonSpecs(self,number):
		"""
		Returns the specifications of every button to draw
		"""
		attribute_list = {
			0:["Scramble",150,370],
			1:["Radix Sort(LSD)",650,370],
			2:["Merge Sort",400,370],
			3:["Quick Sort",160,415],
			4:["Shell Sort",320,415],
			5:["Tim Sort",480,415],
			6:["Heap Sort",640,415],
			7:["Visualize",200,320],
			8:["Slow",400,320],
			9:["Fast",600,320],
		}
		return attribute_list.get(number)

	def __isCursorOver(self,button_pos):
		mouse_pos = pg.mouse.get_pos()
		mouse_pos = pg.Rect(mouse_pos[0]-1,mouse_pos[1]-1,2,2)

		return True if button_pos.colliderect(mouse_pos) else False

	def displayButtons(self,screen,array_to_sort):
		"""
	Draws all the buttons in the main screen
		"""
		for i in range(10):
			attribute_list = self.buttonSpecs(i)
			fuente = pg.font.SysFont("MV Boli",22)
			text = fuente.render(attribute_list[0],True,(0,0,0))
			required_size = text.get_rect()
			button_rect = text.get_rect(center=(attribute_list[1],attribute_list[2]))

			if attribute_list[0] == "Visualize" and array_to_sort.visualize:
				pg.draw.line(screen,(0,0,255),(button_rect[0],button_rect[1]+button_rect[3]-5),\
					(button_rect[0]+button_rect[2],button_rect[1]+button_rect[3]-5),4)

			if attribute_list[0] == array_to_sort.cur_speed:
				pg.draw.line(screen,(0,128,0),(button_rect[0],button_rect[1]+button_rect[3]-5),\
					(button_rect[0]+button_rect[2],button_rect[1]+button_rect[3]-5),4)

			if self.__isCursorOver(button_rect):
				pg.draw.ellipse(screen,(255,0,0),(button_rect[0]-10,button_rect[1]-10,button_rect[2]+20,button_rect[3]+20),2)
				
			if self.positions.get(i) == None: self.positions[i] = button_rect

			screen.blit(text,(attribute_list[1]-(required_size[2]/2) ,attribute_list[2]-(required_size[3]/2)))