from adventurelib import *
Room.items = Bag()
import random

#-- INTRO --
name = input("Your eyes slowly open as the grasp of consciousness slowly grasps you. Light beams between the dense canopy of the cold forest. You have no idea how you got here. All you can remember is your name, which is...")
say(f"Yes, that was your name. {name}. Something about it seems familiar, yet unfamiliar at the same time. You rise and look around at your surroundings. You are in a clearing of a dense forest, and you would estimate the time to be around 8 in the morning on a summers day. You try desperately to remember some sebelance of how you got here or who you are, but as you do, something in your head urges you not to. You notice a strange rock about a metre in front of you. It is glowing with an ominous blue glow. You feel something in your pocket.")

#-- ROOMS --
forest = Room("""
	in a clearing in a dense forest. You woke up here.
	""")

strangetree = Room("""
	in a claring with a strange tree in its center. This tree is significantly larger than the ones surrounding it and it appears to be leaking some strange glowing blue sap.
	""")

treehouseext = Room("""
	in a forest clearing with a large, rotten tree house on a tree in its center, the ladder is still intact, laying rolled up on the ground beneath the treehouse.
	""")

treehouseint = Room("""
	inside of a large tree house. It smells of mould and you can count several types of fungus in the area around you.
	""")

cliffside = Room("""
	in an area where the trees part, revealing a large cliff edge. You stand and pear over the edge, estimating the drop to be about 15 or so metres. Below is a small beach.
	""")

beach = Room("""
	on a small beach. The tide is in. the sound of seagulls chirping unlockes some distant memory, but you feel as if you are unable to access it.
	""")



#-- CONNECTIONS --
forest.east = strangetree
forest.west = treehouseext
strangetree.west = forest
treehouseext.east = forest
forest.south = cliffside
cliffside.north = forest
treehouseint.south = treehouseext


current_room = forest

#-- ITEMS --
Item.description = ""


strangerock = Item("A strange glowing rock","rock", "strange rock", "thrumian stone")
strangerock.description = "a weird glowing rock youfound when you woke up. Just looking at it feels...odd, as if you shouldn't be seeing it. A voice in your head tells you to be careful, but you're not sure if it was your own thought or someone, something, else's. Holding it in your hand, you feel as though its buzzing or vibrating slowly in your hand."

fungus = Item("Some assorted mushrooms of various shapes, sizes and colours","mushrooms")
fungus.description = "a bunch of weird looking mushrooms. You are unsure if any of them are edible, and you don't want to find out the hard way."

ladder = Item("A rope ladder","rope ladder")
ladder.description = "a rope ladder you found crankled on the floor under the strange treehouse. It looks tall, maybe 12 metres."

dogtags = Item("A set of dogtags","dogtags")
dogtags.description = f"a set of dogtags with a name and a number enscribed in it. {name}, 23032022."

journal = Item("A sandy journal","journal", "proof of spell")
journal.description = f"""
a journal that you found on the beach. Something in your mind feels unlocked. You flip through the pages until something catches your eye. Two pages, side by side with a single phrase written along them. The phrase looks as though it was written in a rush with a bloody finger...it reads: 'CAst ThE SpeLL' followed by a list of, what you would asssume are spells:
Shift - Thrumian Stone + Proof of Spell
Focus Energy - Thrumian Stone + Proof of Spell + Slicing Instrument
"""

bottleshard = Item("A shard of glass", "glass shard", "slicing instrument", "shard")
bottleshard.description = "a shard of glass, probably from a bottle of some sort of liquor."


#-- BAGS --
inventory = Bag()



#-- ITEMS IN BAGS --
inventory.add(dogtags)

forest.items.add(strangerock)
treehouseext.items.add(ladder)
treehouseint.items.add(fungus)
beach.items.add(journal)

#-- FUNCTIONS --
@when("go DIRECTION")
@when("travel DIRECTION")
def travel(direction):
	global current_room
	if direction in current_room.exits():
		#checks if the current room list of exits has 
		#the direction the player wants to go
		current_room = current_room.exit(direction)
		print(f"You go {direction}")
		print(f"You are {current_room}")
	elif direction == south and current_room == treehouseint:
		say("You jump down")
		print(f"You are {current_room}")
	else:
		print("You can't go that way")


@when("use ITEM")
def use(item):
	if current_room == cliffside and item == "keypad":
		player_keypad_attempt = int(input("What would you like to input into the keypad?\n"))
		if player_keypad_attempt == 23032022:
			say("The keypad beeps a higher note and the ground begins to shake. You rush to the cliff edge and watch as the cliff face morphs and rumbles until a set of stairs extends from it with a metallic groan. You can now traverse down towards the beach.")
			cliffside.south = beach
			beach.north = cliffside
		else:
			say("The keypad beeps a low note and nothing happens. Maybe there's something with the combination on it nearby.")
	elif item == "keypad":
		say("There is no keypad in this room.")
	else:
		if inventory.find(item) == ladder and current_room == treehouseext:
			print("You unroll the rope ladder and secure it in place. You can now move up and down the ladder.")
			print("You can now enter the treehouse")
			treehouseext.north = treehouseint
		else:
			print("You can't use that here")



@when ("look")
@when ("look around")
def look():
	print(f"You look around at which room you could go into next. Your options are: {current_room.exits()}")
	#checks to seee if there is at least 1 item in the room
	if len(current_room.items) > 0:
		print("You also see:")
		for item in current_room.items:
			print(item)
	elif current_room == cliffside:
		say("You think you see something in a bush to your right. Upon further inspection, you realize its a keypad. As you near it, the display on the front lights up with artificial green, neon text. It looks as though it requires an 8 digit combination.")

@when ("get ITEM")
@when ("pick up ITEM")
@when ("take ITEM")
def pickup(item):
	if item in current_room.items:
		#aquires the item from the room
		t = current_room.items.take(item)
		inventory.add(t)
		print(f"You get the {item}")
	else:
		print("You don't see anything to pick up in this room.")

@when("inventory")
@when("inv")
@when("show inv")
@when("show inventory")
@when("check inv")
@when("check inventory")
def player_inventory():
	print("You are carrying...")
	for item in inventory:
		print(item)

@when ("look at ITEM")
def look_at(item):
	if item in inventory:
		t = inventory.find(item)
		print(f"You look at {item}")
		print(f"It's {t.description}")
	else:
		print(f"You aren't carrying a {item}.")


@when ("drop ITEM")
def drop(item):
	if item in inventory:
		t = inventory.find(item)
		print(f"You drop {item}")
		#removes the item from inventory and adds it to the room
		inventory.remove(t)
		current_room.items.add(t)
	else:
		print(f"You aren't carrying a {item}.")


@when ("cast SPELL")
def cast(spell):
	if spell == "shift":
		si1 = input("Please input the first necessary spell item.\n")
		si2 = input("Please input the second necessary spell item.\n")
		if si1 == "strange rock" or si1 == "rock" or si1 == "thrumian stone" and inventory.find(si1) and si2 == "journal" or si2 == "proof of spell" and inventory.find(si2):
			say("The stange rock glows brighter with more powerful energy.")
			say("The journal begins flippping through pages by itself, the same glow you can see on the rock is eminating from beneath the pages until it lands on a page with the word 'Shift' sprawled on it.")
			say("Shift allows you to randomly transport to any are in the vacinity.")
			shiftroom = random.randint(1, 6)
			if shiftroom == 1:
				current_room = forest
			if shiftroom == 2:
				current_room = strangetree
			if shiftroom == 3:
				current_room = treehouseext
			if shiftroom == 4:
				current_room = treehouseint
			if shiftroom == 5:
				current_room = cliffside
			if shiftroom == 6:
				current_room = beach
			say(f"You close your eyes and cast Shift. You are now at the {current_room}.")
			print(f"You are {current_room}")
			look()
		elif si1 != "strange rock" or si1 != "rock" or si1 != "thrumian stone" or si2 != "journal" or si2 != "proof of spell":
			say("That is not the correct item to cast the spell.")
		elif "strange rock" not in inventory or "journal" not in inventory:
			say("You do not have the necessary items for the spell.")
	elif spell == "focus energy":
		if focused == False:
			fe1 = input("Please input the first necessary spell item.\n")
			fe2 = input("Please input the second necessary spell item.\n")
			fe3 = input("Please input the third necessary spell item.\n")
			if fe1 == "strange rock" or fe1 == "rock" or fe1 == "thrumian stone" and inventory.find(fe1) and fe2 == "journal" or fe2 == "proof of spell" and inventory.find(fe2) and fe3 == "shard of glass" or fe3 == "slicing instrument" or fe3 == "glass shard" or fe3 == "shard" and inventory.find(fe3):
				say("The stange rock glows brighter with more powerful energy.")
				say("The journal begins flippping through pages by itself, the same glow you can see on the rock is eminating from beneath the pages until it lands on a page with the words 'Focus Energy' sprawled on it.")
				say("The glass shard begins to float, dancing and diving through the air around you until it begins to float around your left arm. It plunges down suddenly, refracting with magical energy, and slices deeply into your forearm before hitting the floor and shattering. You recoil in pain, but none comes. Only anger. You feel a fury you have never felt before, and you clench your fists, hard. You want to hit something.")
				focused == True
			elif fe1 != "strange rock" or fe1 != "rock" or fe1 != "thrumian stone" or fe2 != "journal" or fe2 != "proof of spell" or fe3 != "shard of glass" or fe3 != "slicing instrument" or fe3 != "glass shard" or fe3 != "shard":
				say("That is not the correct item to cast the spell.")
			elif "strange rock" not in inventory or "journal" not in inventory or "glass shard" not in inventory:
				say("You do not have the necessary items for the spell.")
		else:
			say("You feel the anger leave you as you cast the spell again. You return to your normal passive self. Everything is going to be okay. Don't let the anger take over, it'll all be over soon...")
			focused == False
		
#-- MAIN --
def main ():
	start()

if __name__ == '__main__':
	main()