import pygame as pg
from sys import exit
from Funciones import initializeParameters,checkButtonContact,updateMainScreen

param_tup = initializeParameters()
screen,buttons,array_to_sort = param_tup[0],param_tup[1],param_tup[2]

while 1:
	for event in pg.event.get():
		if event.type == pg.QUIT: exit()
		elif event.type == pg.MOUSEBUTTONUP:
			checkButtonContact(pg.mouse.get_pos(),buttons,array_to_sort,screen)

	updateMainScreen(screen)