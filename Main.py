import turtle
import tkinter as tk
import time
import random
import math

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

TILE_SIZE = 40
GRID_ROWS = 10
GRID_COLS = 10

GRID_ORIGIN_X = -200
GRID_ORIGIN_Y = 200

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
	

#This function moves the turtle up, while checking the bounds of the turtle.
def move_up():
	global global_cursor
	global_cursor.sety(global_cursor.ycor() + distance)
	global_cursor.setheading(90)


#This function moves the turtle down, while checking the bounds of the turtle.
def move_up():
    global cursor_row
    if cursor_row > 0:
        cursor_row -= 1
        x, y = tile_to_screen(cursor_row, cursor_col)
        global_cursor.goto(x, y)
        global_cursor.setheading(90)

def move_down():
    global cursor_row
    if cursor_row < GRID_ROWS - 1:
        cursor_row += 1
        x, y = tile_to_screen(cursor_row, cursor_col)
        global_cursor.goto(x, y)
        global_cursor.setheading(270)

def move_left():
    global cursor_col
    if cursor_col > 0:
        cursor_col -= 1
        x, y = tile_to_screen(cursor_row, cursor_col)
        global_cursor.goto(x, y)
        global_cursor.setheading(180)

def move_right():
    global cursor_col
    if cursor_col < GRID_COLS - 1:
        cursor_col += 1
        x, y = tile_to_screen(cursor_row, cursor_col)
        global_cursor.goto(x, y)
        global_cursor.setheading(0)

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
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = GRID_ORIGIN_X + col * TILE_SIZE
            y = GRID_ORIGIN_Y - row * TILE_SIZE

            pen.goto(x, y)
            pen.pendown()
            for _ in range(4):
                pen.forward(TILE_SIZE)
                pen.right(90)
            pen.penup()

def tile_to_screen(row, col):
    x = GRID_ORIGIN_X + col * TILE_SIZE + TILE_SIZE / 2
    y = GRID_ORIGIN_Y - row * TILE_SIZE - TILE_SIZE / 2
    return x, y

#This is the main function where the combat logic happens.
def main():
	#We initalise the global variables.
	global global_cursor
	game_font = "PressStart2P"
	#We create the window for the game screen.
	window = turtle.Screen()
	window.setup(600,600)
	window.title("Combat Window")
	draw_grid()
	#We create the cursor turtle.
	cursor = turtle.Turtle()
	cursor.penup()
	#We create turtles for text and the enemy model.
	#text_turtle= create_turtle(window, "Images/combat-text.gif")
	#text_turtle.teleport(-200,-200)
	#We get the location of the text turtle.
	#text_x = text_turtle.xcor()
	#text_y = text_turtle.ycor()
	#We create an array of combat positions based on the text turtle.
	#COMBAT_POSITIONS = [(text_x-70,text_y+33),(text_x-70, text_y+11.5),(text_x -70, text_y-11),(text_x-70,text_y-34)]
	global_cursor = cursor
	global cursor_row, cursor_col
	cursor_row = 0
	cursor_col = 0
	x, y = tile_to_screen(cursor_row, cursor_col)
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

