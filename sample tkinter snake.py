import pygame
import math

background_colour = (255,255,255)
(width, height) = (1400, 400)
objectif = height/4
fps = 100
dt = 1/fps

accMax = 100

class object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 1
        self.colour = (255,0,0)
        self.thickness = 1
        self.speed_X = 100
        self.speed_Y = 0
        self.acc_Y = 0


    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        pygame.draw.line(screen, (125,0,125), (0,height/4), (width,height/4))

    def move(self, control):
        self.acc_Y = control[0] + control[1] + control[2]
        #if(self.acc_Y > accMax):
        #   self.acc_Y = accMax
        #if(self.acc_Y < -accMax):
        #   self.acc_Y = -accMax 
        self.speed_Y += self.acc_Y*dt
        self.y += 1/2 * self.acc_Y*dt*dt + self.speed_Y*dt
        print(self.acc_Y)
        
        
        self.x += self.speed_X*dt

    def getPosition(self):
        return self.y


def controle(erreur, derive, integrale):
    coefP = 6
    coefD = 5
    
    coefI = 4
    
    P = coefP * erreur
    I = coefI * integrale
    D = coefD * derive
    return (P, I, D)
    



screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)

particule = object(10,380)
particule.display()
pygame.display.flip()

clock = pygame.time.Clock()


position = 0
erreurPrecedente = 0
integrale = 0

running = True
while running:
    
    position = particule.getPosition()

    erreur = objectif - position
    derive = (erreur - erreurPrecedente)/dt
    integrale += erreur * dt

    erreurPrecedente = erreur
    
    regulation = controle(erreur, derive, integrale)
    
    particule.move(regulation)
    screen.fill(background_colour)
    particule.display()
    pygame.display.flip()

    #clock.tick(fps)



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
