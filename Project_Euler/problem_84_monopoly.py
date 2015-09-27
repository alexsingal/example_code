# This program will simulate one million turns of Monopoly played with 4-sided dice and plot how many times each square is landed on
 
 
from random import randint
 
 
board = [0 for x in range(0, 40)] #this represents the 40 spots on the gameboard so that board[0] is the GO square and board[10] is the JAIL square. This will be used to tally how many times each square is landed on.
 
chance = [0, 10, 11, 24, 39, 15, 'NextR', 'NextR', 'NextU', 'Back3', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay']
 
 
chest = [0, 10, 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay']
 
 
 
 
def is_chance(place):
    return True if place in [7, 22, 36] else False
    
def is_chest(place):
    return True if place in [2, 17, 33] else False
    
def goto_jail(place, doubles_counter):
    return True if place == 30 or doubles_counter == 3 else False
    
def set_jail():
    return 10, 0  # place goes to 10, doubles_counter goes to 0
    
def set_place(place):
    return place % 40 
 
# Start game
 
place = 0
turn_counter = 0
doubles_counter = 0
chance_counter = 0
chest_counter= 0
 
 
while turn_counter <= 1000000: # a large enough sample to (practically) ensure we get the correct answer
 
    turn_counter += 1
    
    die1 = randint(1,4)
    die2 = randint(1,4)
 
    if die1 == die2:
        doubles_counter += 1
    else:
        doubles_counter = 0
        
    place = set_place(place + die1 + die2)   # even if doublecounter is already at 3, we temporarily advance place, but no matter because gotojail function will correct place to 10 regardless
    
    
    if goto_jail(place, doubles_counter):
       place, doubles_counter =  set_jail()
    
    
    # Dealing with each chance card that requires a movement
    elif is_chance(place):
        
        if chance[chance_counter] in [0, 11, 24, 39, 15]:
            place = chance[chance_counter]
            
        elif chance[chance_counter] == 10: 
            place, doubles_counter = set_jail()
                
        elif chance[chance_counter] == 'NextR':
            
            if place in range(0, 5) or place in range(35, 40):
                place = 5
            
            elif place in range(5, 15):
                place = 15
            
            elif place in range(15, 25):
                place = 25
                
            else:
                place = 35
        
        elif chance[chance_counter] == 'NextU':
            
            if place in range(0, 12) or place in range(28, 40):
                place = 12
            
            else:
                place = 28
                
        elif chance[chance_counter] == 'Back3':
            
            place = set_place(place - 3)
                
        chance_counter += 1
        
        if chance_counter == 15:
            chance_counter = 0
            
            
    # Dealing with each chest card that requires a movement
    
    elif is_chest(place):
        
        if chest[chest_counter] == 0:
            place = chest[chest_counter]
            
        elif chest[chest_counter] == 10:
            place, doubles_counter = set_jail()
        
        chest_counter += 1
        
        if chest_counter == 15:
            chest_counter = 0
            
    
    board[place] += 1 # tallying the spot we landed on
            
 
 
results = sorted([(board[i], i) for i in range(0, 40)])[::-1]
print(results)
