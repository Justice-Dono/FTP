import time
import turtle
import tkinter as tk
import random
import math
import csv
import sys
import os

#This is the cursor turtle used for selecting actions.
global global_cursor
global_cursor = None
#This is the main_hero used for combat and exploration.
global main_hero 
main_hero = None
#This is the cursor used in combat.
global combat_cursor
combat_cursor = None
#This is the array of positions used in combat, declared in the main() function.
global COMBAT_POSITIONS
COMBAT_POSITIONS = None
#This keeps track of the correct action.
global global_index
global_index = 0
#We create rows for the camera's row and column.
global camera_row
camera_row = 0
global camera_col
camera_col = 0
#This the the turtle for the enemy. Needed for the end combat function.
global enemy_turtle
enemy_turtle = None
#This is the turtle for text in combat.
global text_turtle 
text_turtle = None
#This is the turtle for combat updates. Currently does nothing, but functions correctly.
global update_turtle 
update_turtle = None
#This is the window for the game.
global game_window
game_window = None
#This tracks which floor the game is on.
global floor
floor = None
global hero_defense
hero_defense = False
global monster_defense
monster_defense = False

#Shows the maximum size of the tiles, and the map the tiles live in.
TILE_SIZE = 100
tile_map = []
map_rows = 0
map_cols = 0

#This creates the origin of the grid.
SCREEN_CENTER_X = 0
SCREEN_CENTER_Y = 0
global pen
pen = None

global STATE
STATE = None
#The set of tile colours, 0 for normal ground, 1 for walls, and 2 for water, 3 for map change.
TILE_COLORS = {
    0: "lightgray",  
    1: "dimgray",     
    2: "royalblue",
	3: "hotpink"  
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

	#This function deals damage to the monster.
	def damage(self, amount):
		self.hp = self.hp - amount
	
	#This function gets the name of the monster.
	def get_name(self):
		return self.name
	
	#This function gets the hp of the monster.
	def get_hp(self):
		return self.hp
	
	#This function gets the mp of the monster.
	def get_mp(self):
		return self.mp
	
	#This function gets the st of the monster.
	def get_st(self):
		return self.st
	
	#This function gets the int of the monster.
	def get_int(self):
		return self.int
	
	#This function gets the speed of the monster.
	def get_speed(self):
		return self.speed
	
	#This function gets the luck of the monster.
	def get_lck(self):
		return self.lck

def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

#This function checks if the window is still active.
def window_active(window):
	try:
		#If we can update, we return true.
		window.update()
		return True
	except(turtle.Terminator, tk.TclError):
		#Otherwise, we return false.
		return False
	
#This function gets the tile from the tile_map, and returns it's type.
def get_tile(row, col):
	global tile_map
	#We get the tile's row and column
	tile_row = tile_map[row]
	tile_col = tile_row[col]
	#We return the tile's column.
	return tile_col
	
#This function determines the chance of a player getting an encounter on a specific move.
def combat_chance(tile):
	#We set combat variable to false as a default.
	combat = False
	floor = 0
	#If the tile is a water tile, the chance of an encounter is higher.
	if tile == 2:
		floor = 2
	roll = random.randrange(floor,8)
	if roll > 4:
		#If the number is 5 or higher, we trigger combat.
		combat = True
	return combat

#This function moves the turtle in combat, but since I imported it from my previous project I am too afraid to rename or change it.
def move(turtle, index, pos):
	#We get the position, then teleport the turtle to the next position.
	local_position = pos[index]
	turtle.teleport(local_position[0],local_position[1])
	return

#This function moves the combat cursor up by updating the global index.
def combat_up():
	global global_index
	#If we are not in combat, we return as a fallback.
	if STATE != "combat":
		return
	if global_index == 0:
		#If the global index is 0 (the top of the list), we set it to the bottom of the list.
		global_index = 3
		move(combat_cursor, global_index, COMBAT_POSITIONS)
		game_window.update()
		return
	#We subtract 1 from the global index, and move the cursor to that point.
	global_index = (global_index - 1)
	move(combat_cursor, global_index, COMBAT_POSITIONS)
	#We update the game window.
	game_window.update()
	return

#This function move the combat cursor down by updating the global index.
def combat_down():
	global global_index
	if STATE != "combat":
		return
	#If the global index is 3, we move the cursor to the top of the list.
	if global_index == 3:
		global_index = 0
		move(combat_cursor, global_index, COMBAT_POSITIONS)
		game_window.update()
		return
	#We increment the global index, then move the cursor.
	global_index = (global_index + 1)
	move(combat_cursor, global_index, COMBAT_POSITIONS)
	game_window.update()
	return

#This function scrolls the world down, giving the effect that the turtle has moved up.
def move_up():
	global STATE, floor
	if STATE != "explore":
		return
	global camera_row
	global camera_col
	global global_cursor
	global game_window
	global main_hero
	#If we are in the first row, we don't move the world but change the facing angle of the turtle.
	if camera_row == 0:
		global_cursor.setheading(90)
		turtle.update()
		return
	tile = get_tile(camera_row - 1,camera_col)
	#If the tile is a wall, we make it so the user cannot move, and we update the heading of the turtle.
	if tile == 1:
		global_cursor.setheading(90)
		turtle.update()
		return
	elif tile == 3:
		floor = floor + 1
		floorstring = "floor" + str(floor) + ".csv"
		load_map(resource_path(resource_path(floorstring)))
		draw_grid()
		global_cursor.setheading(90)
		turtle.update()
		return
	#We subtract one from the camera row, update the heading, and print the chance.
	camera_row -= 1
	draw_grid()
	global_cursor.setheading(90)
	turtle.update()
	chance = combat_chance(tile)
	if chance :
		run_combat(game_window, main_hero)
	return

#This function moves the world up, giving the illusion that the turtle has moved down.
def move_down():
	global STATE, floor
	if STATE != "explore":
		return
	global camera_row
	global camera_col
	global global_cursor
	global game_window
	global main_hero
	#If the camera is at the edge of the grid, change the turtle's facing angle.
	if camera_row >= (map_rows - 1):
		global_cursor.setheading(270)
		turtle.update()
		return
	#If the turtle attempts to move to a wall tile, we update the turtle's facing angle.
	tile = get_tile(camera_row + 1, camera_col)
	if tile == 1:
		global_cursor.setheading(270)
		turtle.update()
		return
	elif tile == 3:
		floor = floor + 1
		floorstring = "floor" + str(floor) + ".csv"
		load_map(resource_path(floorstring))
		draw_grid()
		global_cursor.setheading(270)
		turtle.update()
		return
	#Otherwise, we move the camera and roll for combat.
	camera_row += 1
	draw_grid()
	global_cursor.setheading(270)
	turtle.update()
	chance = combat_chance(tile)
	if chance:
		run_combat(game_window, main_hero)
	return

#This function moves the world right, giving the illusion that the turtle has moved.
def move_left():
	global STATE, floor
	if STATE != "explore":
		return
	global camera_row
	global camera_col
	global global_cursor
	global game_window
	global main_hero
	#If the camera is at the edge of the map, we update the turtle's facing.
	if camera_col == 0:
		global_cursor.setheading(180)
		turtle.update()
		return
	#If the turtle is going to move into the wall, we update the turtle's facing.
	tile = get_tile(camera_row, camera_col - 1)
	if tile == 1:
		global_cursor.setheading(180)
		turtle.update()
		return
	elif tile == 3:
		floor = floor + 1
		floorstring = "floor" + str(floor) + ".csv"
		load_map(resource_path(floorstring))
		draw_grid()
		global_cursor.setheading(180)
		turtle.update()
		return
	#We move the turtle and update it's facing.
	camera_col -= 1
	draw_grid()
	global_cursor.setheading(180)
	turtle.update()
	chance = combat_chance(tile)
	if chance:
		run_combat(game_window, main_hero)
	return

#We move the world left to give the illusion that the turtle is moving.
def move_right():
	global STATE, floor
	if STATE != "explore":
		return
	global camera_row
	global camera_col
	global global_cursor
	#If the camera is at the edge of the world, we update the turtle's facing angle.
	if camera_col >= (map_cols - 1):
		global_cursor.setheading(0)
		turtle.update()
		return
	#If the turtle attempts to move to a wall tile, we update the facing angele.
	tile = get_tile(camera_row, camera_col + 1)
	if tile == 1:
		global_cursor.setheading(0)
		turtle.update()
		return
	elif tile == 3:
		floor = floor + 1
		floorstring = "floor" + str(floor) + ".csv"
		load_map(resource_path(floorstring))
		draw_grid()
		global_cursor.setheading(0)
		turtle.update()
		return
	#Otherwise, we move the turtle.
	camera_col += 1
	draw_grid()
	global_cursor.setheading(0)
	turtle.update()
	chance = combat_chance(tile)
	if chance:
		run_combat(game_window, main_hero)
	return


#This function loads the map.
def load_map(filename):
	global tile_map, map_rows, map_cols, floor, camera_row, camera_col

	tile_map = []
	#For each line, we loop through to create the tiles.
	with open(filename, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			tile_map.append([int(cell) for cell in row])
	#We save the map row and map columns.
	map_rows = len(tile_map)
	map_cols = len(tile_map[0])
	camera_row = 0 
	camera_col = 0
	return


#This function gets the return value and sets it into the combat return variable.
def enter():
	global combat_return
	combat_return = "a"
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

def cast(hero, enemy, attacker, defense):
	#If the attack is initiated by the player, the attacker variable should read "p"
	if attacker == "p":
		#We get the enemy's hp.
		starting_hp = enemy.get_hp()
		#We get the hero and the monster's strength.
		st = hero.get_int()
		df = enemy.get_int()
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
		dodge = enemy.get_lck()
		chance = random.randint(0,(dodge + 2))
		if chance >= dodge:
			return 100
		enemy.damage(st)
		ending_hp = enemy.get_hp()
		damage = abs(ending_hp - starting_hp)
		#We return the amount of damage the enemy took.
		return damage 
	#This function repeats if the attacker if the enemy, but with the roles swapped.
	if attacker == "e":
		starting_hp = hero.get_hp()
		st = enemy.get_int()
		df = hero.get_int()
		st = random.randint(0,st)
		df = random.randint(0,df)
		df = math.ceil(df /2)
		if(st - df < 0):
			st = 0
		else:
			st = st - df
		dodge = hero.get_lck()
		chance = random.randint(0,(dodge + 2))
		if chance >= dodge:
			return 100
		hero.damage(st)
		ending_hp = hero.get_hp()
		damage = abs(ending_hp - starting_hp)
		return damage
#This function is adapted from the poorly named CTP. It works mostly the same, but with a lot more global imports.
def run_combat(window, hero):
	global STATE
	global global_cursor, global_index, combat_return, combat_cursor, COMBAT_POSITIONS, text_turtle, update_turtle, enemy_turtle
	#We set the game state to combat.
	STATE = "combat"
	#We hide the tile maze.
	pen.clear()
	global_cursor.hideturtle()
	turtle.update()
	combat_return = ""
	#We set the up and down keys to combat_up and combat_down.
	window.onkey(combat_up, "Up")
	window.onkey(combat_down, "Down")
	#We set the global index to 0 as a default.
	global_index = 0
	#We create a new turtle as the cursor.
	cursor = turtle.Turtle()
	cursor.penup()
	combat_cursor = cursor
	combat_cursor.showturtle()
	turtle.update()
	window.update()
	#We make a turtle for the combat text image.
	t_turtle = create_turtle(window, resource_path("Images/combat-text.gif"))
	text_turtle = t_turtle
	text_turtle.teleport(-200, -200)
	#We create a turtle for the enemy image.
	e_turtle = create_turtle(window, resource_path("Images/Slime.gif"))
	enemy_turtle = e_turtle
	enemy_turtle.penup()
	#We set the text x and y, and base the combat positions off of that.
	text_x = text_turtle.xcor()
	text_y = text_turtle.ycor()
	#The combat_positions array is set based off of the text location.
	COMBAT_POSITIONS = [
	    (text_x - 70, text_y + 33),
	    (text_x - 70, text_y + 11.5),
	    (text_x - 70, text_y - 11),
	    (text_x - 70, text_y - 34)
	]
	#The update turtle is created.
	u_turtle = turtle.Turtle()
	update_turtle = u_turtle
	update_turtle.penup()
	update_turtle.hideturtle()
	update_turtle.goto(100, -100)
	#We create a monster. In the future it might even be a different monster.
	monster = Monster("Slime", 3, 1, 1, 2, 6, 3)
	#We create defense variables for the monster and hero, but it doesn't work.
	#We set the window to listen, and move the combat cursor.
	window.listen()
	window.onkey(enter, "Return")
	move(combat_cursor, 0, COMBAT_POSITIONS)
	#This is a function that runs a step of combat.
	def combat_step():
		global combat_return, STATE, hero_defense, monster_defense
		#We update the window.
		window.update()
		if STATE != "combat":
			#If the game state is not combat, we set it to combat.
			print("Leaving combat")
			return
		#If the return is a, the user has hit enter.
		if combat_return == "a":
			print(monster.get_hp())
			print("Doing action")
			if global_index == 0 :
				#We attack the enemy.
				update_turtle.write(hero.get_name + " attacked the " + monster.get_name() + "!")
				turtle.update()
				time.sleep(1)
				update_turtle.clear()
				turtle.update()
				chance = random.randint(0,1)
				if chance == 1:
					monster_defense = True
				update_turtle.write(monster.get_name + " braced for impact!")
				turtle.update()
				time.sleep(1)
				update_turtle.clear
				turtle.update()
				damage = attack(hero, monster, "p", monster_defense)
				if damage <= 0:
					update_turtle.write(monster.get_name() + " took no damage!")
				elif damage == 100:
					update_turtle.write(monster.get_name() + " dodged!")
				else:
					update_turtle.write(monster.get_name() + " took " + str(damage) + " damage!")
				turtle.update()
				time.sleep(1)
				update_turtle.clear()
				turtle.update()
			#Otherwise, we set hero defense to true.
			elif global_index == "1":
				#This variable is inacessable so I will need to rewrite this.
				hero_defense = True
			#We pass if the index is 2.
			elif global_index == "2":
				pass
			#If the index is 3, we end combat.
			elif global_index == "3":
				#This doesn't actually work.
				end_combat()
				return
			if monster.get_hp() > 0:
				damage = attack(hero, monster, "e", hero_defense)
				if damage <= 0:
					update_turtle.write(hero.get_name() + " took no damage!")
				elif damage == -99:
					update_turtle.write(hero.get_name() + " dodged!")
				else:
					update_turtle.write(hero.get_name() + " took " + str(damage) + " damage!")
			hero_defense = False
			monster_defense = False
		#We set the combat_return.
		combat_return = "e"
		#If the monster hp is 0, we end combat and return.
		if monster.get_hp() <= 0:
			update_turtle.write(monster.get_name() + " was defeated!")
			turtle.update()
			time.sleep(1)
			update_turtle.clear()
			turtle.update()
			end_combat()
			return
		window.update()
		window.ontimer(combat_step, 100)
	#We run this function every 100 miliseconds.
	window.ontimer(combat_step, 100)
	window.update()
	return

#This function cleans up after combat.
def end_combat():
	global STATE, global_cursor, combat_cursor, enemy_turtle, update_turtle, text_turtle
	STATE = "explore"
	#We show the global cursor and hide all the combat turtles.
	combat_cursor.hideturtle() 
	global_cursor.showturtle()
	enemy_turtle.hideturtle()
	update_turtle.hideturtle()
	text_turtle.hideturtle()
	#We draw the grid and update the turtle.
	draw_grid()
	turtle.update()
	#We set the game window to accept inputs like normal maze movement.
	game_window.onkey(move_up, "Up")
	game_window.onkey(move_down, "Down")
	game_window.onkey(move_left, "Left")
	game_window.onkey(move_right, "Right")

#This funciton redraws the world after every move.
def draw_grid():
    global pen
    pen.clear()
    for row in range(map_rows):
		#We draw the tiles one tile at a time in each row.
        for col in range(map_cols):
            tile_value = tile_map[row][col]
			#If we cannot get the tile, we create a pink error tile.
            color = TILE_COLORS.get(tile_value, "pink")  

            x, y = tile_to_screen(row, col)
			#The pen draws the tile.
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

#This function gets the tile in relation to where it is on the screen.
def tile_to_screen(row, col):
    dx = (col - camera_col) * TILE_SIZE
    dy = (camera_row - row) * TILE_SIZE
    return SCREEN_CENTER_X + dx, SCREEN_CENTER_Y + dy


#This is the main function where the movement logic happens.
def main():
	#We initalise the global variables.
	global global_cursor
	global pen
	global game_window
	global main_hero
	global STATE
	global COMBAT_POSITIONS
	global floor
	COMBAT_POSITIONS = [(100,200),(150,250),(200,300),(250,350)]
	STATE = "explore"
	floor = 1
	#game_font = "PressStart2P"
	floorstring = "floor" + str(floor) + ".csv"
	load_map(resource_path(floorstring))
	#We create the window for the game screen.
	window = turtle.Screen()
	hero = Hero("Yusha", 15, 10, 5, 4, 5, 10, "Sword")
	main_hero = hero
	window.setup(600,600)
	window.title("Combat Window")
	window.tracer(0)
	game_window = window
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
	x, y = tile_to_screen(camera_row, camera_col)
	global_cursor.goto(x, y)
	global_cursor.showturtle()
	turtle.update()
	window.update()
	#We move the cursor to the starting combat position.
	#We create the update turtle.
	update_turtle = turtle.Turtle()
	update_turtle.penup()
	update_turtle.hideturtle()
	update_turtle.goto(100, -100)
	#We create a hero object.
	main_hero = Hero("Yusha",15,10,5,4,5,10,"Sword")
	#We set the window to react to up and down inputs.
	window.listen()
	window.onkey(move_up, "Up")
	window.onkey(move_down, "Down")
	window.onkey(move_right,"Right")
	window.onkey(move_left, "Left")
	window.onkey(enter, "Return")
	#Updated this to use turtle.mainloop() instead of a terrible window live function.
	turtle.mainloop()

	#We attampt to gracefully close the window.
	try:
		window.bye()
	except Exception:
		pass
	
	
#This is the main function.
main()

