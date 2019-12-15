import pygame
import numpy as np

objects = []

class Dot():
    def __init__(self,position=[0,0],velocity=[0,0],color=(255,255,255),radius=5):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.intialPosition = [position[0],position[1]]
        self.split = False
    def updatePos(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self,surface):
        position = [int(self.position[0]),int(self.position[1])]
        pygame.draw.circle(surface,self.color,position,self.radius)

def create(position=[0,0],velocity=[0,0],color=(255,255,255),radius=5):
    object = Dot(position,velocity,color,radius)
    objects.append(object)
    del object

def delete(object):
    objects.remove(object)

def update():
    for object in objects:
        object.updatePos()

def draw(surface):
    for object in objects:
        object.draw(surface)

def dotDistance(dot1,dot2):
    dist = np.sqrt(np.power((dot1[0]-dot2[0]),2)+np.power((dot1[1]-dot2[1]),2))
    return dist

def distance(point1,point2):
    dist = np.sqrt(np.power((point1-point2),2)+np.power((point1-point2),2))
    return dist

maxSplits = np.power(2,7)
size= (800,800)
vel_table = [[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1]]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Fractal")
run_game = True
black=(0,0,0)
white = (255,255,255)
create([400,790],[0,-1],white)
print(len(vel_table))

startGame = False



while run_game:
    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                startGame = True
    screen.fill(black)

    if startGame:

        update()
        draw(screen)

        if maxSplits > 0:
            for object in objects:
                if object.split:
                    continue
                if dotDistance(object.intialPosition,object.position) > 100:
                    index  = vel_table.index(object.velocity)
                    left_vel = index+1
                    right_vel = index-1
                    if left_vel >= len(vel_table):
                        left_vel = 0
                    if right_vel < 0 :
                        right_vel = len(vel_table)-1
                    create([object.position[0],object.position[1]],vel_table[left_vel])
                    create([object.position[0],object.position[1]],vel_table[right_vel])
                    object.velocity = [0,0]
                    object.split = True
                    maxSplits -= 1

        for object in objects:
            if dotDistance(object.intialPosition,object.position) > 100:
                object.velocity = [0,0]


    pygame.display.update()

    clock.tick(60)
