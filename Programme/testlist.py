from operator import truediv
import pygame
import math

background_colour = (255,255,255)
(width, height) = (1000, 500)
startingPoint = (500,300)
objectif = startingPoint
fps = 100


dt = 1/fps



class point:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.reached = False

    def display(self):
        pygame.draw.circle(screen, (255,0,0), self.coordinate, 2, 2)






def displayDestinations():
    for i in range(0, len(destinations)):
        destinations[i].display()










#initialisations

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)

firstPoint = point(objectif)
destinations = [firstPoint]


clock = pygame.time.Clock()


running = True
while running:
    
    screen.fill(background_colour)
    displayDestinations()
    pygame.display.flip()

    clock.tick(fps)



    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            newDestination = point(pygame.mouse.get_pos())
            destinations.append(newDestination)

pygame.quit()
