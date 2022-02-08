import pygame
import math

background_colour = (255,255,255)
(width, height) = (1400, 400)
objectif = 0 #height/4
fps = 100
dt = 1/fps

accMax = 100

class object:
    def __init__(self, x, y):
        self.size = 3
        self.colour = (255,0,0)
        self.thickness = 2
        #state
        self.x = x
        self.y = y
        self.angle = math.pi / 4
        self.acc_angle = 0
        self.speed = -500
        self.acc = 0


    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        pygame.draw.line(screen, (125,0,125), (0,height/4), (width,height/4))

    def move(self, control):
        self.acc = control[0] + control[1] + control[2]
        self.speed += self.acc*dt
        deplacement = 1/2 * self.acc*dt*dt + self.speed*dt
        print(self.speed)
        self.x += deplacement * math.sin(math.pi - self.angle)
        self.y += deplacement * math.cos(math.pi - self.angle)
        

    def getPosition(self):
        return self.y

    def getSpeed(self):
        return self.speed



class PID:
    def __init__(self,P,I,D):
        self.P = P
        self.I = I
        self.D = D
        self.statePrecedente = 0
        self.integrale = 0

    def controle(self, erreur, state):
        self.integrale += erreur * dt
        
        Pcorrect = self.P * erreur
        Icorrect = self.I * self.integrale
        Dcorrect = self.D * (state - self.statePrecedente) / dt
        
        self.statePrecedente = state
        return(Pcorrect, Icorrect, Dcorrect)
        








screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)

particule = object(400,200)
particule.display()
pygame.display.flip()

clock = pygame.time.Clock()

position = 0

speedPID = PID(
    3,0,0.7)



running = True
while running:

    '''
    position = particule.getPosition()

    erreur = objectif - position'''

    speed = particule.getSpeed()

    erreur = objectif - speed

    particule.move(speedPID.controle(erreur, speed))

    screen.fill(background_colour)
    particule.display()
    pygame.display.flip()

    clock.tick(fps)



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
