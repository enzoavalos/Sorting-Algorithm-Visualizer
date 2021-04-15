from Clases import *
import pygame as pg
from pygame.locals import *
from time import time,sleep

def welcomeMessage(screen):
	"""
	Muestra un mensaje en la pantalla principal
	"""
	fuente = pg.font.SysFont("Comic Sans MS",26)
	fuente.set_underline(True)
	fuente.set_bold(True)
	text = fuente.render("Bienvenido! Elija un ordenamiento para visualizarlo",True,(0,180,0))
	required_size = text.get_rect()
	screen.blit(text,(400-(required_size[2]/2) ,45-(required_size[3]/2)))

def drawLines(screen,array_to_sort):
	"""
	Grafica las lineas correspondientes a los valores del arreglo a ordenar
	"""
	starting_pos = 40
	for values in array_to_sort.values:
		red_color = (1.5 * values)
		pg.draw.line(screen,(red_color,0,0),(starting_pos,260),(starting_pos,260-values),6)
		starting_pos += 6

def initializeParameters():
	"""
	Instancia e inicializa objetos necesarios de las distintas clases
	"""
	global global_params
	background_img = pg.transform.scale(pg.image.load("Background.png"),(800,450))

	pg.init()
	flags,window_size = DOUBLEBUF,(800,450)
	screen = pg.display.set_mode(window_size,flags)
	screen.set_alpha(None)
	pg.display.set_caption("Visualizador de Ordenamientos")

	pg.event.set_blocked(None)
	pg.event.set_allowed(pg.QUIT)
	pg.event.set_allowed(pg.MOUSEMOTION)
	pg.event.set_allowed(pg.MOUSEBUTTONUP)

	new_array,new_buttons = Arreglo(),Botones()
	global_params = (screen,new_buttons,new_array,background_img,)
	return global_params

def updateMainScreen(screen,portion=None):
	"""
	Actualiza todos los elementos de la pantalla
	"""
	global global_params
	
	screen = global_params[0]
	buttons = global_params[1]
	array_to_sort = global_params[2]
	bg_img = global_params[3]

	if portion != None:
		screen_portion = pg.Rect(35,95,735,170)
		screen.blit(bg_img,(0,0))
		drawLines(screen,array_to_sort)
		pg.display.update(screen_portion)
	else:
		screen.blit(bg_img,(0,0))
		drawLines(screen,array_to_sort)
		buttons.displayButtons(screen,array_to_sort)
		welcomeMessage(screen)
		if array_to_sort.status != "scrambled":
			array_to_sort.showSortingTime(screen)
		pg.display.update()

def buttonCommands(array_to_sort,screen,number):
	"""
	Contiene los comandos asignados a cada uno de los botones
	"""
	command_list = {
		0:lambda:array_to_sort.scrambleValues(),
		1:lambda:radixSort(array_to_sort,screen),
		2:lambda:mergeSort(array_to_sort,screen,0,len(array_to_sort.values)-1),
		3:lambda:quickSort(array_to_sort,screen,0,len(array_to_sort.values)-1),
		4:lambda:shellSort(array_to_sort,screen,len(array_to_sort.values)-1),
		5:lambda:timSort(array_to_sort,screen),
		6:lambda:heapSort(array_to_sort,screen),
		7:lambda:array_to_sort.visualizeAlgorithms(),
		8:lambda:array_to_sort.changeExecutionSpeed("Slow"),
		9:lambda:array_to_sort.changeExecutionSpeed("Fast"),
	}

	if number in (0,7,8,9):
		func_temp = command_list.get(number)
		func_temp()
	elif array_to_sort.status != "Sorted":
		func_temp = command_list.get(number)
		array_to_sort.duration = time()
		func_temp()
		trackTime(array_to_sort)

def checkButtonContact(mouse_pos,buttons,array_to_sort,screen):
	"""
	Verifica si el cursor se encuentra en contacto con alguno de los botones
	"""
	mouse_pos = pg.Rect(mouse_pos[0]-1,mouse_pos[1]-1,2,2)

	if buttons.positions[0] != None:
		for i in range(10):
			button_rect = buttons.positions.get(i)
			if mouse_pos.colliderect(button_rect): buttonCommands(array_to_sort,screen,i)

def trackTime(array_to_sort):
	end_time = time()
	total_time = end_time - array_to_sort.duration
	array_to_sort.duration = round(total_time,4)
		

"""--------------------------------------------------------------------
						Ordenamientos
	-------------------------------------------------------------------
"""
def quickSort(array_to_sort,screen,start,end):
	"""
	Se elige un valor como pivot, en este caso el ultimo, y se ordena el resto del arreglo, ubicando el mismo en su posicion
	correspondiente y ubicando a su izquierda todos los valores menores a el, y a su derecha los mayores. Luego se ordena de forma
	recursiva los valores a su izquierda y a su derecha, hasta que el subarray tenga longitud 1 o menor.
	"""
	if start >= end:
		if start >= len(array_to_sort.values)-1:
			array_to_sort.status = "Sorted"
		return

	pivot_index = start
	pivot_value = array_to_sort.values[end]
	i = start
	while i < end:
		if array_to_sort.values[i] < pivot_value:
			array_to_sort.values[pivot_index],array_to_sort.values[i] = array_to_sort.values[i],array_to_sort.values[pivot_index]
			sleep(array_to_sort.exe_speed[array_to_sort.cur_speed])
			if array_to_sort.visualize: updateMainScreen(screen,1)
			pivot_index += 1
		i += 1
	array_to_sort.values[pivot_index],array_to_sort.values[end] = array_to_sort.values[end],array_to_sort.values[pivot_index]
	if array_to_sort.visualize: updateMainScreen(screen,1)

	quickSort(array_to_sort,screen,start,pivot_index-1)
	quickSort(array_to_sort,screen,pivot_index+1,end)



def merge(array,left,right):
	"""
	Funcion auxiliar para el metodo mergeSort, recibe 2 listas correspondientes a particion del arreglo a ordenar, y las une en una
	sola lista ordenada
	"""
	merged_list = []
	i = j = 0
	while i < len(left) and j < len(right):
		if left[i] < right[j]:
			merged_list.append(left[i])
			del left[0]
		elif left[i] > right[j]:
			merged_list.append(right[j])
			del right[0]

	if len(left) == 0:
		for k in right:
			merged_list.append(k)
	else:
		for k in left:
			merged_list.append(k)

	return merged_list

def mergeSort(array_to_sort,screen,start,end):
	"""
	Se subdivide el array de forma recursiva en dos mitades iguales o de longitud n y n-1. Al llegar a una sublista de longitud 1 o 0
	se considera que ya esta ordenada. Luego se ordena cada sublista recursivamente utilizando la funcion merge
	"""
	sub_array = []

	if start == end:
		if start == len(array_to_sort.values)-1:
			array_to_sort.status = "Sorted"
		sub_array.append(array_to_sort.values[start])
		return sub_array

	half = (start + end)//2
	left_list = mergeSort(array_to_sort,screen,start,half)
	right_list = mergeSort(array_to_sort,screen,half+1,end)
	merged_list = merge(array_to_sort,left_list,right_list)

	i = start
	j = 0
	while i <= end:
		sleep(array_to_sort.exe_speed[array_to_sort.cur_speed])
		if array_to_sort.visualize: updateMainScreen(screen,1)
		array_to_sort.values[i] = merged_list[j]
		i+=1
		j+=1

	return merged_list



def radixSort(array_to_sort,screen,current_digit=1):
	"""
	Ordenamiento radixSort LSD(least significative digit). Se analiza de forma recursiva cada digito de los valores del arreglo,
	empezando desde el ultimo y se los almacena en casillas segun estos. Al trabajar con enteros, tendremos 10 casilleros, cada uno
	para un digito en particular.
	"""
	sorted_array = [[],[],[],[],[],[],[],[],[],[]]
	if current_digit > len(str(max(array_to_sort.values))):
		array_to_sort.status = "Sorted"
		return

	for i in array_to_sort.values:
		number = str(i)
		index = len(number) - current_digit
		sub_list = int(number[index])
		sorted_array[sub_list].append(i) if index >= 0 else sorted_array[0].append(i)
	
	k = 0
	for j in sorted_array:
		for x in j:
			array_to_sort.values[k] = x
			sleep(array_to_sort.exe_speed[array_to_sort.cur_speed])
			if array_to_sort.visualize: updateMainScreen(screen,1)
			k += 1
	radixSort(array_to_sort,screen,current_digit+1)



def shellSort(array_to_sort,screen,step):
	"""
	Se toman los valores del arreglo y se los acomoda en filas de cierta longitud, paso siguiente se ordenan las columnas resultantes
	de dichas filas, y se vuelve a formar una lista a partir de las filas. Asi se ordena de forma recursiva el arreglo, con cada vez
	menos columnas pero de mayor longitud, y se repite hasta que la longitud sea 0.
	"""
	def localInsertionSort(array):
		index = len(array)-1

		for i in range(index):
			aux = array[i]
			j = i
			while j >= 0:
				if array[j] > array[j+1]:
					array[j],array[j+1] = array[j+1],array[j]
				j -= 1
		return array

	sub_lists = []
	sorted_list = []
	if step <= 0:
		array_to_sort.status = "Sorted"
		return

	#lo transformo en sublistas
	for i in range(step):
		j = i
		temp_list = []
		while j <= len(array_to_sort.values)-1:
			temp_list.append(array_to_sort.values[j])
			j += step
		sub_lists.append(temp_list)

	#ordena cada una usando insercion
	for k in sub_lists:
		sorted_list.append(localInsertionSort(k))

	j = i = 0
	while j < len(sorted_list[0]):
		for x in sorted_list:
			try:
				array_to_sort.values[i] = x[j]
				sleep(array_to_sort.exe_speed[array_to_sort.cur_speed])
				if array_to_sort.visualize: updateMainScreen(screen,1)
			except IndexError:
				pass
			i+=1
		j+=1
	shellSort(array_to_sort,screen,step//2)



def timSort(array_to_sort,screen):
	"""
	timSort utiliza ambos mergeSort como el ordenamiento de insercion para su funcionamiento. Se subdivide el arreglo en listas de
	tamaño 32 o 64, para una optimizacion de los ordenamientos. Cada sublista es ordenada mediante insercion, y luego son combinadas
	de a una utilizando la funcion merge del ordenamiento merge.
	"""
	def localInsertionSort(array,start,end):
		i = start
		while i < end:
			aux = array.values[i]
			j = i
			while j >= start:
				if array.values[j] > array.values[j+1]:
					if array_to_sort.visualize: updateMainScreen(screen,1)
					array.values[j],array.values[j+1] = array.values[j+1],array.values[j]
				j-=1
			i +=1

	def merge(array,left_start,left_end,right_start,right_end):
		merged_list = []
		i = left_start
		j = right_start

		while i <= left_end and j <= right_end:
			if array.values[i] < array.values[j]:
				merged_list.append(array.values[i])
				i += 1
			elif array.values[j] < array.values[i]:
				merged_list.append(array.values[j])
				j += 1

		if i >= left_end:
			while j <= right_end:
				merged_list.append(array.values[j])
				j += 1
		elif j >= right_end:
			while i <= left_end:
				merged_list.append(array.values[i])
				i += 1
		
		for x in merged_list:
			array.values[left_start] = x
			sleep(array_to_sort.exe_speed[array_to_sort.cur_speed])
			if array_to_sort.visualize: updateMainScreen(screen,1)
			left_start += 1

	run = 32
	start = 0
	end = len(array_to_sort.values)-1
	current_pos = run - 1

	#Ordenamos el arreglo por insercion pero entre intervalos de 32 elementos
	while start <= end:
		localInsertionSort(array_to_sort,start,current_pos)
		start += run
		current_pos += run
		if current_pos > end:
			current_pos = end

	start = 0
	end = len(array_to_sort.values)-1
	current_pos = run - 1
	list_end = current_pos
	while current_pos < end:
		list_end += run
		if list_end > end:
			list_end = end
		merge(array_to_sort,0,current_pos,current_pos+1,list_end)
		current_pos += run

	array_to_sort.status = "Sorted"


def heapifyArray(array,parent,lenght,screen):
	"""
	Toma un arreglo y lo modifica a la forma de un max heap binario, teniendo un indice i y tomando a este como nodo padre o raiz, su hijo izquierdo estara
	en 2*i+1 y el derecho en el indice 2*i+2. Un max heap es aquel donde todos los nodos hijos de un nodo son iguales o menores a el
	"""
	biggest = array.values[parent]
	left_child = (parent*2)+1
	right_child = (parent*2)+2

	if left_child < lenght and array.values[left_child] > array.values[right_child]:
		if array.values[left_child] > biggest:
			array.values[left_child],array.values[parent] = array.values[parent],array.values[left_child]
			heapifyArray(array,left_child,lenght,screen)
			if array.visualize: updateMainScreen(screen,1)
	else:
		if right_child < lenght and array.values[right_child] > biggest:
			array.values[right_child],array.values[parent] = array.values[parent],array.values[right_child]
			heapifyArray(array,right_child,lenght,screen)
			if array.visualize: updateMainScreen(screen,1)
	
def buildHeap(array,lenght,screen):
	last_root = (lenght)//2
	while last_root >= 0:
		heapifyArray(array,last_root,lenght,screen)
		last_root -= 1

def extractRoot(array,lenght,screen):
	"""
	Extrae la raiz del heap, que por definicion sera siempre el elemento mas grande del arreglo
	"""
	last_leaf = lenght
	smallest_val = array.values[last_leaf]
	extracted_val = array.values[0]
	array.values[last_leaf] = extracted_val
	array.values[0] = smallest_val

	buildHeap(array,lenght-1,screen)

def alreadyOrdered(array):
	previous_val = array.values[0]
	for i in range(len(array.values)):
		if array.values[i] < previous_val:
			return False
		previous_val = array.values[i]
	return True

def heapSort(array_to_sort,screen):
	"""
	Consiste en almacenar todos los elementos del arreglo en un heap, aunque se puede implementar este como un arreglo y luego extraer el nodo raiz
	que se encuentra en la cima en sucesivas iteraciones para obtener el conjunto ordenado. Su funcionamiento se basa en la propiedad de los heaps de
	que la cima siempre contiene el menor o mayor elemento, segun su implementacion.
	"""
	buildHeap(array_to_sort,len(array_to_sort.values),screen)

	array_lenght = len(array_to_sort.values)-1
	while array_lenght >= 0 and not alreadyOrdered(array_to_sort):
		extractRoot(array_to_sort,array_lenght,screen)
		array_lenght -= 1
		sleep(array_to_sort.exe_speed[array_to_sort.cur_speed])

	array_to_sort.status = "Sorted"