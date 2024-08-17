import pygame as pg
from images import *
import json

def return_num_ships():
    object = {
        "4": 1,
        "3": 2,
        "2": 3,
        "1": 4
    }
    with open("num_of_ships.json", "w", encoding="utf-8") as file:
        json.dump(object, file, indent=4)

def create_field(space_symbol="-"):
    field = [[space_symbol for _ in range(10)] for i in range(10)]
    return field

def print_field(field):
    for i in range(len(field)):
        print(*field[i])

def update_num_of_ships(cell):
    with open("num_of_ships.json", "r", encoding="utf-8") as num_of_ships:
        num_of_ships = json.load(num_of_ships)
        try:
            if num_of_ships[f"{cell.length}"] < 1:
                return False
            num_of_ships[f"{cell.length - 1}"] += 1
            num_of_ships[f"{cell.length}"] -= 1
        except:
            pass
        else:
            with open("num_of_ships.json", "w", encoding="utf-8") as file:
                json.dump(num_of_ships, file, indent=4)
    return True

def change_coords(x, y, first_x, first_y):
    count = 0
    new_x, new_y = 0, 0

    for i in range(10):
        num = first_x + (32 * i)
        if num <= x < num + 32:
            new_x = i
            count += 1
            break

    for j in range(10):
        num = first_y + (32 * j)
        if num <= y < num + 32:
            new_y = j
            count += 1
            break
                        
    if count == 2:
        return True, new_x, new_y
    else:
        return False, new_x, new_y

def restart_game(screen):
    screen.blit(FieldImg, (0, 0))
    return_num_ships()

def clear_field(screen):
    screen.blit(FieldImg, (0, 0))
    return_num_ships()

def SetClearButton(screen, is_putting):
    '''
    Function put button for clear field
    is_putting - is it time when we are putting ships on the field 
    '''
    if is_putting:
        screen.blit(ClearImg, (0, 0))

def SetRestartButton(screen):
    '''
    Function put button for restart game
    is_again - is it end of rhe game
    '''
    screen.blit(RestartImg, (0, 0))



