import pygame
import numpy as np

objects = []
trails = []

class Dot():
    def __init__(self,position=[0,0],velocity=[0,0],color=(255,255,255),radius=5,splitDistance=100):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.splitDistance = splitDistance
        self.intialPosition = [position[0],position[1]]
        self.split = False
    def updatePos(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self,surface):
        position = [int(self.position[0]),int(self.position[1])]
        pygame.draw.circle(surface,self.color,position,self.radius)

def create(position=[0,0],velocity=[0,0],color=(255,255,255),radius=5,splitDistance=100):
    object = Dot(position,velocity,color,radius,splitDistance=splitDistance)
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

def makeTrail(objects,color):
    for object in objects:
        trail = Dot(position=list(object.position),velocity=[0,0],radius=1,color=color)
        trails.append(trail)
    del trail

def drawTrail(surface):
    for trail in trails:
        trail.draw(surface)

def dotDistance(dot1,dot2):
    dist = np.sqrt(np.power((dot1[0]-dot2[0]),2)+np.power((dot1[1]-dot2[1]),2))
    return dist

def distance(point1,point2):
    dist = np.sqrt(np.power((point1-point2),2)+np.power((point1-point2),2))
    return dist

maxSplits = np.power(2,7)
size= (700,700)
vel_table = [[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1]]
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Fractal")
run_game = True
black=(0,0,0)
white = (255,255,255)
create([350,700],[0,-1],white)
print(len(vel_table))
color = [100,100,100]
startGame = True




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
        makeTrail(objects,color)
        drawTrail(screen)
        draw(screen)

        if maxSplits > 0:
            for object in objects:
                if object.split:
                    continue
                if dotDistance(object.intialPosition,object.position) > object.splitDistance:
                    index  = vel_table.index(object.velocity)
                    left_vel = index+1
                    right_vel = index-1
                    if left_vel >= len(vel_table):
                        left_vel = 0
                    if right_vel < 0 :
                        right_vel = len(vel_table)-1
                    create([object.position[0],object.position[1]],vel_table[left_vel],splitDistance=(object.splitDistance/1.75))
                    create([object.position[0],object.position[1]],vel_table[right_vel],splitDistance=(object.splitDistance/1.75))
                    object.velocity = [0,0]
                    object.split = True
                    delete(object)
                    maxSplits -= 1

        if not maxSplits > 0 :
            for object in objects:
                if object.velocity != [0,0]:
                    delete(object)


    pygame.display.update()

    clock.tick(60)
