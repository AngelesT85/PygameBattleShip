import pygame as pg
from random import randint
from functions import *
from images import *
import json

class Field:
    def __init__(self, first_X, first_Y, live_ships=9) -> None: #108 474 - first field and 596 474 - second
        self.live_ships = live_ships
        self.field = [[Place(first_X + j * 32, first_Y + i * 32) for j in range(10)] for i in range(10)]

    def pr_all(self, screen, print_ships=False):
        status_list = ["skip", "hit"]
        if print_ships:
            status_list.append("part_ship")
        
        for i in self.field:
            for j in i:
                if j.status in status_list:
                    for image in j.images:
                        screen.blit(image, (j.X, j.Y))
    
    def do_ships(self, coords, num_of_ships, bot, comp_field): 
        if bot:
            return_num_ships()
        num_of_ships = Ship.ship_gen(comp_field, num_of_ships, bot, coords)
        for i in range(len(comp_field)):
            for j in range(len(comp_field[0])):
                if type(comp_field[i][j]) == Ship and self.field[i][j].status != "part_ship":
                    self.field[i][j].status = "part_ship"
                    self.field[i][j].images.append(ShipContinueImg)
        
        return num_of_ships

    def normal_ships_image(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if self.field[i][j].status == "part_ship":
                    up, down, right, left = Place(0, 0), Place(0, 0), Place(0, 0), Place(0, 0)
                    if i - 1 >= 0:
                        up = self.field[i - 1][j]
                    if i + 1 <= 9:
                        down = self.field[i + 1][j]
                    if j + 1 <= 9:
                        right = self.field[i][j + 1]
                    if j - 1 >= 0:
                        left = self.field[i][j - 1]
                    
                    if up.status == "part_ship" and down.status == "part_ship":
                        self.field[i][j].images[0] = ShipContinueImg
                    elif up.status == "part_ship" and down.status != "part_ship":
                        self.field[i][j].images[0] = ShipStartImg
                    elif up.status != "part_ship" and down.status == "part_ship":
                        self.field[i][j].images[0] = ShipEndImg
                    elif right.status == "part_ship" and left.status == "part_ship":
                        self.field[i][j].images[0] = pg.transform.rotate(ShipContinueImg, 90.0)
                    elif right.status == "part_ship" and left.status != "part_ship":
                        self.field[i][j].images[0] = pg.transform.rotate(ShipEndImg, 90.0)
                    elif right.status != "part_ship" and left.status == "part_ship":
                        self.field[i][j].images[0] = pg.transform.rotate(ShipStartImg, 90.0)
                    else:
                        self.field[i][j].images[0] = OneDeckShipImg
            
    def synchronize(self, x, y, field=None):
        if field == None:
            if self.field[y][x].status == "free_place":
                self.field[y][x].status = "skip"
                self.field[y][x].images.append(SkipImg)
            elif self.field[y][x].status == "part_ship":
                self.field[y][x].status = "hit"
                self.field[y][x].images.append(HitImg)
        else:
            for i in range(10):
                for j in range(10):
                    if field[i][j] == "*":
                        self.field[i][j].status = "skip"
                        self.field[i][j].images.append(SkipImg)


class Ship:
    def __init__(self) -> None:
        self.length = 1
        self.hp = 1
        self.direction = None # tuple like (-1, 0)
        self.start_coords = None # tuple like (0, 0)

    def put_ship(self, comp_field, coords) -> tuple:
    
        string, column = coords

        # check coords 
        if isinstance(string, int) and isinstance(column, int):
            if (string <= -1 or string >= 10) and (column <= -1 or column >= 10) or comp_field[string][column] != "-":
                return False, None
        else:
            return False, None
        
        # check corners of ship
        for i in (1, -1): 
            for j in (1, -1):
                try:
                    if (0 <= string + i <= 9) and (0 <= column + j <= 9):
                        if isinstance(comp_field[string + i][column + j], Ship):
                            return False, None
                except IndexError:
                    continue

        num_of_ships_around = 0

        # check num of ships around coords
        for i in (1, -1):
            
            # check cells sround ship
            try:
                column_cell = comp_field[string][column + i] # there are change only column
            except:
                if column + i >= 10:
                    column_cell = comp_field[string][column]

            try:
                string_cell = comp_field[string + i][column] # there are change only string
            except:
                if string + i >= 10:
                    string_cell = comp_field[string][column]

            # check column cell and srtring cell
            if isinstance(column_cell, Ship):
                if column + i >= 0:
                    num_of_ships_around += 1


            if isinstance(string_cell, Ship):
                if string + i >= 0:
                    num_of_ships_around += 1

        # create new ship
        if num_of_ships_around == 0:
            comp_field[string][column] = self
            with open("num_of_ships.json", "r", encoding="utf-8") as file:
                num_of_ships = json.load(file)
                if num_of_ships["1"] <= 0:
                    comp_field[string][column] = "-"
                    return False, None
                num_of_ships["1"] -= 1
                self.start_coords = coords
                with open("num_of_ships.json", "w", encoding="utf-8") as file1:
                    json.dump(num_of_ships, file1, indent=4)
            return True, "new"

        # continue ship
        elif num_of_ships_around == 1:

            # check continue of ship
            for i in (1, -1):

                # we will check cells around coords
                try:
                    column_cell = comp_field[string][column + i] # there are change only column
                except IndexError:
                    if (column + i >= 10) or (column + i <= -1):
                        column_cell = comp_field[string][column]

                try:
                    string_cell = comp_field[string + i][column] # there are change only string
                except IndexError:
                    if (string + i >= 10) or (string + i <= -1):
                        string_cell = comp_field[string][column]

                
                # if horizontal ship
                if isinstance(column_cell, Ship):
                    comp_field[string][column] = column_cell

                    if (column_cell.length + 1 == comp_field[string].count(column_cell)) and (column_cell.length + 1 <= 4):
                        column_cell.length += 1
                        column_cell.hp += 1
                        if not update_num_of_ships(column_cell):
                            column_cell.length -= 1
                            column_cell.hp -= 1
                            comp_field[string][column] = "-"
                            return False, None
                        column_cell.direction = (0, 1)
                        if (column < column_cell.start_coords[1]):
                            column_cell.start_coords = (string, column)
                    else:
                        comp_field[string][column] = "-"
                        return False, None
                    return True, None

                # if vertical ship
                if isinstance(string_cell, Ship):
                    column_values = list()
                    for _ in range(10):
                        column_values.append(comp_field[_][column])
                    
                    comp_field[string][column] = string_cell
                    if (string_cell.length == column_values.count(string_cell)) and (string_cell.length + 1 <= 4):
                        string_cell.length += 1
                        string_cell.hp += 1
                        if not update_num_of_ships(string_cell):
                            string_cell.length -= 1
                            string_cell.hp -= 1
                            comp_field[string][column] = "-"
                        string_cell.direction = (1, 0)
                        if (string < string_cell.start_coords[0]):
                            string_cell.start_coords = (string, column)
                    else:
                        comp_field[string][column] = "-"
                        return False, None
                    return True, None

        return False, None

    def create_ship(comp_field, coords) -> tuple:
        ship = Ship()
        result = ship.put_ship(comp_field, coords)
        return result
    
    def death(self, comp_field, coords):
        string, col = coords
        fired_cell = comp_field[string][col]

        # death for one-deck ship
        if fired_cell.length == 1:
            for i in (1, -1):
                for j in (1, -1):
                    if (0 <= string + i <= 9) and (0 <= col + j <= 9):
                        comp_field[string + i][col + j] = "*"
                if (0 <= col + i <= 9):
                    comp_field[string][col + i] = "*"
                
                if (0 <= string + i <= 9):
                    comp_field[string + i][col] = "*"
             
            return None

        start_string = fired_cell.start_coords[0]
        start_col = fired_cell.start_coords[1]

        str_dire = fired_cell.direction[0]
        col_dire = fired_cell.direction[1]

        # vertical ship death
        if str_dire:

            # sides of ship 
            for i in range(fired_cell.length):
                if col + 1 <= 9:
                    comp_field[start_string + i][start_col + 1] = "*"

                if col - 1 >= 0:
                    comp_field[start_string + i][start_col - 1] = "*"
            
            # top and end of ship
            # idk why '+' -------\/
            if 0 <= start_string - str_dire <= 9:
                comp_field[start_string - str_dire][start_col] = "*"

            if 0 <= start_string + fired_cell.length <= 9:
                comp_field[start_string + fired_cell.length][start_col] = "*"
            
            # corners of ship
            for i in (-1, fired_cell.length):
                for j in (-1, 1):
                    if (0 <= (start_string + i) <= 9) and (0 <= (start_col + j) <= 9):
                        comp_field[start_string + i][start_col + j] = "*"

            
        # horizontal ship death
        elif col_dire:

            # sides of ship
            for i in range(fired_cell.length):
                if string + 1 <= 9:
                    comp_field[start_string + 1][start_col + i] = "*"
                
                if string - 1 >= 0:
                    comp_field[start_string - 1][start_col + i] = "*"

            # top and end of ship
            if 0 <= start_col - col_dire <= 9:
                comp_field[start_string][start_col - col_dire] = "*"
            
            if 0 <= start_col + fired_cell.length <= 9:
                comp_field[start_string][start_col + fired_cell.length] = "*"
            
            # corners of ship
            for i in (-1, fired_cell.length):
                for j in (-1, 1):
                    if (0 <= (start_string + j) <= 9) and (0 <= (start_col + i) <= 9):
                        comp_field[start_string + j][start_col + i] = "*"  

    def fire(self, comp_field, coords) -> tuple: # tuple - (is hit, Death/Hit/None)
        string, col = coords
        fired_cell = comp_field[string][col]

        if isinstance(fired_cell, Ship):
            if fired_cell.hp >= 1:
                fired_cell.hp -= 1

                if fired_cell.hp <= 0:
                    fired_cell.death(comp_field, coords)
                    comp_field[string][col] = "o"
                    return True, "Death"
                
                comp_field[string][col] = "o"
                return True, "Hit"
        
        comp_field[string][col] = "o"

        return False, None

    def create_ship(comp_field, coords):
        ship = Ship()
        result = ship.put_ship(comp_field, coords)
        return result
    
    def ship_gen(comp_field, num_of_ships, bot, coords):
        if bot:
            num_of_errors = 0
            while num_of_ships < 10:

                if num_of_errors >= 300:
                    num_of_errors = 0
                    comp_field = create_field()
                    num_of_ships = 0
                    return_num_ships()

                result = Ship.create_ship(comp_field, (randint(0, 9), randint(0, 9)))
                if not result[0]:
                    num_of_errors += 1

                elif result[1] == "new":
                    num_of_ships += 1

            return num_of_ships

        else:
            result = Ship.create_ship(comp_field, coords)
            if result[1] == "new":
                num_of_ships += 1        
        return num_of_ships

class Place:
    def __init__(self, X, Y) -> None:
        self.images = []
        self.status = "free_place"
        self.X = X
        self.Y = Y