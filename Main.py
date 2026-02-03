import turtle
import tkinter as tk
import time
import random
import math
import csv

#This is the cursor turtle used for selecting actions.
global global_cursor
global_cursor = None

#This keeps track of the correct action.
global global_index
global_index = 0
global cursor_row 
cursor_row = 0
global cursor_col
cursor_col = 0 
distance = 20

global camera_row
camera_row = 0
global camera_col
camera_col = 0

TILE_SIZE = 100
tile_map = []
map_rows = 0
map_cols = 0

GRID_ORIGIN_X = -200
GRID_ORIGIN_Y = 200
SCREEN_CENTER_X = 0
SCREEN_CENTER_Y = 0
global pen
pen = None

TILE_COLORS = {
    0: "lightgray",   # floor
    1: "dimgray",     # wall
    2: "royalblue"    # water
}

#Class for the hero object. Probably could be made as a subclass of a larger character class.
class Hero:
	def __init__(self, name, hp, mp, st, int, speed, lck, items):
		#Attributes are lifted from standard JRPGS, such as name, health, magic, strength, int, speed, luck, and items.
		self.name = name
		self.hp = hp
		self.mp = mp
		self.st = st
		self.int = int
		self.speed = speed
		self.lck = lck
		self.items = items

	#This function subtracts HP from the Hero by the defined amount.
	def damage(self, amount):
		self.hp = self.hp - amount
	
	#This function returns the hero's name.
	def get_name(self):
		return self.name
	
	#This function returns the hp of the hero.
	def get_hp(self):
		return self.hp
	
	#This function returns the mp of the hero.
	def get_mp(self):
		return self.mp
	
	#This function returns the st of the hero.
	def get_st(self):
		return self.st
	
	#This function returns the int of the hero.
	def get_int(self):
		return self.int
	
	#This function returns the speed of the hero.
	def get_speed(self):
		return self.speed
	
	#This function returns the luck of the hero.
	def get_lck(self):
		return self.lck
	
	#This function returns the items of the hero.
	def get_items(self):
		return self.items

#This is the monster version of the hero class. All attributes and functions are the same.
class Monster:
	def __init__(self, name, hp, mp, st, int, lck, speed):
		self.name = name
		self.hp = hp
		self.mp = mp
		self.st = st
		self.int = int
		self.speed = speed
		self.lck = lck

	def damage(self, amount):
		self.hp = self.hp - amount
	
	def get_name(self):
		return self.name
	
	def get_hp(self):
		return self.hp
	
	def get_mp(self):
		return self.mp
	
	def get_st(self):
		return self.st
	
	def get_int(self):
		return self.int
	
	def get_speed(self):
		return self.speed
	
	def get_lck(self):
		return self.lck
	
#This function checks if the window is still active.
def window_active(window):
	try:
		#If we can update, we return true.
		window.update()
		return True
	except(turtle.Terminator, tk.TclError):
		#Otherwise, we return false.
		return False
	

def get_tile(row, col):
	global tile_map
	tile_row = tile_map[row]
	tile_col = tile_row[col]
	print(tile_col)
	return tile_col
	
#This function moves the turtle down, while checking the bounds of the turtle.
def move_up():
	global camera_row
	global camera_col
	global global_cursor
	if camera_row == 0:
		global_cursor.setheading(90)
		turtle.update()
		return
	tile = get_tile(camera_row - 1,camera_col)
	if tile == 1:
		global_cursor.setheading(90)
		turtle.update()
		return
	camera_row -= 1
	draw_grid()
	global_cursor.setheading(90)
	turtle.update()
	

def move_down():
	global camera_row
	global camera_col
	global global_cursor
	if camera_row >= (map_rows - 1):
		global_cursor.setheading(270)
		turtle.update()
		return
	tile = get_tile(camera_row + 1, camera_col)
	if tile == 1:
		global_cursor.setheading(270)
		turtle.update()
		return
	camera_row += 1
	draw_grid()
	global_cursor.setheading(270)
	turtle.update()

def move_left():
	global camera_row
	global camera_col
	global global_cursor
	if camera_col == 0:
		global_cursor.setheading(180)
		turtle.update()
		return
	tile = get_tile(camera_row, camera_col - 1)
	if tile == 1:
		global_cursor.setheading(180)
		turtle.update()
		return
	camera_col -= 1
	draw_grid()
	global_cursor.setheading(180)
	turtle.update()

def move_right():
	global camera_row
	global camera_col
	global global_cursor
	if camera_col >= (map_cols - 1):
		global_cursor.setheading(0)
		turtle.update()
		return
	tile = get_tile(camera_row, camera_col + 1)
	if tile == 1:
		global_cursor.setheading(0)
		turtle.update()
		return
	camera_col += 1
	draw_grid()
	global_cursor.setheading(0)
	turtle.update()

def load_map(filename):
    global tile_map, map_rows, map_cols

    tile_map = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tile_map.append([int(cell) for cell in row])

    map_rows = len(tile_map)
    map_cols = len(tile_map[0])

#This function gets the return value and sets it into the combat return variable.
def enter():
	print("Player hit enter!")
	return

#This function creates a turtle and adds some formatting to save lines of code.
def create_turtle(window, shape):
	local_turtle = turtle.Turtle()
	local_turtle.penup()
	local_turtle.goto(0,0)
	window.addshape(shape)
	local_turtle.shape(shape)
	return local_turtle

#This function simulates the attack action between the hero and a monster.
def attack(hero, enemy, attacker, defense):
	#If the attack is initiated by the player, the attacker variable should read "p"
	if attacker == "p":
		#We get the enemy's hp.
		starting_hp = enemy.get_hp()
		#We get the hero and the monster's strength.
		st = hero.get_st()
		df = enemy.get_st()
		if defense == True:
			#If the monster is defending, we multiply the monster's defense by 2.
			df = df *2
		#We roll random numbers based on the strength to determine final damage.
		st = random.randint(0,st)
		df = random.randint(0,df)
		df = math.ceil(df /2)
		if(st - df < 0):
			#We can do no less than 0 damage.
			st = 0
		else:
			st = st - df
		#Enemy takes damage by the final value.
		enemy.damage(st)
		ending_hp = enemy.get_hp()
		damage = abs(ending_hp - starting_hp)
		#We return the amount of damage the enemy took.
		return damage 
	#This function repeats if the attacker if the enemy, but with the roles swapped.
	if attacker == "e":
		starting_hp = hero.get_hp()
		st = enemy.get_st()
		df = hero.get_st()
		st = random.randint(0,st)
		df = random.randint(0,df)
		df = math.ceil(df /2)
		if(st - df < 0):
			st = 0
		else:
			st = st - df
		hero.damage(st)
		ending_hp = hero.get_hp()
		damage = abs(ending_hp - starting_hp)
		return damage
	
def draw_grid():
    global pen
    pen.clear()
    for row in range(map_rows):
        for col in range(map_cols):
            tile_value = tile_map[row][col]
            color = TILE_COLORS.get(tile_value, "pink")  # fallback

            x, y = tile_to_screen(row, col)

            pen.goto(x - TILE_SIZE / 2, y + TILE_SIZE / 2)
            pen.fillcolor(color)
            pen.pencolor("black")
            pen.pendown()
            pen.begin_fill()

            for _ in range(4):
                pen.forward(TILE_SIZE)
                pen.right(90)

            pen.end_fill()
            pen.penup()

def tile_to_screen(row, col):
    dx = (col - camera_col) * TILE_SIZE
    dy = (camera_row - row) * TILE_SIZE
    return SCREEN_CENTER_X + dx, SCREEN_CENTER_Y + dy

#This is the main function where the combat logic happens.
def main():
	#We initalise the global variables.
	global global_cursor
	global pen
	game_font = "PressStart2P"
	load_map("map.csv")
	#We create the window for the game screen.
	window = turtle.Screen()
	window.setup(600,600)
	window.title("Combat Window")
	window.tracer(0)
	local_pen = turtle.Turtle()
	local_pen.hideturtle()
	local_pen.speed(0)
	local_pen.penup()
	pen = local_pen
	draw_grid()
	window.update()
	#We create the cursor turtle.
	cursor = turtle.Turtle()
	cursor.penup()
	
	global_cursor = cursor
	global cursor_row, cursor_col
	cursor_row = 0
	cursor_col = 0
	x, y = tile_to_screen(camera_row, camera_col)
	cursor.goto(x, y)
	#We move the cursor to the starting combat position.
	#move(cursor, global_index, COMBAT_POSITIONS)
	#We set the combat_return to e.
	combat_return = "e"
	#We create the update turtle.
	update_turtle = turtle.Turtle()
	update_turtle.penup()
	update_turtle.hideturtle()
	update_turtle.goto(100, -100)
	#We create a hero and a monster object.
	main_hero = Hero("Yusha",15,10,5,4,5,10,"Sword")
	#We set the window to react to up and down inputs.
	window.listen()
	window.onkey(move_up, "Up")
	window.onkey(move_down, "Down")
	window.onkey(move_right,"Right")
	window.onkey(move_left, "Left")
	window.onkey(enter, "Return")
	#We set it so the hero and monster are not defending by default.
	#We loop input on the window.
	while window_active(window):
		time.sleep(0.001)

	#We attampt to gracefully close the window.
	try:
		window.bye()
	except Exception:
		pass
	
	
#This is the main function.
main()

