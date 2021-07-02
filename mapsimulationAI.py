# import the pygame module, so you can use it
import pygame as pg
import AstarSearch as astr

class sqrtMeter:
    def __init__(self, px, py, tam, img, scr):
        self.posx = px
        self.posy = py
        self.tam = tam
        self.content = img
        self.screen = scr

    def draw(self):
        self.screen.blit(self.content, (self.posx, self.posy))

    def drawOver(self, IMG):
        IMGRect = IMG.get_rect()
        IMGRect.center = (self.posx + self.tam/2, self.posy + self.tam/2)
        self.screen.blit(IMG, IMGRect)
 

# define a main function
def main():
     
    # initialize the pygame module
    pg.init()
    # pygame.display.set_icon(logo)
    pg.display.set_caption("Tabalho 1")
    # create a surface on screen that has the size of 240 x 180
    screen = pg.display.set_mode((1000,1000))
    screen.fill((220,220,220))
    clock = pg.time.Clock()

    #starting position of map, units as square meters
    map_len = 41
    map_hgh = 42
    mapstart_x = -50
    mapstart_y = -50

    #map texting 
    black = (0, 0, 0)
    green = (0, 255, 0)
    font = pg.font.Font('freesansbold.ttf', 12)
    costFont = pg.font.Font('freesansbold.ttf', 8)
    # text = font.render(str(i+1), True, black)
    # textRect = text.get_rect()
    # textRect.center = (500, 450)
    # screen.blit(text, textRect) 

    #square meter = (x, y)
    tam = 26
    floor = pg.transform.scale(pg.image.load("place.png"), (tam, tam))
    tree = pg.transform.scale(pg.image.load("tree.png"), (tam+8, tam+8))
    bush = pg.transform.scale(pg.image.load("plant.png"), (tam//2, tam))
    gym = pg.transform.scale(pg.image.load("gym.png"), (tam+5, tam+5))
    path = pg.transform.scale(pg.image.load("finalpath.png"), (tam, tam))

    #Initializing squareMeter grid and printing, +1 for text column and row
    sqrMs = {}
    for y in range(map_hgh + 1):
        for x in range(map_len + 1):
            if y == 0 or x == 0:
                text = font.render(str(max(x, y)), True, black)
                sqrMs[(x, y)] = sqrtMeter(mapstart_x + x*tam, mapstart_y + y*tam, tam, text, screen)
                sqrMs[(x, y)].drawOver(text)
            elif astr.m[y-1][x-1] == 'M':
                sqrMs[(x, y)] = sqrtMeter(mapstart_x + x*tam, mapstart_y + y*tam, tam, tree, screen)
                sqrMs[(x, y)].drawOver(sqrMs[(x, y)].content)
            elif astr.m[y-1][x-1] == 'R':
                sqrMs[(x, y)] = sqrtMeter(mapstart_x + x*tam, mapstart_y + y*tam, tam, bush, screen)
                sqrMs[(x, y)].drawOver(sqrMs[(x, y)].content)
            elif astr.m[y-1][x-1] in astr.gymname:
                sqrMs[(x, y)] = sqrtMeter(mapstart_x + x*tam, mapstart_y + y*tam, tam, gym, screen)
                sqrMs[(x, y)].drawOver(sqrMs[(x, y)].content)
            else:
                sqrMs[(x, y)] = sqrtMeter(mapstart_x + x*tam, mapstart_y + y*tam, tam, floor, screen)
                sqrMs[(x, y)].draw()

    for px, py in astr.cost_so_far:
        t_cost = costFont.render(str(astr.cost_so_far[(px, py)]), True, black)
        sqrMs[(py+1, px+1)].drawOver(t_cost)

    for px, py in astr.pathf:
        sqrMs[(px+1, py+1)].drawOver(path)

    pg.display.flip()

 
    # define a variable to control the main loop
    running = True
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # screen.fill((220,220,220))
        #screen.blit(image, (imgX, imgY))
        # pg.display.flip()
        clock.tick(60)
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()