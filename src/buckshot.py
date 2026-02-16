import random
import time
import sys
import os
from inputimeout import inputimeout

TURN_DEALER = 0
TURN_PLAYER = 1
ITEM_HAND_SAW = "Hand Saw"
ITEM_HANDCUFFS = "Handcuffs"
ITEM_MAGNIFYING_GLASS = "Magnifying Glass"
ITEM_TAVUK_PILAV = "Tavuk Pilav"
ITEM_BLOXY_COLA = "Bloxy Cola"
ITEM_ADRENALINE = "Adrenaline"
ITEM_LUCKY_BLOCK = "Lucky Block"
ITEM_EXPIRED_MEDICINE = "Expired Medicine"
ITEM_INVERTER = "Inverter"
ITEM_BURNER_PHONE = "Burner Phone"
current_turn = TURN_PLAYER
skip_turn = None
player_cant_use_handcuffs_second_time = False
bullets = []
player_inventory = []
dealer_inventory = []
items = [ITEM_HAND_SAW, ITEM_HANDCUFFS, ITEM_MAGNIFYING_GLASS, ITEM_TAVUK_PILAV, ITEM_BLOXY_COLA, ITEM_LUCKY_BLOCK, ITEM_ADRENALINE, ITEM_EXPIRED_MEDICINE, ITEM_INVERTER, ITEM_BURNER_PHONE]
items_without_luckyblock = [ITEM_HAND_SAW, ITEM_HANDCUFFS, ITEM_MAGNIFYING_GLASS, ITEM_TAVUK_PILAV, ITEM_BLOXY_COLA, ITEM_ADRENALINE, ITEM_EXPIRED_MEDICINE, ITEM_INVERTER, ITEM_BURNER_PHONE]
dealer_used_mglass = False
dealer_gonna_know_that_round = {""}
dealer_knows_the_current_bullet = False
dealer_handsaw_case = False

max_player_health = 4
current_player_health = 4
max_dealer_health = 4
current_dealer_health = 4

# colors
color_green = "\x1b[92m"
color_yellow = "\x1b[33m"
color_red = "\x1b[91m"
color_blue = "\x1b[34m"
color_orange = "\x1b[38;5;202m"
color_purple = "\x1b[38;5;93m"
color_default = "\x1b[0m"

os.system("cls")

def delayed_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.015)


def check_death():
        if current_dealer_health == 0:
            delayed_print("Player wins")
            return True
        elif current_player_health == 0:
            delayed_print("Dealer wins")
            return True
        return False

def show_healths():
    global max_player_health
    global current_player_health
    global max_dealer_health
    global current_dealer_health

    current_player_health = max(current_player_health, 0)
    current_dealer_health = max(current_dealer_health, 0)


    # display
    bars = 20
    remaining_health_symbol = "█"
    lost_health_symbol = "_"

    # health color update
    if current_player_health == max_player_health:
        health_color = color_green
    elif current_player_health == max_player_health -1 or current_player_health == max_player_health -2:
        health_color = color_yellow
    elif current_player_health == max_player_health -3:
        health_color = color_red
    else:
        health_color = color_default
    
    if current_dealer_health == max_dealer_health:
        dealer_health_color = color_green
    elif current_dealer_health == max_dealer_health -1 or current_dealer_health == max_dealer_health -2:
        dealer_health_color = color_yellow
    elif current_dealer_health == max_dealer_health -3:
        dealer_health_color = color_red
    elif current_dealer_health == max_dealer_health +1:
        dealer_health_color = color_orange
    elif current_dealer_health == max_dealer_health +2:
        dealer_health_color = color_purple
    else:
        dealer_health_color = color_default
    

    # bar update
    remaining_health_bars = round(current_player_health / max_player_health * bars)
    lost_health_bars = bars - remaining_health_bars
    remaining_dealer_health_bars = round(current_dealer_health / max_dealer_health * bars)
    lost_dealer_health_bars = bars - remaining_dealer_health_bars

    # printing stats
    delayed_print(f"\x1b[s\x1b[{1};{0}H|PLayer Health: {current_player_health} / {max_player_health}\t"
        f"{health_color}{remaining_health_bars * remaining_health_symbol}"
          f"{lost_health_bars * lost_health_symbol}{color_default}|"
          f"\t|Dealer Health: {current_dealer_health} / {max_dealer_health}\t"
        f"{dealer_health_color}{remaining_dealer_health_bars * remaining_health_symbol}"
          f"{lost_dealer_health_bars * lost_health_symbol}{color_default}|\x1b[K\x1b[u\n")



show_healths()

def loading_inventorys():
    x = random.sample(items, 4)
    for q in range(2):
        player_inventory.append(x[q])
        x.remove(x[q])
    for w in range(2):
        dealer_inventory.append(x[w])

loading_inventorys()

def reloading_inventorys():
    # return None
    if not player_inventory and current_turn == TURN_DEALER:
        for i in range(0,2):
            q = random.choice(items)
            player_inventory.append(q)

    if not dealer_inventory and current_turn == TURN_PLAYER:
        for i in range(0,2):
            w = random.choice(items)
            dealer_inventory.append(w)

def loading_bullets():
    global empty_count
    global loaded_count
    global cartidge_color
    global cartidge_symbol
    global bars
    empty_count = 0
    loaded_count = 0
    
    cartidge_color = ""

    # display
    bars = len(bullets)
    cartidge_symbol = "▮"
    
    delayed_print("Cartidges in the gun: ")
    for i in range(0, random.randint(4,6)):
        c = random.randint(0,1)
        bullets.append(c)
        if c == 0:
            empty_count += 1
            cartidge_color = color_blue
        else:
            loaded_count += 1
            cartidge_color = color_red
        
        delayed_print(f"{cartidge_color}{cartidge_symbol}")
    
    cartidge_color = color_default
    print(cartidge_color)
    # print(bullets)
    random.shuffle(bullets)
    # print(bullets)
    
loading_bullets()

time.sleep(3)
print("\x1b[A \x1b[2K \x1b[A")


def reloading_bullets():
    if not bullets:
        delayed_print("\nNo more bullets left. Reloading bullets...\n")
        loading_bullets()
        time.sleep(3)
        print("\x1b[2A \x1b[J \x1b[2A")


def dealer_items_function():
    global skip_turn
    global current_player_health
    global current_dealer_health
    global dealer_used_mglass
    global dealer_gonna_know_that_round
    global dealer_handsaw_case

    if dealer_inventory:

        selected_item = random.choice(dealer_inventory)
        dealer_inventory.remove(selected_item)

        if selected_item == ITEM_HAND_SAW and bullets[-1] != 2:
           delayed_print("\nDealer cuts the gun barrel...\n")
           bullets[-1] *= 2
           k = random.randint(1,10)
           if k <= 7:
            dealer_handsaw_case = True
        
        elif selected_item == ITEM_HANDCUFFS:
            if not skip_turn == TURN_PLAYER:
                delayed_print("\nDealer handcuffs you...\n")
                dealer_used_mglass = True
                skip_turn = TURN_PLAYER
        
        elif selected_item == ITEM_MAGNIFYING_GLASS:
            if len(bullets) == 1:
                dealer_inventory.append(ITEM_MAGNIFYING_GLASS)
            else:
                delayed_print("\nDealer inspects the gun with magnifying glass...\n")
                dealer_used_mglass = True

        elif selected_item == ITEM_TAVUK_PILAV:

            if current_dealer_health < 4:
                delayed_print("\nNom Nom Nom...")
                current_dealer_health += 1
                show_healths()
            else:
                dealer_inventory.append(ITEM_TAVUK_PILAV)

        elif selected_item == ITEM_BLOXY_COLA:
            delayed_print("\nGlug glug glug...")
            if bullets.pop() == 1:
                delayed_print("\nThe popped bullet was... Live!\n")
            else:
                delayed_print("\nThe popped bullet was... Blank!\n")

        elif selected_item == ITEM_LUCKY_BLOCK:
            delayed_print(f"\nDealer opens a lucky block...\n")
            random_item = random.choice(items_without_luckyblock)
            dealer_inventory.append(random_item)
            dealer_items_function()

        elif selected_item == ITEM_ADRENALINE:
            
            if player_inventory:
                delayed_print(f"\n{color_red}Dealer injects himself with the adrenaline...")

                random_player_item = random.choice(player_inventory)

                if random_player_item == ITEM_ADRENALINE or skip_turn == TURN_PLAYER and random_player_item == ITEM_HANDCUFFS:
                    delayed_print(f"\nDealer is on demon time! Its doing some sinister things...\n")
                
                player_inventory.remove(random_player_item)
                dealer_inventory.append(random_player_item)
                delayed_print(f"\nDealer steals the {random_player_item} from you!{color_default}\n")
                reloading_inventorys()
                dealer_items_function()

            else:
                dealer_inventory.append(ITEM_ADRENALINE)

        elif selected_item == ITEM_EXPIRED_MEDICINE:
            if current_dealer_health >= 4 < 7:
                current_dealer_health += 1
                delayed_print(f"\nDealer eats the expired medicine... Something unusual happens... (Its the dealer\x1b[6D{color_red}Devil \x1b[6D{color_default}dealer after all)")
                show_healths()
            else:
                current_dealer_health += 1
                delayed_print("\nDealer eats the expired medicine...")
                show_healths()

        elif selected_item == ITEM_INVERTER:
            delayed_print("\nDealer used the inverter... beep boop bop (The polarity of the current shell in the chamber changes.)\n")
            polarity_bullet = bullets.pop()
            if polarity_bullet == 1 or polarity_bullet == 2:
                polarity_bullet = 0
            else:
                polarity_bullet = 1
            bullets.append(polarity_bullet)
        
        elif selected_item == ITEM_BURNER_PHONE:
            delayed_print("\nTorururururu")
            shell_index = random.randint(0, len(bullets)-1)
            dealer_gonna_know_that_round.add(len(bullets)-shell_index)
            delayed_print(f"\nDealer learned the {shell_index + 1}. shell's state. ('1.' means current shell in the chamber)\n")




def player_items_function():
    global skip_turn
    global current_player_health
    global current_dealer_health
    global player_cant_use_handcuffs_second_time
    expired_medicine_special_case = False

    if player_inventory:
        delayed_print(f"\nYour items: {player_inventory}")
        for i, elements in enumerate(player_inventory):
            delayed_print(f"\n{i}. {elements}")
    else:
        delayed_print("\nYou have no items left.\n")
        players_desicion()
        return None

    while True:
        try:
            selected_item_index = int(input("\nUse item (Item number) Exit (666)\n"))

            if len(player_inventory) == 2:

                if selected_item_index in range(0, len(player_inventory)):
                    selected_item = player_inventory.pop(selected_item_index)
                    delayed_print(f"\x1b[6A\x1b[J")
                    break
                
                elif selected_item_index == 666:
                    print("\x1b[5A\x1b[J\x1b[2A")
                    players_desicion()
                    return None
                
            elif len(player_inventory) == 1:
                if selected_item_index in range(0, len(player_inventory)):
                    selected_item = player_inventory.pop(selected_item_index)
                    delayed_print(f"\x1b[5A\x1b[J")
                    break
                
                elif selected_item_index == 666:
                    print("\x1b[4A\x1b[J\x1b[2A")
                    players_desicion()
                    return None
                
        except ValueError:
                print("\x1b[1A\x1b[2K\x1b[3A")
        else:
            print("\x1b[1A\x1b[2K\x1b[3A")

        
    
    if selected_item == ITEM_HAND_SAW and bullets[-1] != 2:
        delayed_print("\nYou used the hand saw... The next cartidge deals double damage.\n")
        bullets[-1] *= 2

    elif selected_item == ITEM_MAGNIFYING_GLASS:
        if bullets[-1] == 1:
            delayed_print(f"\nThe round in the chamber is... Live!\n")
        elif bullets[-1] == 0:
            delayed_print(f"\nThe round in the chamber is... Blank!\n")
    
    elif selected_item == ITEM_TAVUK_PILAV:
        
        if current_player_health < 4:
            delayed_print(f"\nYou ate the tavuk pilav... It was delicious. (+1 health)")
            current_player_health += 1
            show_healths()
        else:
            delayed_print("\nYou ate the tavuk pilav... You are already max health. (Nothing happens)\n")

    elif selected_item == ITEM_BLOXY_COLA:
        delayed_print("\nYou drink the bloxy cola... It was so bloxy that the last bullet popped.")
        if bullets.pop() == 1:
            delayed_print("\nThe popped bullet was... Live!\n")
        else:
            delayed_print("\nThe popped bullet was... Blank!\n")

    elif selected_item == ITEM_HANDCUFFS:
        if not skip_turn == TURN_DEALER and player_cant_use_handcuffs_second_time == False:
            delayed_print("\nYou used the handcuffs, dealer skips a turn.\n")
            player_cant_use_handcuffs_second_time = True
            skip_turn = TURN_DEALER
        elif player_cant_use_handcuffs_second_time == True:
            delayed_print("\nDealer is already handcuffed.\n")
            player_inventory.append(ITEM_HANDCUFFS)
    
    elif selected_item == ITEM_LUCKY_BLOCK:
        delayed_print(f"\nYou opened the lucky block... A random item added to your inventory!\n")
        random_item = random.choice(items_without_luckyblock)
        player_inventory.append(random_item)
    
    elif selected_item == ITEM_ADRENALINE:

        while True:
            try:
                if dealer_inventory:
                    delayed_print(f"\n{color_red}You injected yourself with the adrenaline...")
                    delayed_print(f"\nDealer's items: {dealer_inventory}")
                    for i, elements in enumerate(dealer_inventory):
                        delayed_print(f"\n{i}. {elements}")
                else:
                    delayed_print(f"\n{color_default}You tried to use the adrenaline... but nothing happens. (The dealer have nothing to steal.)\n")
                    break

                time_over = int(inputimeout(prompt=f"\nBe quick! Select an item to steal!\n", timeout=10))

                if time_over in range(0, len(dealer_inventory)):
                    selected_item = dealer_inventory.pop(time_over)   

                    if len(dealer_inventory) == 1:
                        if selected_item == ITEM_ADRENALINE or skip_turn == TURN_DEALER and selected_item == ITEM_HANDCUFFS:
                            delayed_print(f"\x1b[6A\x1b[J{color_default}You are so clever aren't you?")
                            break
                        delayed_print(f"\x1b[6A\x1b[J{color_default}You steal the {selected_item}\n")
                        player_inventory.append(selected_item)
                        break

                    elif len(dealer_inventory) == 0:
                        if selected_item == ITEM_ADRENALINE or skip_turn == TURN_DEALER and selected_item == ITEM_HANDCUFFS:
                            delayed_print(f"\x1b[5A\x1b[J{color_default}You are so clever aren't you?")
                            break
                        delayed_print(f"\x1b[5A\x1b[J{color_default}You steal the {selected_item}\n")
                        player_inventory.append(selected_item)
                        break

                else:
                    if len(dealer_inventory) == 2:
                        time_over = f"\x1b[6A\x1b[J{color_default}Adrenalin wears off..."
                    elif len(dealer_inventory) == 1:
                        time_over = f"\x1b[5A\x1b[J{color_default}Adrenalin wears off..."
                    delayed_print(time_over)
                    break
                
            except Exception:
                if len(dealer_inventory) == 2:
                    time_over = f"\x1b[6A\x1b[J{color_default}Adrenalin wears off..."
                elif len(dealer_inventory) == 1:
                    time_over = f"\x1b[5A\x1b[J{color_default}Adrenalin wears off..."
                delayed_print(time_over)
                break

    elif selected_item == ITEM_EXPIRED_MEDICINE:
        y = random.randint(0,1)
        while y == 0:
            delayed_print("\nYou eat the expired medicine... You really did that?")
            current_player_health -= 1
            if current_player_health <= 0:
                expired_medicine_special_case = True
                current_player_health  = 0
                break      
            show_healths()
            break
        if y == 1 and current_player_health < 4:
            delayed_print("\nYou eat the expired medicine... Luckily you misread the expire date. (It wasn't expired)")
            current_player_health += 1
            show_healths()
        elif current_player_health == 4:
            delayed_print("\nYou eat the expired medicine... You are already max health. (Nothing happens)\n")

    elif selected_item == ITEM_INVERTER:
        delayed_print("\nYou used the inverter... beep boop bop (The polarity of the current shell in the chamber changes.)\n")
        polarity_bullet = bullets.pop()
        if polarity_bullet == 1 or polarity_bullet == 2:
            polarity_bullet = 0
        else:
            polarity_bullet = 1
        bullets.append(polarity_bullet)

    elif selected_item == ITEM_BURNER_PHONE:
        if len(bullets) == 1:
            delayed_print(f"\nHow unfortunate... Only the dealer\x1b[6D{color_red}Devil \x1b[6D{color_default}dealer knows the last bullet.\n")
            players_desicion()
        delayed_print("\nYou used the burner phone... Torururururu")
        bullets_reversed = list(reversed(bullets))
        shell_index = random.randint(0, len(bullets_reversed)-1)
        shell_state = bullets_reversed[shell_index]
        if shell_state == 0:
            delayed_print(f"\nMoshi moshi {shell_index + 1}. Shell is blank! ('1.' means current shell in the chamber)\n")
        else:
            delayed_print(f"\nMoshi moshi {shell_index + 1}. Shell is live! ('1.' means current shell in the chamber)\n")
        
    if expired_medicine_special_case == False:
        players_desicion()

def players_desicion():
    global current_player_health
    global current_dealer_health
    global dealer_gonna_know_that_round
    global dealer_knows_the_current_bullet
    reloading_bullets()

    for value in dealer_gonna_know_that_round:
        if value == len(bullets):
            dealer_knows_the_current_bullet = False
            dealer_gonna_know_that_round.remove(value)
            break


    while True:
        try:
            a = int(input("\nShoot the dealer (1) Shoot yourself (2) Look at your items (3)\n"))
            if a in range(1,4):
                break
            else:
                delayed_print("\x1b[3A\x1b[J")
        except ValueError:
            delayed_print("\x1b[3A\x1b[J")
 
    if a == 3:
        player_items_function()
    else:
        bullet = bullets.pop()
    
    if a == 1 and bullet == 1:
        delayed_print("Player attacks! It's a hit.")
        current_dealer_health -= bullet
    
    elif a == 1 and bullet == 2:
        delayed_print("Player attacks! It's a double hit.")
        current_dealer_health -= bullet
        
    elif a == 1 and bullet == 0:
        delayed_print("Player attacks! It's a miss.")
        
    elif a == 2 and bullet == 1:
        delayed_print("Player shoots itself It's a hit.")
        current_player_health -= bullet
    
    elif a == 2 and bullet == 2:
        delayed_print("Player shoots itself It's a double hit.")
        current_player_health -= bullet
        
    elif a == 2 and bullet == 0:
        delayed_print("Player shoots itself! It was a blank cartidge")
        delayed_print("\nIts players turn again!\n")        
        players_desicion()
    


def dealer_desicion():
    global current_player_health
    global current_dealer_health
    global dealer_used_mglass
    global dealer_knows_the_current_bullet 
    global dealer_gonna_know_that_round
    global dealer_handsaw_case    
    reloading_bullets()   
    dealer_items_function()
    reloading_bullets()

    for value in dealer_gonna_know_that_round:
        if value == len(bullets):
            dealer_knows_the_current_bullet = True
            dealer_gonna_know_that_round.remove(value)
            break
        
        else:
            dealer_knows_the_current_bullet = False
            continue

    
    r = random.randint(1,2)
    bullet = bullets.pop()
    # print("\n",dealer_knows_the_current_bullet, dealer_gonna_know_that_round)
            
    
    if not bullets or dealer_used_mglass == True or dealer_knows_the_current_bullet or dealer_handsaw_case == True:
        dealer_used_mglass = False
        dealer_knows_the_current_bullet = False
        dealer_handsaw_case = False
        if bullet == 1:
            delayed_print("\nDealer attacks! It's a hit.")
            current_player_health -= bullet
            return None
            
        elif bullet == 2:
            delayed_print("\nDealer attacks! It's a double hit.")
            current_player_health -= bullet
            return None

        else:
            delayed_print("\nDealer shoots itself! It was a blank cartidge.")
            delayed_print("\nIts Dealer's turn again!\n")
            dealer_desicion()
            return None
       
    
    if r == 1 and bullet == 1:
        delayed_print("\nDealer attacks! It's a hit.")
        current_player_health -= bullet
    
    elif r == 1 and bullet == 2:
        delayed_print("\nDealer attacks! It's a double hit.")
        current_player_health -= bullet

    elif r == 1 and bullet == 0:
        delayed_print("\nDealer attacks! It's a miss.")

    elif r == 2 and bullet == 1:
        delayed_print("\nDealer shoots itself! It's a hit.")
        current_dealer_health -= bullet
    
    elif r == 2 and bullet == 2:
        delayed_print("\nDealer shoots itself! It's a double hit.")
        current_dealer_health -= bullet

    elif r == 2 and bullet == 0:
        delayed_print("\nDealer shoots itself! It was a blank cartidge.")
        delayed_print("\nIts Dealer's turn again!\n")        
        dealer_desicion()


while current_player_health > 0 and current_dealer_health > 0:
    if current_turn == TURN_PLAYER:
        players_desicion()
        show_healths()
        if check_death() == True:
            break
        current_turn = TURN_DEALER

    elif current_turn == TURN_DEALER:
        dealer_desicion()
        show_healths()
        if check_death() == True:
            break
        reloading_bullets()
        player_cant_use_handcuffs_second_time = False
        current_turn = TURN_PLAYER
        while True:
            try:
                a = input("Write (>) to continue. ")
                if a == ">":
                    os.system("cls")
                    show_healths()
                    break
                else:
                    print("\x1b[1A\x1b[2K\x1b[1A")
            except ValueError:
                print("\x1b[1A\x1b[2K\x1b[1A")
    
    reloading_inventorys()

    if skip_turn == TURN_DEALER:
        delayed_print("\nDealer's turn is skipped!\n")
        skip_turn = None
        current_turn = TURN_PLAYER
    
    elif skip_turn == TURN_PLAYER:
        delayed_print("\nPlayer's turn is skipped!\n")
        skip_turn = None
        current_turn = TURN_DEALER