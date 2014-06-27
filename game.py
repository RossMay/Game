from __future__ import division
import libtcodpy as libtcod
from libtcodpy import random_get_int as rand
import math, textwrap, time, sys, shelve


##################################################################################################################################
##################################################################################################################################
##																																##
##						    CCCCCCC        OOOO      NNN     NN  EEEEEEEE  IIIIIIII   GGGGGGG   		    					##
##						   CC      CC    OO    OO    NNNN    NN  EE           II     GG      GG   		    					##
##						  CC           OO        OO  NN NN   NN  EE           II     GG   		    							##
##						  CC           OO        OO  NN NN   NN  EEEEEEE      II     GG   		    							##
##						  CC           OO        OO  NN  NN  NN  EE           II     GG    GGGGG   		    					##
##						  CC           OO        OO  NN   NN NN  EE           II     GG      GG   		    					##
##						   CC      CC    OO    OO    NN    NNNN  EE           II     GG      GG   		    					##
##						    CCCCCCC        OOOO      NN     NNN  EE        IIIIIIII    GGGGGG   		    					##
##																																##
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Debug																														 #
##################################################################################################################################

DEBUG 		= False
DEBUGMSG 	= DEBUG
DISABLE_AI	= DEBUG

##################################################################################################################################
#	Configuration																												 #
##################################################################################################################################

#	FPS Limit
LIMIT_FPS 		= 20	# Limit the speed of the main loop

#	Screen Dimensions
SCREEN_WIDTH 	= 80	# Overall screen width
SCREEN_HEIGHT 	= 50	# Overall screen height

#	Map Dimensions
MAP_WIDTH 		= 80	# Width of the playable map
MAP_HEIGHT 		= 43	# Height of the playable map

#	Game States
STATE_PLAYING	= 0		# Player os currently playing, each action triggers a turn
STATE_TARGET 	= 1 	# Player is selecting a target, no turn is used up
STATE_DEAD 		= 2 	# Player died

#	Player Actions
ACTION_NONE 	= 0 	# Player did not take an action
ACTION_TURN		= 1 	# Player took a turn
ACTION_EXIT 	= 2 	# Player selected quit

#	Results
RESULT_CANCELLED = 1 	# Function was cancelled (Ex. Spell is out of range)

#	FOV
FOV_ALGO 		= 0		# Field of view algorithm to use (Default = 0)
FOV_LIGHT_WALLS = True	# Should the first layer of walls light up while in fov (Yes)

#	UI
INVENTORY_WIDTH = 50							# Width of the inventory menu
SPELL_WIDTH 	= 50							# Width of the spell menu

BAR_WIDTH 		= 25							# Width of health / mana bars
PANEL_HEIGHT 	= 7 							# Height of the bottom panel
PANEL_Y 		= SCREEN_HEIGHT - PANEL_HEIGHT	# Where to start the panel

MSG_X 			= BAR_WIDTH + 2 				# Where to start the message window, right after the bars
MSG_WIDTH 		= SCREEN_WIDTH - BAR_WIDTH - 2 	# Where to end the message window, 2 from the edge of the screen
MSG_HEIGHT 		= PANEL_HEIGHT - 1 				# Height of the message window


##################################################################################################################################
#	Generation																													 #
##################################################################################################################################

#	Spawning
MAX_ROOM_MONSTERS 	= 3 	# Maximum number of monsters to spawn in a room
MAX_ROOM_ITEMS 		= 2 	# Maximum number of items to spawn in a room

#	Room Creation
ROOM_MIN_SIZE 		= 8 	# Minimum room width / height
ROOM_MAX_SIZE 		= 20	# Maximum room width / height
RANDOM_HALLS 		= 10 	# Number of random rooms to connect after map generation

##################################################################################################################################
#	Default Values																												 #
##################################################################################################################################

#	Light Radius
LIGHT_RADIUS = 10 if not DEBUG else 1000	# Light radius!

##################################################################################################################################
#	Characters																													 #
##################################################################################################################################

CHAR_PLAYER 	= '@'	# Player
CHAR_NPC    	= 'N'	# NPC
CHAR_WALL   	= '#'	# Wall
CHAR_GROUND 	= '.'	# Basic ground
CHAR_OTHER  	= ' '	# Anything else
CHAR_CORPSE 	= '%'	# Corpse
CHAR_SPELL 		= ' '	# Default spell character
CHAR_SPELL_PATH = ' '	# Default spell path character


##################################################################################################################################
#	Keybinds																													 #
##################################################################################################################################

#	Movement
KEYS_UP 		= [libtcod.KEY_UP, libtcod.KEY_KP8]
KEYS_DOWN 		= [libtcod.KEY_DOWN, libtcod.KEY_KP2]
KEYS_LEFT 		= [libtcod.KEY_LEFT, libtcod.KEY_KP4]
KEYS_RIGHT 		= [libtcod.KEY_RIGHT, libtcod.KEY_KP6]
KEYS_UPLEFT 	= [libtcod.KEY_KP7]
KEYS_UPRIGHT 	= [libtcod.KEY_KP9]
KEYS_DOWNLEFT 	= [libtcod.KEY_KP1]
KEYS_DOWNRIGHT 	= [libtcod.KEY_KP3]
KEYS_WAIT		= [libtcod.KEY_KP5, 'w']

#	General
KEYS_CONFIRM	= [libtcod.KEY_KPENTER, 'c']
KEYS_CANCEL		= [libtcod.KEY_KPSUB, 'q']

# 	Spells
KEYS_CAST		= [libtcod.KEY_KPADD, libtcod.KEY_SPACE]
KEYS_SPELL		= [libtcod.KEY_KPMUL, 's']

#	Items
KEYS_PICKUP 	= [libtcod.KEY_KP0, ',']
KEYS_DROP		= ['d']
KEYS_INVENTORY 	= ['i', libtcod.KEY_KPSUB]

#	Other
KEYS_EXIT 		= [libtcod.KEY_ESCAPE]
KEYS_FULLSCREEN = [libtcod.KEY_F11]

# libtcod.KEY_KPADD / SUB / DIV / MUL / DEC / ENTER

##################################################################################################################################
#	Colors																														 #
##################################################################################################################################

#	Color to use for transparency
COLOR_TRANSPARENT = libtcod.Color(255,0,255)			# Color to use as the transparency for things like spell target console

#	Walls
COLOR_DARK_WALL_BG 	= libtcod.Color(0,0,0)				# Background for dark walls
COLOR_DARK_WALL_FG 	= libtcod.Color(41,16,2)			# Foreground for dark walls
COLOR_LIGHT_WALL_BG = libtcod.Color(0,0,0)				# Background for light walls
COLOR_LIGHT_WALL_FG = libtcod.Color(85,41,15)			# Foreground for light walls

#	Ground
COLOR_DARK_GROUND_BG 	= libtcod.Color(0,0,0)			# Background for dark ground
COLOR_DARK_GROUND_FG 	= libtcod.Color(39,39,39)		# Foreground for dark ground
COLOR_LIGHT_GROUND_BG 	= libtcod.Color(0,0,0)			# Background for light ground
COLOR_LIGHT_GROUND_FG 	= libtcod.Color(129,129,129)	# Foreground for light ground

#	Spell Targetting Valid
SPELL_TARGET_TRANSPARENCY 	= 0.65						# Transparency level for the spell targetting console 0.0 -> 1.0
COLOR_SPELL_TARGET_LINE_BG 	= libtcod.lightest_green	# Background for the spell targetting line
COLOR_SPELL_TARGET_LINE_FG 	= COLOR_TRANSPARENT			# Foreground for the spell targetting line (Spell path character color)
COLOR_SPELL_TARGET_BG 		= libtcod.green 			# Background of the cell being targetted
COLOR_SPELL_TARGET_FG 		= COLOR_TRANSPARENT			# Foreground on the cell being targetted (Spell character color)

#	Spell Targetting Invalid
COLOR_SPELL_TARGET_LINE_BAD_BG 	= libtcod.lightest_red	# Background for the line to an invalid target
COLOR_SPELL_TARGET_LINE_BAD_FG 	= COLOR_TRANSPARENT		# Foreground for the line to an invalid target
COLOR_SPELL_TARGET_BAD_BG 		= libtcod.red 			# Background for the cell of an invalid target
COLOR_SPELL_TARGET_BAD_FG 		= COLOR_TRANSPARENT		# Foreground for the cell of an invalid target


##################################################################################################################################
##################################################################################################################################
##																																##
##					      OOOO      BBBBBBBBB   JJJJJJJJJJJ  EEEEEEEE    CCCCCCC    TTTTTTTT   SSSSSSSS 						##
##					    OO    OO    BB      BB        JJ     EE         CC      CC     TT     SS       							##
##					  OO        OO  BB      BB        JJ     EE        CC              TT     SS       							##
##					  OO        OO  BBBBBBBB          JJ     EEEEEEE   CC              TT       SSS    							##
##					  OO        OO  BB     BB         JJ     EE        CC              TT         SSS  							##
##					  OO        OO  BB      BB        JJ     EE        CC              TT            SS							##
##					    OO    OO    BB      BB  JJ   JJ      EE         CC      CC     TT            SS							##
##					      OOOO      BBBBBBBBB     JJJJ       EEEEEEEE    CCCCCCC       TT     SSSSSSSS 							##
##																																##
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Classes																														 #
##################################################################################################################################

class Object:
	def __init__(self, x, y, char=' ', name='Unknown Object', color=libtcod.white, blocks=False, fighter=None, ai=None, item=None):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.name = name
		self.blocks = blocks
		self.fighter = fighter
		self.ai = ai
		self.item = item

		if self.fighter: self.fighter.owner = self	
		if self.ai: self.ai.owner = self
		if self.item: self.item.owner = self

	def move(self, dx, dy):
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
			return True
		return False

	def move_towards(self, target_x, target_y):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		self.move(dx,dy)

	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y

		return math.sqrt(dx ** 2 + dy ** 2)

	def distance_to_point(self, x, y):
		dx = x - self.x
		dy = y - self.y

		return math.sqrt(dx ** 2 + dy ** 2)

	def in_range(self,x,y,d):
		return self.distance_to_point(x,y) >= d

	def object_in_range(self,obj,d):
		return self.distance_to(obj) >= d

	def draw(self):
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self):
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

	def send_to_back(self):
		global objects

		objects.remove(self)
		objects.insert(0,self)


##################################################################################################################################
##################################################################################################################################
##																																##
##										  NNN     NN  PPPPPPPP      CCCCCCC     SSSSSSSS 										##
##										  NNNN    NN  PP     PP    CC      CC  SS       										##
##										  NN NN   NN  PP      PP  CC           SS       										##
##										  NN NN   NN  PP     PP   CC             SSS    										##
##										  NN  NN  NN  PPPPPPP     CC               SSS  										##
##										  NN   NN NN  PP          CC                  SS										##
##										  NN    NNNN  PP           CC      CC         SS										##
##										  NN     NNN  PP            CCCCCCC    SSSSSSSS 										##
##																																##
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Classes																														 #
##################################################################################################################################

class Fighter:
	def __init__(self, hp, mana, defense, power, death_function=None, friendly=False, enemy=True):
		self.death_function = death_function
		self.max_hp = hp
		self.hp = hp
		self.max_mana = mana
		self.mana = mana
		self.defense = defense
		self.friendly = friendly
		self.enemy = enemy

		if not len(power):
			power = (power,power)

		self.power_min = power[0]
		self.power_max = power[1]

	def take_damage(self, damage):
		if damage > 0:
			self.hp -= damage

		if self.hp <= 0:
			self.hp = 0
			function = self.death_function
			if function is not None:
				function(self.owner)

	def attack(self, target):
		damage = rand(0,self.power_min,self.power_max) - target.fighter.defense

		if damage > 0:
			message("%s attacks %s for %s damage." % (self.owner.name.capitalize(), target.name, damage), libtcod.white)
			target.fighter.take_damage(damage)
		else:
			message("%s attacks %s but it does nothing." % (self.owner.name.capitalize(), target.name), libtcod.white)

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

def spawn_monster(x, y, monster):
	global objects

	new_monster = Object(x, y, 
					char=monster['char'],
					name=monster['name'],
					color=monster['color'], 
					blocks=True, 
					fighter=Fighter(
								hp=monster['hp'],
								mana=monster['mana'],
								defense=monster['defense'],
								power=(monster['power_min'],monster['power_max']), 
								death_function=monster['death_function'],
								friendly=False,
								enemy=True
							), 
					ai=monster['ai']()
				)
	objects.append(new_monster)

	return True


##################################################################################################################################
##################################################################################################################################
##																																##
##  													   AAAA     IIIIIIII													##
##														  AA  AA       II 														##
##														 AA    AA      II 														##
##														AA      AA     II 														##
##														AAAAAAAAAA     II 														##
##														AA      AA     II 														##
##														AA      AA     II 														##
##														AA      AA  IIIIIIII													##
##																																##
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Classes																														 #
##################################################################################################################################

class BasicMonster:
	def take_turn(self):
		monster = self.owner
		if DISABLE_AI: return
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)

			elif player.fighter.hp > 0:
				monster.fighter.attack(player)

class ConfusedMonster:
	def __init__(self, old_ai, duration=5):
		self.old_ai = old_ai
		self.duration = duration
	def take_turn(self):
		if self.duration > 0:
			self.owner.move(rand(0,-1,1), rand(0,-1,1))
			self.duration -= 1
		else:
			self.owner.ai = self.old_ai
			message('The %s is no longer confused.', libtcod.red)


##################################################################################################################################
##################################################################################################################################
##																																##
##										IIIIIIII  TTTTTTTT  EEEEEEEE  MM         MM   SSSSSSSS 									##
##										   II        TT     EE        MMMM     MMMM  SS       									##
##										   II        TT     EE        MM MM   MM MM  SS       									##
##										   II        TT     EEEEEEE   MM  MM MM  MM    SSS    									##
##										   II        TT     EE        MM   MMM   MM      SSS  									##
##										   II        TT     EE        MM         MM         SS									##
##										   II        TT     EE        MM         MM         SS									##
##										IIIIIIII     TT     EEEEEEEE  MM         MM  SSSSSSSS 									##
##																																##			
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Classes																														 #
##################################################################################################################################

class Item:
	def __init__(self, spell=None, consumable=False, use_function=None, value=None):
		self.use_function = use_function
		self.consumable = consumable
		self.value = value
		self.spell = spell
		if self.spell and not self.use_function:
			self.use_function = self.spell['cast_function']

	def use(self):
		if self.use_function is None:
			message('The %s cannot be used.' % self.owner.name)
		else:
			if self.spell:
				value = self.spell
			else:
				value = self.value

			if self.use_function(value) != RESULT_CANCELLED and self.consumable:
				inventory.remove(self.owner)


	def pick_up(self):
		if len(inventory) >= 26:
			message('Your inventory is full, cannot pick up  %s.' % self.owner.name, libtcod.red)
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			message("You picked up a %s." % self.owner.name, libtcod.green)

	def drop(self):
		objects.append(self.owner)
		inventory.remove(self.owner)
		self.owner.x = player.x
		self.owner.y = player.y
		message("You dropped a %s." % self.owner.name, libtcod.yellow)

def spawn_item(x, y, item):

	global objects

	new_item =  Object(x, y, 
					char=item['char'], 
					name=item['name'], 
					color=item['color'], 
					item=Item(
						spell=item.get('spell',None), 
						consumable=item.get('consumable',False), 
						use_function=item.get('use_function',None), 
						value=item.get('value',None)
						)
					)

	objects.append(new_item)
	new_item.send_to_back()

	return True


##################################################################################################################################
##################################################################################################################################
##																																##
##								 SSSSSSSS  PPPPPPPP    EEEEEEEE  LL        LL         SSSSSSSS 									##
##								SS         PP     PP   EE        LL        LL        SS 										##
##								SS         PP      PP  EE        LL        LL        SS 										##
##								  SSS      PP     PP   EEEEEEE   LL        LL          SSS 										##
##								    SSS    PPPPPPP     EE        LL        LL            SSS 									##
##								       SS  PP          EE        LL        LL               SS 									##
##								       SS  PP          EE        LL        LL               SS 									##
##								SSSSSSSS   PP          EEEEEEEE  LLLLLLLL  LLLLLLLL  SSSSSSSS									##
##																																##
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Cast functions																												 #
##################################################################################################################################

def cast_heal(spell, x=None, y=None):
	amount = rand(0, spell['min'], spell['max'])

	if x == None:
		target = player
	else:
		target = get_target_at(x,y,friendly=spell['friendly'], enemy=spell['enemy'], self=spell['self'])
		if target is None:
			message('Invalid target.', libtcod.red)
			return RESULT_CANCELLED
		elif player.distance_to(target) > spell['range']:
			message('Target is out of range.', libtcod.red)
			return RESULT_CANCELLED


	if target.fighter.hp == target.fighter.max_hp:
		if target == player:
			message('You are already at full health.', libtcod.red)
		else:
			message('%s is already at full health.' % target.name, libtcod.red)
		return RESULT_CANCELLED

	if target == player:
		message('You restored %s health!' % amount, libtcod.light_green)
	else:
		message('%s restored %s health!' % (target.name,amount), libtcod.light_green)
	target.fighter.heal(amount)

def cast_lightning(spell, x=None, y=None):
	damage = rand(0, spell['min'], spell['max'])

	if x == None:
		target = closest_monster(spell['range'])
		if target is None:
			message('No enemy in range.', libtcod.red)
			return RESULT_CANCELLED
	else:
		target = get_target_at(x,y,friendly=spell['friendly'], enemy=spell['enemy'], self=spell['self'])
		if target is None:
			message('Invalid target.', libtcod.red)
			return RESULT_CANCELLED
		elif player.distance_to(target) > spell['range']:
			message('Target is out of range.', libtcod.red)
			return RESULT_CANCELLED

	message('%s strikes %s for %s damage.' % (spell['name'], target.name, damage), libtcod.light_blue)
	target.fighter.take_damage(damage)

def cast_confuse(spell, x=None, y=None):	
	duration = rand(0, spell['min_duration'], spell['max_duration'])

	if x == None:
		target = closest_monster(spell['range'])
		if target is None:
			message('No enemy in range.', libtcod.red)
			return RESULT_CANCELLED
	else:
		target = get_target_at(x,y)
		if target is None:
			message('Invalid target.', libtcod.red)
			return RESULT_CANCELLED
		elif player.distance_to(target) > spell['range']:
			message('Target is out of range.', libtcod.red)
			return RESULT_CANCELLED

	old_ai = target.ai
	target.ai = ConfusedMonster(old_ai, duration=duration)
	target.ai.owner = target
	message('%s is now confused for %s turns.' % (target.name, duration), libtcod.light_blue)

def cast_fireball(spell, x=None, y=None):
	damage = rand(0, spell['min'], spell['max'])

	if x == None:
		closest = closest_monster(spell['range'])
		if closest is None:
			message('No enemy in range.', libtcod.red)
			return RESULT_CANCELLED
		else:
			x = closest.x
			y = closest.y
	
	if player.in_range(x,y,spell['range']):
		message('Target is out of range.', libtcod.red)
		return RESULT_CANCELLED

	targets = get_targets_around(x,y,spell['radius'],friendly=spell['friendly'], enemy=spell['enemy'], self=spell['self'])

	if not len(targets):
		message('Nothing was hit by the fireball', libtcod.red)
		return

	for target in targets:
		message('%s strikes %s for %s damage.' % (spell['name'], target.name, damage), libtcod.light_blue)
		target.fighter.take_damage(damage)

def move_target(dx, dy):
	global target_coords
	target_coords = (target_coords[0] + dx, target_coords[1] + dy)


##################################################################################################################################
##################################################################################################################################
##																																##
##								EEEEEEEE  VV      VV  EEEEEEEE  NNN     NN  TTTTTTTT   SSSSSSSS  								##
##								EE        VV      VV  EE        NNNN    NN     TT     SS        								##
##								EE         VV    VV   EE        NN NN   NN     TT     SS        								##
##								EEEEEEE    VV    VV   EEEEEEE   NN NN   NN     TT       SSS     								##
##								EE          VV  VV    EE        NN  NN  NN     TT         SSS   								##
##								EE          VV  VV    EE        NN   NN NN     TT            SS 								##
##								EE           VVVV     EE        NN    NNNN     TT            SS 								##
##								EEEEEEEE      VV      EEEEEEEE  NN     NNN     TT     SSSSSSSS  								##
##																																##			
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Death Events																												 #
##################################################################################################################################

def player_death(player):
	global game_state

	message("You have died!", libtcod.dark_red)
	game_state = STATE_DEAD

	player.char = CHAR_CORPSE
	player.color = libtcod.dark_red

def monster_death(monster):
	message("%s is slain." % monster.name, libtcod.orange)

	monster.char = CHAR_CORPSE
	monster.color = libtcod.dark_red

	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'Remains of %s' % monster.name

	monster.send_to_back()

##################################################################################################################################
#	Player Events																												 #
##################################################################################################################################

def player_move_or_attack(dx, dy):
	global fov_recompute

	x = player.x + dx
	y = player.y + dy

	target = None

	for obj in objects:
		if obj.fighter and obj.x == x and obj.y == y:
			target = obj
			break

	if target is not None:
		player.fighter.attack(target)

	else:
		fov_recompute = player.move(dx, dy)


##################################################################################################################################
##################################################################################################################################
##																																##
##											MM         MM     AAAA     PPPPPPPP    												##
##											MMMM     MMMM    AA  AA    PP     PP   												##
##											MM MM   MM MM   AA    AA   PP      PP  												##
##											MM  MM MM  MM  AA      AA  PP     PP   												##
##											MM   MMM   MM  AAAAAAAAAA  PPPPPPP     												##
##											MM         MM  AA      AA  PP          												##
##											MM         MM  AA      AA  PP          												##
##											MM         MM  AA      AA  PP          												##
##																																##			
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Classes																														 #
##################################################################################################################################

class MapNode:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.room = None
		self.left = None
		self.right = None

	def get_room(self):
		if self.room != None:
			return self.room

		if self.left != None:
			lroom = self.left.get_room()
		if self.right != None:
			rroom = self.right.get_room()

		if lroom == None and rroom == None:
			return None
		elif rroom == None:
			return lroom
		elif lroom == None:
			return rroom
		elif rand(0,1,100) > 50:
			return lroom
		else:
			return rroom
		
	def get_random_room(self):
		if self.room != None:
			return self.room

		if self.left != None or self.right != None:
			return self.left.get_random_room() if rand(0,1,100) > 50 else self.right.get_random_room()
		else:
			return None

	def split(self):
		if self.left != None or self.right != None:
			return False
		random = False

		if (self.width > self.height) and (self.height/self.width) <=  0.25:
			split = False
		elif (self.height > self.width) and (self.width / self.height) <= 0.25:
			split = True
		else:
			random = True
			split = rand(0,1,100) > 50

		maxlen = (self.height if split else self.width) - ROOM_MIN_SIZE

		if maxlen < ROOM_MIN_SIZE:
			return False

		splitspot = rand(0,ROOM_MIN_SIZE, maxlen)

		if split:
			self.left = MapNode(self.x, self.y, self.width, splitspot)
			self.right = MapNode(self.x, self.y + splitspot, self.width, self.height - splitspot)
		else:
			self.left = MapNode(self.x, self.y, splitspot, self.height)
			self.right = MapNode(self.x + splitspot, self.y, self.width - splitspot, self.height)
		
		if self.left.width > ROOM_MAX_SIZE or self.left.height > ROOM_MAX_SIZE or rand(0,1,100) > 715:
			self.left.split()
		if self.right.width > ROOM_MAX_SIZE or self.right.height > ROOM_MAX_SIZE or rand(0,1,100) > 175:
			self.right.split()
		return True

	def create_rooms(self):
		global level_map

		if self.left != None or self.right != None:
			if self.left != None:
				self.left.create_rooms()
			if self.right != None:
				self.right.create_rooms()

			if self.left != None and self.right != None:
				create_hall(self.left.get_room(), self.right.get_room())

		else:
			w = rand(0,ROOM_MIN_SIZE,self.width - 1)
			h = rand(0,ROOM_MIN_SIZE,self.height - 1)

			rx = rand(0, 0, self.width - w - 1)
			ry = rand(0, 0, self.height - h - 1)

			self.room = Rect(self.x + rx, self.y + ry, w, h)
			
			for x in range(self.room.x1 + 1, self.room.x2):
				for y in range(self.room.y1 + 1, self.room.y2):
					level_map[x][y].blocked = False
					level_map[x][y].block_sight = False

			place_objects(self.room)

class Tile:
	def __init__(self, blocked, block_sight=None):
		self.blocked = blocked
		self.explored = False

		if block_sight is None: 
			block_sight = blocked

		self.block_sight = block_sight

class Rect:
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2) // 2
		center_y = (self.y1 + self.y2) // 2
		return (center_x, center_y)

	def intersect(self, other):
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

##################################################################################################################################
#	Map Generation																												 #
##################################################################################################################################

def make_map():
	global level_map, player, target_coords, objects

	objects = [player]

	level_map = [[ Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

	nodes = []
	root_node = MapNode(0, 0, MAP_WIDTH, MAP_HEIGHT)
	root_node.split()

	root_node.create_rooms()

	for i in range(RANDOM_HALLS):
		create_hall(root_node.get_random_room(),root_node.get_random_room())

	player.x, player.y = root_node.get_random_room().center()
	target_coords = (player.x+1,player.y+2)

def create_hall(room1, room2):

	prev_x, prev_y = room1.center()
	new_x, new_y = room2.center()

	libtcod.line_init(prev_x,prev_y,new_x,new_y)
	x,y = libtcod.line_step()
	while x is not None:
		level_map[x][y].blocked = False
		level_map[x][y].block_sight = False
		level_map[x][y+1].blocked = False
		level_map[x][y+1].block_sight = False
		x,y = libtcod.line_step()

##################################################################################################################################
#	Field of View Initialization																								 #
##################################################################################################################################

def init_fov():
	global fov_map, fov_recompute

	fov_recompute = True

	libtcod.console_clear(con)

	fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			if DEBUG:
				libtcod.map_set_properties(fov_map, x, y, True, True)
			else:
				libtcod.map_set_properties(fov_map, x, y, not level_map[x][y].block_sight, not level_map[x][y].blocked)

def place_objects(room):
	global items, objects
	num_monsters = rand(0, 0, MAX_ROOM_MONSTERS)

	for i in range(num_monsters):
		while True:
			x = rand(0, room.x1+1, room.x2-1)
			y = rand(0, room.y1+1, room.y2-1)

			if not is_blocked(x,y):
				break

		chance = rand(0, 0, 100)

		if chance < 20:
			monster = monsters['orc']
		elif chance < 20+40:			
			monster = monsters['troll']
		elif chance < 20+40+30:
			monster = monsters['zombie']
		else:
			monster = monsters['bat']

		spawn_monster(x, y, monster)

	num_items = rand(0, 0, MAX_ROOM_ITEMS)
	for i in range(num_items):
		while True:
			x = rand(0, room.x1+1, room.x2-1)
			y = rand(0, room.y1+1, room.y2-1)

			if not is_blocked(x, y):
				break

		chance = rand(0, 0, 100)

		if chance < 50:
			spawn_item(x, y, items['potions']['healing'])
		elif chance < 50 + 25:
			spawn_item(x, y, items['scrolls']['lightning'])			
		else:
			spawn_item(x, y, items['scrolls']['confuse'])


##################################################################################################################################
##################################################################################################################################
##																																##
##				  UU      UU  TTTTTTTT  IIIIIIII  LL        IIIIIIII  TTTTTTTT  IIIIIIII  EEEEEEEE   SSSSSSSS  					##
##				  UU      UU     TT        II     LL           II        TT        II     EE        SS         					##
##				  UU      UU     TT        II     LL           II        TT        II     EE        SS         					##
##			  	  UU	  UU     TT        II     LL           II        TT        II     EEEEEEE     SSS      					##
##				  UU      UU     TT        II     LL           II        TT        II     EE            SSS    					##
##				  UU      UU     TT        II     LL           II        TT        II     EE               SS  					##
##				  UU      UU     TT        II     LL           II        TT        II     EE               SS  					##
##				    UUUUUU       TT     IIIIIIII  LLLLLLLL  IIIIIIII     TT     IIIIIIII  EEEEEEEE  SSSSSSSS   					##
##																																##			
##################################################################################################################################
##################################################################################################################################


def is_blocked( x, y):
		if level_map[x][y].blocked:
			return True

		for obj in objects:
			if obj.blocks and obj.x == x and obj.y == y:
				return True

		return False

def closest_monster(max_range):
	closest_enemy = None
	closest_dist = max_range + 1

	for obj in objects:
		if obj.fighter and not obj == player and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
			dist = player.distance_to(obj)
			if dist < closest_dist:
				closest_enemy = obj
				closest_dist = dist
	return closest_enemy

def get_target_at(x,y, friendly=None, enemy=None, self=False):
	for obj in objects:
		if obj.fighter and obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):

			if self and obj == player:
				return obj
			elif not self and obj == player:
				continue

			if friendly is not None and friendly and obj.fighter.friendly:
				return obj
			elif friendly is not None and not friendly and obj.fighter.friendly:
				continue

			if enemy is not None and enemy and obj.fighter.enemy:
				return obj
			elif enemy is not None and not enemy and obj.fighter.enemy:
				continue

			return obj
	return None

def get_targets_around(x,y,radius, friendly=None, enemy=None, self=False):
	targets = []
	for obj in objects:
		if obj.fighter and obj.distance_to_point(x,y) <= radius and libtcod.map_is_in_fov(fov_map, obj.x, obj.y):

			if self and obj == player:
				targets.append(obj)
				continue
			elif not self and obj == player:
				continue

			if friendly is not None and friendly and obj.fighter.friendly:
				targets.append(obj)
				continue
			elif friendly is not None and not friendly and obj.fighter.friendly:
				continue

			if enemy is not None and enemy and obj.fighter.enemy:
				targets.append(obj)
				continue
			elif enemy is not None and not enemy and obj.fighter.enemy:
				continue

	return targets


##################################################################################################################################
##################################################################################################################################
##																																##
##													UU      UU  IIIIIIII														##
##													UU      UU     II   														##	
##													UU      UU     II   														##
##													UU	    UU     II   														##
##													UU      UU     II   														##
##													UU      UU     II   														##
##													UU      UU     II   														##
##													  UUUUUU    IIIIIIII														##
##																																##			
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Menu System																													 #
##################################################################################################################################

def menu(header, options, width):
	if len(options) > 26: 
		raise ValueError('Cannot have a menu with more than 26 items')

	header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header) if len(header) else 0
	height = len(options) + header_height

	window = libtcod.console_new(width, height)
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '%s) %s' % (chr(letter_index), option_text)
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	x = SCREEN_WIDTH//2 - width//2
	y = SCREEN_HEIGHT//2 - height//2
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

	libtcod.console_flush()
	key = libtcod.console_wait_for_keypress(True)

	index = key.c - ord('a')
	if index >= 0 and index < len(options): return index
	return None

def main_menu():
	img = libtcod.image_load('bg.png')

	while not libtcod.console_is_window_closed():

		libtcod.image_blit_2x(img, 0, 0, 0)

		libtcod.console_set_default_foreground(0, libtcod.light_yellow)
		libtcod.console_print_ex(0, int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)-4, libtcod.BKGND_NONE, libtcod.CENTER, 'FUTURE TITLE HERE')

		choice = menu('', ['New Game', 'Continue', 'Load', 'Quit'], 24)

		if key.vk in KEYS_FULLSCREEN:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

		if choice == 0:
			new_game()
			play_game()

		elif choice == 1:
			if not game_started:
				new_game()
			play_game()

		elif choice == 2:
			try:
				load_game()
			except:
				msgbox('\nError loading game.\n', 24)
				continue
			play_game()

		elif choice == 4:
			save_game()
			break

def inventory_menu(header):
	if len(inventory) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory]

	index = menu(header, options, INVENTORY_WIDTH)

	if index is None or len(inventory) == 0: return None
	return inventory[index].item

def spell_menu(header):
	if len(spell_list) == 0:
		options = ['You don\'t know any spells.']
	else:
		options = [spell['name'] for spell in spell_list]

	index = menu(header, options, SPELL_WIDTH)

	if index is None or len(spell_list) == 0: return None
	return spell_list[index]

##################################################################################################################################
#	UI Utilities																												 #
##################################################################################################################################

def message_box(text, width=50):
	menu(text, [], width)

def message(new_msg, color = libtcod.white):
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		if len(game_messages) == MSG_HEIGHT:
			del game_messages[0]
		game_messages.append( (line, color) )

def get_names_under_mouse():
	global mouse

	(x, y) = mouse.cx, mouse.cy
	
	names = [obj.name for obj in objects if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map,obj.x, obj.y)]

	names = ','.join(names)

	return names.capitalize()



##################################################################################################################################
##################################################################################################################################
##								RRRRRRRR    EEEEEEEE  NNN     NN  DDDDDD     EEEEEEEE  RRRRRRRR   								##
##								RR     RR   EE        NNNN    NN  DD    DD   EE        RR     RR  								##
##								RR     RR   EE        NN NN   NN  DD     DD  EE        RR     RR  								##
##								RRRRRRRR    EEEEEEE   NN NN   NN  DD     DD  EEEEEEE   RRRRRRRR   								##
##								RRRR        EE        NN  NN  NN  DD     DD  EE        RRRR       								##
##								RR  RR      EE        NN   NN NN  DD     DD  EE        RR  RR     								##
##								RR    RR    EE        NN    NNNN  DD    DD   EE        RR    RR   								##
##								RR     RR   EEEEEEEE  NN     NNN  DDDDDD     EEEEEEEE  RR     RR  								##
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Main Render 																												 #
##################################################################################################################################

def render_all():
	global fov_map, fov_recompute

	if fov_recompute:
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, LIGHT_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			visible = libtcod.map_is_in_fov(fov_map, x, y)

			if visible:
					if level_map[x][y].blocked:
						libtcod.console_put_char_ex(con, x, y, CHAR_WALL, COLOR_LIGHT_WALL_FG, COLOR_LIGHT_WALL_BG)
					else:
						libtcod.console_put_char_ex(con, x, y, CHAR_GROUND, COLOR_LIGHT_GROUND_FG,COLOR_LIGHT_GROUND_BG)
					level_map[x][y].explored = True
			else:
				if level_map[x][y].explored:
					if level_map[x][y].blocked:
						libtcod.console_put_char_ex(con, x, y, CHAR_WALL, COLOR_DARK_WALL_FG, COLOR_DARK_WALL_BG)
					else:
						libtcod.console_put_char_ex(con, x, y, CHAR_GROUND,COLOR_DARK_GROUND_FG,COLOR_DARK_GROUND_BG)

	for obj in objects:
		if obj != player:
			obj.draw()
	player.draw()


	libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)


	if game_state == STATE_TARGET and target_coords[0] != None:

		if temp_spell != None:
			spell = temp_spell['spell']
		else:
			spell = current_spell

		libtcod.console_set_default_background(spell_con, COLOR_TRANSPARENT)
		libtcod.console_clear(spell_con)

		in_range = player.distance_to_point(target_coords[0],target_coords[1]) <= spell['range']
		if in_range:
			spell_fg = COLOR_SPELL_TARGET_FG
			spell_bg = COLOR_SPELL_TARGET_BG
			spell_line_fg = COLOR_SPELL_TARGET_LINE_FG
			spell_line_bg = COLOR_SPELL_TARGET_LINE_BG
		else:
			spell_fg = COLOR_SPELL_TARGET_BAD_FG
			spell_bg = COLOR_SPELL_TARGET_BAD_BG
			spell_line_fg = COLOR_SPELL_TARGET_LINE_BAD_FG
			spell_line_bg = COLOR_SPELL_TARGET_LINE_BAD_BG

		libtcod.line_init(player.x, player.y, target_coords[0],target_coords[1])
		x,y = libtcod.line_step()
		while x is not None:
			libtcod.console_put_char_ex(spell_con, x, y, CHAR_SPELL_PATH, spell_line_fg, spell_line_bg)
			x,y = libtcod.line_step()

		libtcod.console_put_char_ex(spell_con, target_coords[0], target_coords[1], CHAR_SPELL, spell_fg, spell_bg)


		libtcod.console_blit(spell_con, 0, 0, 0, 0, 0, 0, 0, SPELL_TARGET_TRANSPARENCY,SPELL_TARGET_TRANSPARENCY)

	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	y = 1
	for (line, color) in game_messages:
		libtcod.console_set_default_foreground(panel, color)
		libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1

	render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
	render_bar(1, 3, BAR_WIDTH, 'MA', player.fighter.mana, player.fighter.max_mana, libtcod.light_blue, libtcod.darker_blue)

	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,'Spell: %s' % (current_spell['name']))

	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

	libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

##################################################################################################################################
#	Bar Render 																													 #
##################################################################################################################################

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):

	bar_width = int(float(value) / maximum * total_width)

	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
	libtcod.console_set_default_background(panel, bar_color)

	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width // 2, y, libtcod.BKGND_NONE, libtcod.CENTER,'%s: %s/%s' % (name,value,maximum))



##################################################################################################################################
##################################################################################################################################
##																																##
##										   KK     KK  EEEEEEEE  YY      YY   SSSSSSSS 											##
##										   KK    KK   EE         YY    YY   SS       											##
##										   KK   KK    EE          YY  YY    SS       											##
##										   KKKKK      EEEEEEE      YYYY       SSS    											##
##										   KK  KK     EE            YY          SSS  											##
##										   KK    KK   EE            YY             SS											##
##										   KK     KK  EE            YY             SS											##
##										   KK     KK  EEEEEEEE      YY      SSSSSSSS 											##
##																																##			
##################################################################################################################################
##################################################################################################################################


##################################################################################################################################
#	Main Key Handler																											 #
##################################################################################################################################

def handle_keys():
	global game_state, target_coords, current_spell

	if key.vk in KEYS_FULLSCREEN:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk in KEYS_EXIT:
		return ACTION_EXIT

	if game_state == STATE_TARGET:
		if key_match(key, KEYS_CANCEL):
			game_state = STATE_PLAYING
			return ACTION_NONE

		elif key_match(key, KEYS_CONFIRM):
			if temp_spell != None:
				spell = temp_spell['spell']
			else:
				spell = current_spell

			success = spell['cast_function'](spell,target_coords[0],target_coords[1])

			if success == RESULT_CANCELLED:
				return ACTION_NONE

			return ACTION_TURN
			

		elif key_match(key, KEYS_UP):
			move_target(0,-1)
			return ACTION_NONE
	 
	 	elif key_match(key, KEYS_DOWN):
			move_target(0,1)
			return ACTION_NONE
	 	
	 	elif key_match(key, KEYS_LEFT):
			move_target(-1,0)
			return ACTION_NONE
	 	
	 	elif key_match(key, KEYS_RIGHT):
			move_target(1,0)
			return ACTION_NONE

		elif key_match(key, KEYS_UPLEFT):
			move_target(-1,-1)
			return ACTION_NONE
	 
	 	elif key_match(key, KEYS_UPRIGHT):
			move_target(1,-1)
			return ACTION_NONE
	 	
	 	elif key_match(key,  KEYS_DOWNLEFT):
			move_target(-1,1)
			return ACTION_NONE
	 	
	 	elif key_match(key, KEYS_DOWNRIGHT):
			move_target(1,1)
			return ACTION_NONE

		elif key_match(key, KEYS_WAIT):
			return ACTION_TURN

		else:
			return ACTION_NONE

	if game_state == STATE_PLAYING:
		if key_match(key, KEYS_UP):
			player_move_or_attack(0,-1)
			return ACTION_TURN
	 
	 	elif key_match(key, KEYS_DOWN):
			player_move_or_attack(0,1)
			return ACTION_TURN
	 	
	 	elif key_match(key, KEYS_LEFT):
			player_move_or_attack(-1,0)
			return ACTION_TURN
	 	
	 	elif key_match(key, KEYS_RIGHT):
			player_move_or_attack(1,0)
			return ACTION_TURN

		elif key_match(key, KEYS_UPLEFT):
			player_move_or_attack(-1,-1)
			return ACTION_TURN
	 
	 	elif key_match(key, KEYS_UPRIGHT):
			player_move_or_attack(1,-1)
			return ACTION_TURN
	 	
	 	elif key_match(key,  KEYS_DOWNLEFT):
			player_move_or_attack(-1,1)
			return ACTION_TURN
	 	
	 	elif key_match(key, KEYS_DOWNRIGHT):
			player_move_or_attack(1,1)
			return ACTION_TURN

		elif key_match(key, KEYS_WAIT):
			return ACTION_TURN

		elif key_match(key, KEYS_CAST):
			target_coords = (player.x,player.y)
			game_state = STATE_TARGET
			return ACTION_NONE

		elif key_match(key, KEYS_PICKUP):
			for obj in objects:
				if obj.item and obj.x == player.x and obj.y == player.y:
					obj.item.pick_up()
					break
			return ACTION_NONE

		elif key_match(key, KEYS_INVENTORY):
			item = inventory_menu("Press the key next to an item to use it or any other to cancel.\n")
			if item is not None:
				item.use()
			return ACTION_NONE

		elif key_match(key, KEYS_DROP):
			item = inventory_menu("Press the key next to an item to drop it or any other to cancel.\n")
			if item is not None:
				item.drop()
			return ACTION_NONE

		elif key_match(key, KEYS_SPELL):
			spell = spell_menu("Press the key next to an spell to select it or any other to cancel.\n")
			if spell is not None:
				current_spell = spell
			return ACTION_NONE

		else:
			return ACTION_NONE

def key_match(key,keys):
	if key.vk == libtcod.KEY_CHAR:
		return chr(key.c) in keys
	else:
		return key.vk in keys



##################################################################################################################################
##################################################################################################################################
##																																##
##										MM         MM     AAAA     IIIIIIII  NNN     NN											##
##										MMMM     MMMM    AA  AA       II     NNNN    NN											##
##										MM MM   MM MM   AA    AA      II     NN NN   NN											##
##										MM  MM MM  MM  AA      AA     II     NN NN   NN											##
##										MM   MMM   MM  AAAAAAAAAA     II     NN  NN  NN											##
##										MM         MM  AA      AA     II     NN   NN NN											##
##										MM         MM  AA      AA     II     NN    NNNN											##
##										MM         MM  AA      AA  IIIIIIII  NN     NNN											##
##																																##			
##################################################################################################################################
##################################################################################################################################

##################################################################################################################################
#	Monster Definitions																											 #
##################################################################################################################################

monsters = {
	'orc': {
		'name': 'Orc',
		'char': 'O',
		'color': libtcod.desaturated_green,
		'hp': 10,
		'mana': 0,
		'defense': 1,
		'power_min': 2,
		'power_max': 4,
		'death_function': monster_death,
		'ai': BasicMonster
	},
	'troll': {
		'name': 'Troll',
		'char': 'T',
		'color': libtcod.darker_green,
		'hp': 16,
		'mana': 0,
		'defense': 1,
		'power_min': 3,
		'power_max': 5,
		'death_function': monster_death,
		'ai': BasicMonster
	},
	'zombie': {
		'name': 'Zombie',
		'char': 'Z',
		'color': libtcod.copper,
		'hp': 18,
		'mana': 0,
		'defense': 0,
		'power_min': 2,
		'power_max': 4,
		'death_function': monster_death,
		'ai': BasicMonster
	},
	'bat': {
		'name': 'Bat',
		'char': 'B',
		'color': libtcod.silver,
		'hp': 7,
		'mana': 0,
		'defense': 0,
		'power_min': 1,
		'power_max': 3,
		'death_function': monster_death,
		'ai': BasicMonster
	}	
}

##################################################################################################################################
#	Spell Definitions																											 #
##################################################################################################################################

spells = {
	'lightning': {
		'name': 'Lightning Bolt',
		'range': 5,
		'min': 14,
		'max': 25,
		'radius': 1,
		'friendly': False,
		'self': False,
		'enemy': True,
		'cast_function': cast_lightning
	},
	'confuse': {
		'name': 'Confusion',
		'range': 8,
		'min_duration': 5,
		'max_duration': 15,
		'radius': 1,
		'friendly': False,
		'self': False,
		'enemy': True,
		'cast_function': cast_confuse
	},
	'heal': {
		'name': 'Heal',
		'min': 10,
		'max': 25,
		'range': 5,
		'radius': 1,
		'friendly': True,
		'self': True,
		'enemy': True,
		'cast_function': cast_heal
	},
	'fireball': {
		'name': 'Fireball',
		'range': 6,
		'min': 7,
		'max': 12,
		'radius': 2,
		'friendly': False,
		'self': False,
		'enemy': True,
		'cast_function': cast_fireball
	},
}

##################################################################################################################################
#	Item Definitions																											 #
##################################################################################################################################

items = {
	'potions': {
		'healing': {
			'name': 'Minor Healing Potion',
			'spell': spells['heal'],
			'char': '!',
			'color': libtcod.violet,
			'consumable': True
		}
	},
	'scrolls': {
		'lightning': {
		'name': 'Scroll of Minor Lightning',
			'spell': spells['lightning'],
			'char': '<',
			'color': libtcod.darker_blue,
			'consumable': True
		},
		'confuse': {
			'name': 'Scroll of Confusion',
			'spell': spells['confuse'],
			'char': '<',
			'color': libtcod.darker_green,
			'consumable': True
		}
	}
}

##################################################################################################################################
#	Default Player Values																										 #
##################################################################################################################################

player_config = {
	'name': 'Player',
	'char': CHAR_PLAYER,
	'color': libtcod.white,
	'hp': 30,
	'mana': 15,
	'defense': 2,
	'power_min': 4,
	'power_max': 7
}

##################################################################################################################################
##################################################################################################################################
##																																##
##									   SSSSSSSS  EEEEEEEE  TTTTTTTT  UU      UU  PPPPPPPP  										##
##									  SS         EE           TT     UU      UU  PP     PP 										##
##									  SS         EE           TT     UU      UU  PP      PP										##
##									    SSS      EEEEEEE      TT     UU	     UU  PP     PP 										##
##									      SSS    EE           TT     UU      UU  PPPPPPP   										##
##									         SS  EE           TT     UU      UU  PP        										##
##									         SS  EE           TT     UU      UU  PP        										##
##									  SSSSSSSS   EEEEEEEE     TT       UUUUUU    PP        										##
##																																##
##################################################################################################################################
##################################################################################################################################

def save_game():
	savefile = shelve.open('savegame', 'n')

	savefile['map']				= level_map
	savefile['objects'] 		= objects
	savefile['spell_list'] 		= spell_list
	savefile['inventory'] 		= inventory
	savefile['game_messages'] 	= game_messages
	savefile['game_state'] 		= game_state
	savefile['current_spell'] 	= current_spell
	savefile['temp_spell'] 		= temp_spell
	savefile['target_coords'] 	= target_coords
	savefile['player_index'] 	= objects.index(player)

	savefile.close()

def load_game():
	global level_map, objects, spell_list, inventory, game_messages, game_state, current_spell, temp_spell, target_coords, player, game_started

	savefile = shelve.open('savegame', 'r')

	level_map 		= savefile['map']
	objects 		= savefile['objects']
	spell_list 		= savefile['spell_list']
	inventory 		= savefile['inventory']
	game_messages 	= savefile['game_messages']
	game_state		= savefile['game_state']
	current_spell	= savefile['current_spell']
	temp_spell		= savefile['temp_spell']
	target_coords	= savefile['target_coords']
	player 			= objects[savefile['player_index']]

	savefile.close()	

	init_fov()

	game_started = True

def new_game():
	global player, game_state, inventory, spell_list, current_spell, temp_spell, game_messages, game_started

	player = Object(
				x=0, 
				y=0, 
				char=player_config['char'], 
				name=player_config['name'], 
				color=player_config['color'], 
				blocks=True, 
				fighter=Fighter(
					hp=player_config['hp'],
					mana=player_config['mana'],
					defense=player_config['defense'],
					power=(player_config['power_min'],player_config['power_max']), 
					death_function=player_death,
					friendly=True,
					enemy=False
					)
				)

	make_map()

	init_fov()

	game_state = STATE_PLAYING	

	inventory = []
	spell_list = [spells['lightning'],spells['fireball'],spells['confuse'],spells['heal']]
	current_spell = spells['lightning']
	temp_spell = None

	target_coords = (None,None)

	game_messages = []

	game_started = True


	#message('Kill all of the monsters!', libtcod.red)

def play_game():
	global key, mouse, player_action

	player_action = ACTION_NONE

	while not libtcod.console_is_window_closed():

		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)

		render_all()

	 	libtcod.console_flush()
	 	
	 	for obj in objects:
	 		obj.clear()
		
		player_action = handle_keys()

		if player_action == ACTION_TURN:
			for obj in objects:
				if obj.ai:
					obj.ai.take_turn()

		if player_action == ACTION_EXIT: 
			break



libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
spell_con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
libtcod.console_set_key_color(spell_con,COLOR_TRANSPARENT)

mouse = libtcod.Mouse()
key = libtcod.Key()

game_started = False


main_menu()

