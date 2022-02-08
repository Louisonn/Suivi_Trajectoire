import pygame
import math

background_colour = (255,255,255)
(width, height) = (1400, 1000)
objectif = (600, 400)
startingPoint = (400,400)
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
        self.angle = math.pi/2
        self.vel_angle = 0
        self.speed = 0
        self.acc = 0


    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, self.thickness)
        pygame.draw.line(screen, (125,0,125), (self.x,self.y), (self.x + 50 * math.sin(math.pi - self.angle),self.y + 50 * math.cos(math.pi - self.angle)))
        pygame.draw.line(screen, (125,0,125), (0,height/4), (width,height/4))
        pygame.draw.circle(screen, (125,0,125), objectif, 4, 4)


    def angleCorrection(self, control):
        self.vel_angle = control[0] + control[1] + control[2]
        self.angle += self.vel_angle * dt


    def speedCorrection(self, control):
        self.acc = control[0] + control[1] + control[2]
        self.speed += self.acc*dt
        deplacement = 1/2 * self.acc*dt*dt + self.speed*dt
        self.x += deplacement * math.sin(math.pi - self.angle)
        self.y += deplacement * math.cos(math.pi - self.angle)
        

    def getPosition(self):
        return (self.x, self.y)

    def getSpeed(self):
        return self.speed

    def getAngle(self):
        return self.angle



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
        



def process(systeme):

    actualPosition = systeme.getPosition()
    actualSpeed = systeme.getSpeed()
    actualAngle = systeme.getAngle()
        


    erreur_angle = math.atan((objectif[1] - actualPosition[1]) /(objectif[0] - actualPosition[0] + 0.01)) - actualAngle + math.pi/2
    
    systeme.angleCorrection(anglePID.controle(erreur_angle, actualAngle))

    realDistance = math.sqrt((actualPosition[0] - objectif[0])**2 + (actualPosition[1] - objectif[1])**2)

    erreur_Distance = realDistance * math.cos(erreur_angle)
    posPIDResult = positionPID.controle(erreur_Distance, erreur_Distance)

    erreur_Speed = posPIDResult[0] + posPIDResult[1] + posPIDResult[2] - actualSpeed
    systeme.speedCorrection(speedPID.controle(erreur_Speed, actualSpeed))



    








#initialisations

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)




particule = object(startingPoint[0], startingPoint[1])
particule.display()
pygame.display.flip()

clock = pygame.time.Clock()

position = 0

positionPID =   PID(1, 0, 0)

speedPID    =   PID(1, 0, 0)

anglePID    =   PID(2, 0, 0)



running = True
while running:

    process(particule)

    
    
    screen.fill(background_colour)
    particule.display()
    pygame.display.flip()

    clock.tick(fps)



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
