import pygame as pg

def game():
    is_game = True
    pg.init()

    screen = pg.display.set_mode((1024, 900))
    screen.fill((255, 255, 255))

    while is_game:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_game = False
                break
        
        pg.display.flip()

game()