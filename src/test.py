import random

ITEM_HAND_SAW = "Hand Saw"
ITEM_HANDCUFFS = "Handcuffs"
ITEM_MAGNIFYING_GLASS = "Magnifying Glass"
ITEM_TAVUK_PILAV = "Tavuk Pilav"

bullets = []
player_inventory = []
enemy_inventory = []
items = [ITEM_HAND_SAW, ITEM_HANDCUFFS, ITEM_MAGNIFYING_GLASS, ITEM_TAVUK_PILAV]
selected_item_index = -1
player_health = 3
enemy_health = 3

def check_death():
        if enemy_health == 0:
            print("Player won")
            return True
        elif player_health == 0:
            print("Enemy won")
            return True
        return False

def loading_inventorys():
    for i in range(0,2):
        q = random.choice(items)
        player_inventory.append(q)
        w = random.choice(items)
        enemy_inventory.append(w)

loading_inventorys()
print("Player items:",player_inventory)
print("Enemy items:",enemy_inventory)

def loading_bullets():
    global empty_count
    global loaded_count
    empty_count = 0
    loaded_count = 0
 
    for i in range(0, random.randint(8,8)):
        c = 1
        bullets.append(c)
        if c == 0:
            empty_count += 1
        else:
            loaded_count += 1
loading_bullets()
print(f"Empty count: {empty_count} Loaded count: {loaded_count}")

def player_items_function():
    global player_health
    global enemy_health
    
    selected_item_index = int(input("Use item (Item number) Exit (666)\n"))
    selected_item = player_inventory[selected_item_index]
    if selected_item_index == 666:
        players_desicion()

    if selected_item == ITEM_HAND_SAW:
        bullets[-1] *= 2

    elif selected_item == ITEM_MAGNIFYING_GLASS:
        print(f"The bullet in the chamber is... {bullets[-1]}")
    
    elif selected_item == ITEM_TAVUK_PILAV:
        print(f"You ate the tavuk pilav... It was delicious. (+1 health)")
        if player_health < 3:
            player_health += 1
        print(player_health)

    if selected_item_index in range(0, len(player_inventory)):
        selected_item = player_inventory.pop(selected_item_index)
        print(f"Player used: {selected_item}")
        players_desicion()

    

def players_desicion():
    global enemy_health
    while True:
        try:
            a = int(input("Shoot the enemy (1) Shoot yourself (2) Look at your items (3)\n"))
            if a in range(1,4):
                break
            else:
                print("Invalid input! Please enter 1 or 2")
        except ValueError:
            print("Invalid input! Please enter a number.")
 

    if a == 3:
        print(f"Your items: {player_inventory}")
        for i, elements in enumerate(player_inventory):
            print(f"{i}. {elements}")
        player_items_function()
    if a == 1:
        bullet = bullets.pop()
        enemy_health -= bullet
        print("Enemy health: ",enemy_health)

def enemy_desicion():
    global player_health
    global enemy_health
 
    r = 1
    bullet = bullets.pop()
    if r == 1 and bullet == 1:
        print("Enemy attacks! It's a hit.")
        player_health -= bullet
        print(f"Player health: {player_health}")
    elif r == 1 and bullet == 0:
        print("Enemy attacks! It's a miss.")
    

while player_health > 0 and enemy_health > 0:
   
    players_desicion()
    if check_death() == True:
        break
    enemy_desicion()
    if check_death():
        break