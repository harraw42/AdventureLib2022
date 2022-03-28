from adventurelib import *
Room.items = Bag()

#-- INTRO --
name = input("Your eyes slowly open as the grasp of consciousness slowly grasps you. Light beams between the dense canopy of the cold forest. You have no idea how you got here. All you can remember is your name, which is...")
say(f"Yes, that was your name. {name}. Something about it seems familiar, yet unfamiliar at the same time. You rise and look around at your surroundings. You are in a clearing of a dense forest, and you would estimate the time to be around 8 in the morning on a summers day. You try desperately to remember some sebelance of how you got here or who you are, but as you do, something in your head urges you not to. You notice a strange rock about a metre in front of you. It is glowing with an ominous blue glow. You feel something in your pocket.")

#-- ROOMS --
forest = Room("""
	A clearing in a dense forest. You woke up here.
	""")

strangetree = Room("""
	A claring with a strange tree in its center. This tree is significantly larger than the ones surrounding it and it appears to be leaking some strange glowing blue sap.
	""")

treehouseext = Room("""
	A forest clearing with a large, rotten tree house on a tree in its center, the ladder is still intact, laying rolled up on the ground beneath the treehouse.
	""")

treehouseint = Room("""
	The inside of the large tree house. It smells of mould and you can count several types of fungus in the area around you.
	""")

cliffside = Room("""
	An area where the trees part, revealing a large cliff edge. You stand and pear over the edge, estimating the drop to be about 15 or so metres. Below is a small beach.
	""")

beach = Room("""
	The middle of the small beach. The tide is in. the sound of seagulls chirping unlockes some distant memory, but you feel as if you are unable to access it.
	""")



#-- CONNECTIONS --
forest.east = strangetree
forest.west = treehouseext
strangetree.west = forest
treehouseext.east = forest
forest.south = cliffside
cliffside.north = forest



current_room = forest

#-- ITEMS --
Item.description = ""


strangerock = Item("A strange glowing rock","rock", "strange rock")
strangerock.description = "a weird glowing rock youfound when you woke up. Just looking at it feels...odd, as if you shouldn't be seeing it. A voice in your head tells you to be careful, but you're not sure if it was your own thought or someone, something, else's. Holding it in your hand, you feel as though its buzzing or vibrating slowly in your hand."

fungus = Item("Some assorted mushrooms of various shapes, sizes and colours","mushrooms")
fungus.description = "a bunch of weird looking mushrooms. You are unsure if any of them are edible, and you don't want to find out the hard way."

ladder = Item("A rope ladder","rope ladder")
ladder.description = "a rope ladder you found crankled on the floor under the strange treehouse. It looks tall, maybe 12 metres."

dogtags = Item("A set of dogtags","dogtags")
dogtags.description = f"a set of dogtags with a name and a number enscribed in it. {name}, 23032022."

journal = Item("A sandy journal","journal")
journal.description = f"""
a journal that you found on the beach. Something in your mind feels unlocked. You flip through the pages until something catches your eye. Two pages, side by side with a single phrase written along them. The phrase looks as though it was written in a rush with a bloody finger...it reads: 'CAst ThE SpeLL' followed by a list of, what you would asssume are spells:
Shift - Thrumian Stone + Proof of Spell
"""


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
		print(current_room)
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
			treehouseint.south = treehouseext
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
		if si1 == "strange rock" and inventory.find(si1) and si2 == "journal" and inventory.find(si2):
			say("The stange rock glows brighter with more powerful energy.")
			say("The journal begins flippping through pages by itself, the same glow you can see on the rock is eminating from beneath the pages until it lands on a page with the word 'Shift' sprawled on it.")
			shiftroom = input("Shift allows you to instantly transport to any are in the vacinity. Where do you want to shift to?\n")
			if shiftroom == forest:
				current_room = forest
			if shiftroom == strangetree:
				current_room = strangetree
			if shiftroom == tree:
				current_room = forest
				say(f"You close your eyes and cast Shift. You are now at the {shiftroom}.")
				look()
			else:
				say("That is not a valid room.")
		elif si1 != "strange rock" or si2 != "journal":
			say("That is not the correct item to cast the spell.")
		elif "strange rock" not in inventory or "journal" not in inventory:
			say("You do not have the necessary items for the spell.")



		
#-- MAIN --
def main ():
	start()

if __name__ == '__main__':
	main()