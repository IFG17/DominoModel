import pygame as pg
from random import randrange
import pymunk.pygame_util
import time
pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 1000 , 800
FPS = 30

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 2000
DOMINOMASSES = [2, 30, 40, 50, 60, 70, 80, 90, 100] 
DOMINOSIZES = [(2,15), (20, 90), (20, 100), (20, 110), (20, 120), (20, 130), (20, 140,), (20, 150), (20,160)]
DOMINOLS = [10, 30, 40, 50, 60, 70, 80, 90, 100]
domino_mass, domino_size = 20, (10, 50) # ТУТ МЕНЯЮТ РАЗМЕРЫ ДОМИНОШКИ
STARTPOINT_X = 80 # ЭТО НЕ МЕНЯЮТ
STARTPOINT_Y = 20 # ЭТО НЕ МЕНЯЮТ
DOMINO_COUNT = 500# ТУТ МЕНЯЮТ КОЛИЧЕСТВО ДОМИНОШЕК
DOMINO_L = 2# ТУТ МЕНЯЮТ РАССМТОЯНИЕ МЕЖДУ НИМИ
EXPLOREINDEX = 60
PEGPOINTPOS = (60,720)

COLLIDEFLAG = False

TIMESINCESTART = time.time()

OBJECTS = list()

def create_peg(pos, space):
    circle_shape = pymunk.Circle(space.static_body, radius=70, offset=(pos))
    circle_shape.color = [randrange(256) for i in range (4)]
    #circle_shape.elasticity = 0.0
    circle_shape.friction = 0.0
    space.add(circle_shape)
    OBJECTS.append(circle_shape)
    
def create_domino (space, position, collisionType, domino_mass, domino_size):
    domino_moment = pymunk.moment_for_box (domino_mass, domino_size)
    domino_body = pymunk.Body(domino_mass, domino_moment)
    domino_body.position = position
    domino_shape = pymunk.Poly.create_box(domino_body, domino_size)
    #domino_shape.elasticity = 0.0
    domino_shape.friction = 0.5
    domino_shape.collision_type = collisionType
    domino_shape.color = [randrange(256) for i in range (4)]
    space.add(domino_body, domino_shape)
    OBJECTS.append(domino_shape)

def collide (arbiter, space, data):
    global COLLIDEFLAG
    if (COLLIDEFLAG == False):
        print ("---------------COLLIDE PROTOCOL------------")
        print ("~TIME (seconds) :  ", time.time() - TIMESINCESTART)
        print ("~EXPLORE INDEX:  ", EXPLOREINDEX)
        print ("~RESULT SPEED (c.u.):  ", (EXPLOREINDEX * DOMINO_L) / (time.time() - TIMESINCESTART))
        print ("~DOMINO_L (xui):  ", DOMINO_L)
        COLLIDEFLAG = True

    return True

def RunSim ():
    global TIMESINCESTART
    global COLLIDEFLAG
    print ("--")
    COLLIDEFLAG = False
    collisionType = 0
    TIMESINCESTART = time.time()
    CURPOS = STARTPOINT_X
    for i in range (DOMINO_COUNT):   
        CURPOS += DOMINOLS[0]
        if (i == EXPLOREINDEX):
            collisionType = 1
        if (i == EXPLOREINDEX - 1) :
            collisionType = 2
        create_domino(space, (CURPOS, HEIGHT - STARTPOINT_Y), collisionType, DOMINOMASSES[0], DOMINOSIZES[0])
    create_peg(PEGPOINTPOS, space)
    
def Clear ():
    global OBJECTS
    for i in OBJECTS:
        space.remove(i)
    OBJECTS = list()
    
    
segment_shape = pymunk.Segment (space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 20)
segment_shape.friction = 0.5
space.add(segment_shape)



# ball_mass, ball_radius = 1, 7
# segment_thickness = 6

# a, b, c, d = 10, 100, 18, 40
# x1, x2, x3, x4 = a, WIDTH // 2 - c, WIDTH // 2 + c, WIDTH - a
# y1, y2, y3, y4, y5 = b, HEIGHT // 4 - d, HEIGHT // 4, HEIGHT // 2 - 1.5 * b, HEIGHT - 4 * b
# L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
# R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
# B1, B2 = (0, HEIGHT), (WIDTH, HEIGHT)


# def create_ball(space):
#     ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
#     ball_body = pymunk.Body(ball_mass, ball_moment)
#     ball_body.position = randrange(x1, x4), randrange(-y1, y1)
#     ball_shape = pymunk.Circle(ball_body, ball_radius)
#     ball_shape.elasticity = 0.1
#     ball_shape.friction = 0.1
#     space.add(ball_body, ball_shape)
#     return ball_body


# def create_segment(from_, to_, thickness, space, color):
#     segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
#     segment_shape.color = pg.color.THECOLORS[color]
#     space.add(segment_shape)


# def create_peg(x, y, space, color):
#     circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
#     circle_shape.color = pg.color.THECOLORS[color]
#     circle_shape.elasticity = 0.1
#     circle_shape.friction = 0.5
#     space.add(circle_shape)


# # pegs
# peg_y, step = y4, 60
# for i in range(10):
#     peg_x = -1.5 * step if i % 2 else -step
#     for j in range(WIDTH // step + 2):
#         create_peg(peg_x, peg_y, space, 'darkslateblue')
#         if i == 9:
#             create_segment((peg_x, peg_y + 50), (peg_x, HEIGHT), segment_thickness, space, 'darkslategray')
#         peg_x += step
#     peg_y += 0.5 * step

# platforms = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
# for platform in platforms:
#     create_segment(*platform, segment_thickness, space, 'darkolivegreen')
# create_segment(B1, B2, 20, space, 'darkslategray')

# # balls
# balls = [([randrange(256) for i in range(3)], create_ball(space)) for j in range(600)]

while True:
    surface.fill(pg.Color('black'))

    handler = space.add_collision_handler(1,2)
    handler.begin = collide

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                #print (i.pos)
                #create_peg(i.pos, space)
                Clear()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 3:
                print (i.pos)
                #create_peg(i.pos, space)
                RunSim()
    space.step(1 / FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)
