from operator import truediv
import pygame
import math

background_colour = (255,255,255)
(width, height) = (1000, 500)
startingPoint = (500,300)
objectif = startingPoint
tolerance = 3
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
        self.angle = math.pi/4
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
        
        if(self.angle < -math.pi ):
            self.angle += 2*math.pi
        elif(self.angle > math.pi):
            self.angle -= 2*math.pi


    def speedCorrection(self, control):
        self.acc = control[0] + control[1] + control[2]
        self.speed += self.acc*dt
        self.speed = self.speed if self.speed > 0 else 0
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

    angleObjectif = math.atan2((objectif[0] - actualPosition[0]) ,-(objectif[1] - actualPosition[1] + 0.01))

    erreur_angle = angleObjectif - actualAngle
    if((angleObjectif * actualAngle < 0) & (abs(actualAngle) + abs(angleObjectif) > math.pi)):
        erreur_angle = 2 * math.pi + angleObjectif - actualAngle
        if (actualAngle < 0):
            erreur_angle = erreur_angle - 4 * math.pi

 
    print("erreur ", erreur_angle*180 / math.pi,",objectif ", angleObjectif*180 / math.pi,",angle ", actualAngle*180 / math.pi)
    systeme.angleCorrection(anglePID.controle(erreur_angle, actualAngle))
        
    if( isarrived(actualPosition)):
        erreur_Speed = -actualSpeed
        systeme.speedCorrection(speedPID.controle(erreur_Speed, actualSpeed))

    else:




        
        realDistance = math.sqrt((actualPosition[0] - objectif[0])**2 + (actualPosition[1] - objectif[1])**2)

        erreur_Distance = realDistance * math.cos(erreur_angle)
        posPIDResult = positionPID.controle(erreur_Distance, erreur_Distance)

        erreur_Speed = posPIDResult[0] + posPIDResult[1] + posPIDResult[2] - actualSpeed
        systeme.speedCorrection(speedPID.controle(erreur_Speed, actualSpeed))


def isarrived(position):
    if((position[0] < objectif[0] + tolerance) &
    (position[0] > objectif[0] - tolerance) &
    (position[1] < objectif[1] + tolerance) &
    (position[1] > objectif[1] - tolerance)):
        return True
    else:
        return False










#initialisations

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)





particule = object(startingPoint[0], startingPoint[1])
particule.display()
pygame.display.flip()

clock = pygame.time.Clock()

position = 0

positionPID =   PID(3, 0, 1)

speedPID    =   PID(2, 0, .5)

anglePID    =   PID(5, 0, 0)



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
        if event.type == pygame.MOUSEBUTTONUP:
            objectif = pygame.mouse.get_pos()

pygame.quit()
