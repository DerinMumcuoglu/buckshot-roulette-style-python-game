import random

TURN_ENEMY = 0
TURN_PLAYER = 1
ITEM_HAND_SAW = "Hand Saw"
ITEM_HANDCUFFS = "Handcuffs"
ITEM_MAGNIFYING_GLASS = "Magnifying Glass"
ITEM_TAVUK_PILAV = "Tavuk Pilav"
ITEM_BLOXY_COLA = "Bloxy Cola"
current_turn = TURN_PLAYER
skip_turn = None
bullets = []
player_inventory = []
enemy_inventory = []
items = [ITEM_HANDCUFFS, ITEM_HAND_SAW, ITEM_MAGNIFYING_GLASS, ITEM_TAVUK_PILAV, ITEM_BLOXY_COLA]
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

def show_healths():
    print(f"Player health: {player_health} Enemy health: {enemy_health}\n")

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
 
    for i in range(0, random.randint(2,8)):
        c = random.randint(0,1)
        bullets.append(c)
        if c == 0:
            empty_count += 1
        else:
            loaded_count += 1
loading_bullets()
print(f"Empty count: {empty_count} Loaded count: {loaded_count}")

def reloading_bullets():
    if not bullets:
        print("No more bullets left. Reloading bullets...\n")
        loading_bullets()
        print(f"Empty count: {empty_count} Loaded count: {loaded_count}")

def player_items_function():
    global skip_turn
    global player_health
    global enemy_health


    if player_inventory:
        print(f"\nYour items: {player_inventory}")
        for i, elements in enumerate(player_inventory):
            print(f"{i}. {elements}")
    else:
        print("You have no items left.")
        players_desicion()
        return None

    while True:
        try:
            selected_item_index = int(input("\nUse item (Item number) Exit (666)\n"))

            if selected_item_index in range(0, len(player_inventory)):
                selected_item = player_inventory.pop(selected_item_index)
                print(f"Player used: {selected_item}")
                break
            
            elif selected_item_index == 666:
                players_desicion()
                return None
            
            else:
                print(f"Please enter a number in range of 0 to {len(player_inventory)}\n")

        except ValueError:
                print("Invalid input! Please enter a number.\n")
    
    if selected_item == ITEM_HAND_SAW and bullets[-1] != 2:
        bullets[-1] *= 2

    elif selected_item == ITEM_MAGNIFYING_GLASS:
        if bullets[-1] == 1:
            print(f"The round in the chamber is... Live!")
        elif bullets[-1] == 0:
            print(f"The round in the chamber is... Blank!")
    
    elif selected_item == ITEM_TAVUK_PILAV:
        
        if player_health < 3:
            print(f"You ate the tavuk pilav... It was delicious. (+1 health)")
            player_health += 1
        else:
            print("You ate the tavuk pilav... You are already max health. Nothing happens.")
        print("Player health: ", player_health)

    elif selected_item == ITEM_BLOXY_COLA:
        print("You drink the bloxy cola... It was so bloxy that the last bullet popped.")
        if bullets.pop() == 1:
            print("The popped bullet was... Live!")
        else:
            print("The popped bullet was... Blank!")

    elif selected_item == ITEM_HANDCUFFS:
        if not skip_turn == TURN_ENEMY:
            print("You used the handcuffs, enemy skips a turn.")
            skip_turn = TURN_ENEMY
        else:
            print("Enemy is already handcuffed.")
            player_inventory.append(ITEM_HANDCUFFS)
    
    players_desicion()

def players_desicion():
    global player_health
    global enemy_health
    reloading_bullets()

    while True:
        try:
            a = int(input("\nShoot the enemy (1) Shoot yourself (2) Look at your items (3)\n"))
            if a in range(1,4):
                break
            else:
                print("Invalid input! Please enter 1, 2 or 3")
        except ValueError:
            print("Invalid input! Please enter a number.")
 
    if a == 3:
        player_items_function()
    else:
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
        print("Its players turn again!")        
        players_desicion()

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
        print("Enemy shoots itself! It's a hit.")
        enemy_health -= bullet

    elif r == 2 and bullet == 0:
        print("Enemy shoots itself! It was a blank cartidge.")
        print("Its Enemy's turn again!\n")        
        enemy_desicion()
    

while player_health > 0 and enemy_health > 0:
    if current_turn == TURN_PLAYER:
        players_desicion()
        show_healths()
        if check_death() == True:
            break
        current_turn = TURN_ENEMY

    elif current_turn == TURN_ENEMY:
        enemy_desicion()
        show_healths()
        if check_death() == True:
            break
        current_turn = TURN_PLAYER

    if skip_turn == TURN_ENEMY:
        print("Enemy's turn is skipped!")
        skip_turn = None
        current_turn = TURN_PLAYER