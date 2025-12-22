import random

ITEM_HAND_SAW = "Hand Saw"
ITEM_HANDCUFFS = "Handcuffs"
ITEM_TAVUKPILAV = "Tavuk Pilav"
ITEM_MAGNIFYING_GLASS = "Magnifying Glass"
 
TURN_PLAYER = 0
TURN_ENEMY = 1
 
bullets = []
items = [ITEM_HAND_SAW, ITEM_HANDCUFFS, ITEM_MAGNIFYING_GLASS, ITEM_TAVUKPILAV]
player_inventory = []
enemy_inventory = []
empty_count = 0
loaded_count = 0
player_health = 3
enemy_health = 3
selected_item_index = -1
current_turn = TURN_PLAYER
 
def loading_inventorys():
    for i in range(0,2):
        q = random.choice(items)
        player_inventory.append(q)
        w = random.choice(items)
        enemy_inventory.append(w)
 
loading_inventorys()
 
def items_functions():
    if selected_item_index == -1:
        return
    selected_item = player_inventory[selected_item_index]
    if selected_item == ITEM_HAND_SAW:
        bullets[-1] *= 2
 
print("Player items:",player_inventory)
print("Enemy items:",enemy_inventory)
 
def loading_bullets():
    global empty_count
    global loaded_count
    empty_count = 0
    loaded_count = 0
 
    for i in range(0, random.randint(2,2)):
        c = 0
        bullets.append(c)
        if c == 0:
            empty_count += 1
        else:
            loaded_count += 1
loading_bullets()
print(f"Empty count: {empty_count} Loaded count: {loaded_count}")
 
def reloading_bullets():
    if not bullets:
        print("\nNo more bullets left. Reloading bullets...\n")
        loading_bullets()
        print(f"Empty count: {empty_count} Loaded count: {loaded_count}")
 
def check_death():
        if enemy_health == 0:
            print("Player won")
            return True
        elif player_health == 0:
            print("Enemy won")
            return True
        return False
 
def players_desicion():
    global player_health
    global enemy_health
    reloading_bullets()
 
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
        print("Your items:")
        for i, elements in enumerate(player_inventory):
            print(f"{i}. {elements}")
        b = input("Use item (Item number) Exit (x)\n")
        if b in player_inventory:
            player_inventory.remove[f"{b}"]
            print(player_inventory)
            # items_functions()
            players_desicion()
        if b == "x":
            players_desicion()
    bullet = bullets.pop()        
    if a == 1 and bullet > 0:
        print("Player attacks! It's a hit.")
        enemy_health -= bullet
    elif a == 1 and bullet == 0:
        print("Player attacks! It's a miss.")
    elif a == 2 and bullet > 0:
        print("Player shoots itself It's a hit.")
        player_health -= bullet
    elif a == 2 and bullet == 0:
        print("Player shoots itself! It was a blank cartidge")
        players_desicion()
 
    if player_health > 0:
        print(f"Players health: {player_health} Enemy health: {enemy_health}")
 
def enemy_desicion():
    global player_health
    global enemy_health
    reloading_bullets()
 
    r = random.randint(1,2)
    bullet = bullets.pop()
    if r == 1 and bullet == 1:
        print("Enemy attacks! It's a hit.")
        player_health -= bullet
    elif r == 1 and bullet == 0:
        print("Enemy attacks! It's a miss.")
    elif r == 2 and bullet == 1:
        print("Enemy shoots itself It's a hit.")
        enemy_health -= bullet
    elif r == 2 and bullet == 0:
        print("Enemy shoots itself! It was a blank cartidge")
        enemy_desicion()
   
    if enemy_health > 0:
        print(f"Players health: {player_health} Enemy health: {enemy_health}")
 
while player_health > 0 and enemy_health > 0:
   
    players_desicion()
    if check_death() == True:
        break
    enemy_desicion()
    if check_death():
        break