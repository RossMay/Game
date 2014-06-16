from __future__ import division
import libtcodpy as libtcod
import math, textwrap, time, sys

DEBUG = False
DEBUGMSG = False

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

LIMIT_FPS = 20

LEAF_MIN = 8
LEAF_MAX = 20

INVENTORY_WIDTH = 50

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

MAP_WIDTH = 80
MAP_HEIGHT = 43

ROOM_MAX_SIZE = 20
ROOM_MIN_SIZE = 8
MAX_ROOMS = 30

RANDOM_HALLS = 10

MAX_ROOM_MONSTERS = 3
MAX_ROOM_ITEMS = 2

STATE_PLAYING = 0
STATE_DEAD = 1

ACTION_NONE = 0
ACTION_EXIT = 1

RESULT_CANCELLED = 0

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
if DEBUG:
	LIGHT_RADIUS = 1000
else:
	LIGHT_RADIUS = 10

CHAR_PLAYER = '@'
CHAR_NPC    = 'N'
CHAR_WALL   = '#'
CHAR_GROUND = '.'
CHAR_OTHER  = ' '
CHAR_CORPSE = '%'

KEYS_UP = [libtcod.KEY_UP]
KEYS_DOWN = [libtcod.KEY_DOWN]
KEYS_LEFT = [libtcod.KEY_LEFT]
KEYS_RIGHT = [libtcod.KEY_RIGHT]
KEYS_PICKUP = [',']
KEYS_EXIT = [libtcod.KEY_ESCAPE]
KEYS_FULLSCREEN = [libtcod.KEY_F11]
KEYS_INVENTORY = ['i']

COLOR_DARK_WALL_BG = libtcod.Color(0,0,0)
COLOR_DARK_WALL_FG = libtcod.Color(41,16,2)
COLOR_LIGHT_WALL_BG = libtcod.Color(0,0,0)
COLOR_LIGHT_WALL_FG = libtcod.Color(85,41,15)

COLOR_DARK_GROUND_BG = libtcod.Color(0,0,0)
COLOR_DARK_GROUND_FG = libtcod.Color(39,39,39)
COLOR_LIGHT_GROUND_BG = libtcod.Color(0,0,0)
COLOR_LIGHT_GROUND_FG = libtcod.Color(129,129,129)

spells = {
	'lightning': {
		'range': 5,
		'min': 14,
		'max': 25
	},
	'confuse': {
		'range': 8,
		'min_duration': 5,
		'max_duration': 15
	}
}

items = {
	'potions':{
		'healing':{
			'min': 10,
			'max': 25
		}
	}
}

class Leaf:
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
		elif libtcod.random_get_int(0,1,100) > 50:
			return lroom
		else:
			return rroom
		
	def get_random_room(self):
		if self.room != None:
			return self.room

		if self.left != None or self.right != None:
			return self.left.get_random_room() if libtcod.random_get_int(0,1,100) > 50 else self.right.get_random_room()
		else:
			return None

	def split(self):
		if DEBUGMSG: print "Splitting %s %s..." % (self.x, self.y),
		if self.left != None or self.right != None:
			if DEBUGMSG: print "Already split"
			return False
		random = False

		if (self.width > self.height) and (self.height/self.width) <=  0.25:
			if DEBUGMSG: print "vsplit %f" % (self.height/self.width),
			split = False
		elif (self.height > self.width) and (self.width / self.height) <= 0.25:
			if DEBUGMSG: print "hsplit % f" % (self.width / self.height),
			split = True
		else:
			if DEBUGMSG: print "random",
			random = True
			split = libtcod.random_get_int(0,1,100) > 50

		maxlen = (self.height if split else self.width) - LEAF_MIN

		if maxlen < LEAF_MIN:
			if DEBUGMSG: print "Too small, not splitting"
			return False

		splitspot = libtcod.random_get_int(0,LEAF_MIN, maxlen)
		if DEBUGMSG: print "%s w - %s h - %s max - %f spot - %f" % (("Horizontal" if split else "Vertical"), self.width, self.height, maxlen, splitspot)

		if split:
			self.left = Leaf(self.x, self.y, self.width, splitspot)
			self.right = Leaf(self.x, self.y + splitspot, self.width, self.height - splitspot)
		else:
			self.left = Leaf(self.x, self.y, splitspot, self.height)
			self.right = Leaf(self.x + splitspot, self.y, self.width - splitspot, self.height)
		
		if self.left.width > LEAF_MAX or self.left.height > LEAF_MAX or libtcod.random_get_int(0,1,100) > 715:
			if DEBUGMSG: print "Left ",
			self.left.split()
		if self.right.width > LEAF_MAX or self.right.height > LEAF_MAX or libtcod.random_get_int(0,1,100) > 175:
			if DEBUGMSG: print "Right ",
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
			w = libtcod.random_get_int(0,ROOM_MIN_SIZE,self.width - 1)
			h = libtcod.random_get_int(0,ROOM_MIN_SIZE,self.height - 1)

			rx = libtcod.random_get_int(0, 0, self.width - w - 1)
			ry = libtcod.random_get_int(0, 0, self.height - h - 1)

			self.room = Rect(self.x + rx, self.y + ry, w, h)
			
			if DEBUGMSG: print "MR POS: (%s,%s) LD: (%sx%s) RP: (%s,%s) RD: (%sx%s)" % (self.x,self.y,self.width,self.height,self.room.x1,self.room.y1,w,h)
			for x in range(self.room.x1 + 1, self.room.x2):
				for y in range(self.room.y1 + 1, self.room.y2):
					level_map[x][y].blocked = False
					level_map[x][y].block_sight = False

			place_objects(self.room)



class Item:
	def __init__(self, value=None, consumable=False, use_function=None):
		self.use_function = use_function
		self.consumable = consumable
		self.value = value

	def use(self):
		if self.use_function is None:
			message('The %s cannot be used.' % self.owner.name)
		else:
			if self.use_function(self.value) != RESULT_CANCELLED and self.consumable:
				inventory.remove(self.owner)


	def pick_up(self):
		if len(inventory) >= 26:
			message('Your inventory is full, cannot pick up  %s.' % self.owner.name, libtcod.red)
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			message("You picked up a %s." % self.owner.name, libtcod.green)

class Fighter:
	def __init__(self, health, mana, defense, power, death_function=None):
		self.death_function = death_function
		self.max_health = health
		self.health = health
		self.max_mana = mana
		self.mana = mana
		self.defense = defense
		self.power = power

	def take_damage(self, damage):
		if damage > 0:
			self.health -= damage

		if self.health <= 0:
			self.health = 0
			function = self.death_function
			if function is not None:
				function(self.owner)

	def attack(self, target):
		damage = self.power - target.fighter.defense

		if damage > 0:
			message("%s attacks %s for %s damage." % (self.owner.name.capitalize(), target.name, damage), libtcod.white)
			target.fighter.take_damage(damage)
		else:
			message("%s attacks %s but it does nothing." % (self.owner.name.capitalize(), target.name), libtcod.white)

	def heal(self, amount):
		self.health += amount
		if self.health > self.max_health:
			self.health = self.max_health

class BasicMonster:
	def take_turn(self):
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)

			elif player.fighter.health > 0:
				monster.fighter.attack(player)

class ConfusedMonster:
	def __init__(self, old_ai, duration=int((spells['confuse']['min_duration'] + spells['confuse']['max_duration']) / 2)):
		self.old_ai = old_ai
		self.duration = duration
	def take_turn(self):
		if self.duration > 0:
			self.owner.move(libtcod.random_get_int(0,-1,1), libtcod.random_get_int(0,-1,1))
			self.duration -= 1
		else:
			self.owner.ai = self.old_ai
			message('The %s is no longer confused.', libtcod.red)

class Object:
	def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None, item=None):
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

def cast_heal(value):
	if len(value) > 1:
		vmin = value[0]
		vmax = value[1]
	else:
		vmin = vmax = value

	amount = libtcod.random_get_int(0, vmin, vmax)

	if player.fighter.health == player.fighter.max_health:
		message('You are already at full health.', libtcod.red)
		return RESULT_CANCELLED
	
	message('You restored %s health!' % amount, libtcod.light_green)
	player.fighter.heal(amount)

def cast_lightning(value):

	if len(value) > 1:
		vmin = value[0]
		vmax = value[1]
	else:
		vmin = vmax = value

	damage = libtcod.random_get_int(0, vmin, vmax)

	monster = closest_monster(spells['lightning']['range'])
	if monster is None:
		message('No enemy in range.', libtcod.red)
		return RESULT_CANCELLED

	message('Lightning strikes %s for %s damage.' % (monster.name, damage), libtcod.light_blue)
	monster.fighter.take_damage(damage)

def cast_confuse(value):
	if len(value) > 1:
		vmin = value[0]
		vmax = value[1]
	else:
		vmin = vmax = value

	duration = libtcod.random_get_int(0, vmin, vmax)

	monster = closest_monster(spells['confuse']['range'])
	if monster is None:
		message('No enemy in range.', libtcod.red)
		return RESULT_CANCELLED

	old_ai = monster.ai
	monster.ai = ConfusedMonster(old_ai, duration=duration)
	monster.ai.owner = monster
	message('The %s is now confused for %s turns.' % (monster.name, duration), libtcod.light_blue)

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

def is_blocked( x, y):
		if level_map[x][y].blocked:
			return True

		for obj in objects:
			if obj.blocks and obj.x == x and obj.y == y:
				return True

		return False

def place_objects(room):
	global spells, items
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

	for i in range(num_monsters):
		while True:
			x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
			y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

			if not is_blocked(x,y):
				break

		chance = libtcod.random_get_int(0, 0, 100)

		if chance < 20:
			monster = Object(x, y, 'O', 'Orc', libtcod.desaturated_green, blocks=True, fighter=Fighter(10,0,0,3, death_function=monster_death), ai=BasicMonster())
		elif chance < 20+40:
			monster = Object(x, y, 'T', 'Troll', libtcod.darker_green, blocks=True, fighter=Fighter(16,0,1,4, death_function=monster_death), ai=BasicMonster())
		elif chance < 20+40+30:
			monster = Object(x, y, 'Z', 'Zombie', libtcod.copper, blocks=True, fighter=Fighter(12,0,0,2, death_function=monster_death), ai=BasicMonster())
		else:
			monster = Object(x, y, 'B', 'Bat', libtcod.silver, blocks=True, fighter=Fighter(7,0,0,1, death_function=monster_death), ai=BasicMonster())

		objects.append(monster)

	num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)
	for i in range(num_items):
		while True:
			x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
			y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

			if not is_blocked(x, y):
				break

		chance = libtcod.random_get_int(0, 0, 100)

		if chance < 50:
			item = Object(x, y, '!', 'healing potion', libtcod.violet, item=Item(consumable=True, use_function=cast_heal, value=(items['potions']['healing']['min'],items['potions']['healing']['max'])))
		elif chance < 50 + 25:
			item = Object(x, y, '<', 'lightning bolt', libtcod.blue, item=Item(consumable=True, use_function=cast_lightning, value=(spells['lightning']['min'],spells['lightning']['max'])))
		else:
			item = Object(x, y, '<', 'confuse', libtcod.darker_green, item=Item(consumable=True, use_function=cast_confuse, value=(spells['confuse']['min_duration'],spells['confuse']['max_duration'])))

		objects.append(item)
		item.send_to_back()

def create_hall(room1, room2):

	prev_x, prev_y = room1.center()
	new_x, new_y = room2.center()

	if libtcod.random_get_int(0, 0, 1) == 1:
		create_h_tunnel(prev_x, new_x, prev_y)
		create_v_tunnel(prev_y, new_y, new_x)
	else:
		create_v_tunnel(prev_y, new_y, new_x)
		create_h_tunnel(prev_x, new_x, prev_y)

def create_h_tunnel(x1, x2, y):
	global level_map
	
	for x in range(min(x1, x2), max(x1, x2) + 1):
		level_map[x][y].blocked = False
		level_map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
	global level_map

	for y in range(min(y1, y2), max(y1, y2) + 1):
		level_map[x][y].blocked = False
		level_map[x][y].block_sight = False

def make_map():
	global level_map, player

	level_map = [[ Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

	leafs = []
	root_leaf = Leaf(0, 0, MAP_WIDTH, MAP_HEIGHT)
	root_leaf.split()

	root_leaf.create_rooms()

	for i in range(RANDOM_HALLS):
		create_hall(root_leaf.get_random_room(),root_leaf.get_random_room())

	player.x, player.y = root_leaf.get_random_room().center()


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

	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	y = 1
	for (line, color) in game_messages:
		libtcod.console_set_default_foreground(panel, color)
		libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1

	render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.health, player.fighter.max_health, libtcod.light_red, libtcod.darker_red)
	render_bar(1, 3, BAR_WIDTH, 'MA', player.fighter.mana, player.fighter.max_mana, libtcod.light_blue, libtcod.darker_blue)

	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

	libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)


def handle_keys():
	global game_state, key

	#key = libtcod.console_wait_for_keypress(True)

	if key.vk in KEYS_FULLSCREEN:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk in KEYS_EXIT:
		return ACTION_EXIT

	if game_state == STATE_PLAYING:
		if key.vk in KEYS_UP:
			player_move_or_attack(0,-1)
	 
	 	elif key.vk in KEYS_DOWN:
			player_move_or_attack(0,1)
	 	
	 	elif key.vk in KEYS_LEFT:
			player_move_or_attack(-1,0)
	 	
	 	elif key.vk in KEYS_RIGHT:
			player_move_or_attack(1,0)

		else:
			key_char = chr(key.c)

			if key_char in KEYS_PICKUP:
				for obj in objects:
					if obj.item and obj.x == player.x and obj.y == player.y:
						obj.item.pick_up()
						break
			elif key_char in KEYS_INVENTORY:
				item = inventory_menu("Press the key next to an item to use it or any other to cancel.\n")
				if item is not None:
					item.use()

			return ACTION_NONE

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):

	bar_width = int(float(value) / maximum * total_width)

	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
	libtcod.console_set_default_background(panel, bar_color)

	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width // 2, y, libtcod.BKGND_NONE, libtcod.CENTER,'%s: %s/%s' % (name,value,maximum))

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

def menu(header, options, width):
	if len(options) > 26: 
		raise ValueError('Cannot have a menu with more than 26 items')

	header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
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

def inventory_menu(header):
	if len(inventory) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory]

	index = menu(header, options, INVENTORY_WIDTH)

	if index is None or len(inventory) == 0: return None
	return inventory[index].item


libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Game', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)


player = Object(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, CHAR_PLAYER, "Player", libtcod.white, blocks=True, fighter=Fighter(30,15,2,5, death_function=player_death))

game_state = STATE_PLAYING
player_action = ACTION_NONE

mouse = libtcod.Mouse()
key = libtcod.Key()

objects = [player]
inventory = []

game_messages = []

message('Welcome stranger! Prepare to perish in the Tombs of the Ancient Kings.', libtcod.red)

make_map()

fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		if DEBUG:
			libtcod.map_set_properties(fov_map, x, y, True, True)
		else:
			libtcod.map_set_properties(fov_map, x, y, not level_map[x][y].block_sight, not level_map[x][y].blocked)

fov_recompute = True

while not libtcod.console_is_window_closed():

	libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)

	render_all()

 	libtcod.console_flush()
 	
 	for obj in objects:
 		obj.clear()
	
	player_action = handle_keys()

	if game_state == STATE_PLAYING and player_action != ACTION_NONE:
		for obj in objects:
			if obj.ai:
				obj.ai.take_turn()

	if player_action == ACTION_EXIT: 
		break