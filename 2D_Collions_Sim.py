# IMPORTS ==============================

import pygame

import math

import numpy as np

import copy

import random

# GLOBAL VARIABLES =====================

BLACK = (0,0,0)

BLUE = (0,0,255)

GAME = pygame.display.set_mode((800,800))

clock = pygame.time.Clock()

pygame.init()

# SUBPROGRAMS ==========================

def Display(List, dt):

    # Define colors
    
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    # Fill Background
    
    GAME.fill(BLACK)

    # Draw all circles from the list onto the surface
    
    for element in List:
        
        positionx = element[0]
        positiony = element[1]
        radius = element[2]
        pygame.draw.circle(GAME, BLUE, (positionx, positiony), radius)

    # Update the display once after all circles have been drawn
    
    pygame.display.update()
    

    #pygame.time.delay(int(1000*dt))
    
def detectCollision (List):

    distance = 0

    listOfCollisions = []

    for first in range(0, len(List)-1):

        for second in range(first+1, len(List)):

            distance = math.sqrt((List[first][0] - List[second][0])**2 + (List[first][1] - List[second][1])**2)

            if distance <= (List[first][2] + List[second][2]):

                listOfCollisions.append([first, second])
            
    return listOfCollisions

def movementCalculator (List, dt):

    for element in range(0, len(List)):

        # Updating acceleration then velocity then position
        
        accx = 0
        accy = 9.8

        velx = List[element][4] + accx*dt
        vely = List[element][5] + accy*dt

        positionx = List[element][0] + velx*dt
        positiony = List[element][1] + vely*dt

        List[element][0] = positionx
        List[element][1] = positiony

        List[element][4] = velx
        List[element][5] = vely
        
    return List

def Collisioncalculator(List):

    for pairs in range(0, len(List)):

        n1 = List[pairs][0]
        n2 = List[pairs][1]

        # Initial conditions
        
        u_1 = [Objects[n1][4],Objects[n1][5]]
        u_2 = [Objects[n2][4],Objects[n2][5]]

        c_1 = [Objects[n1][0],Objects[n1][1]]
        c_2 = [Objects[n2][0],Objects[n2][1]]

        m_1 = float(Objects[n1][3])
        m_2 = float(Objects[n2][3])

        # Ditance from centers

        D = np.sqrt((c_2[0]-c_1[0])**2 + (c_2[1]-c_1[1])**2)

        # Normal unit vector
        
        n = [((c_2[0]-c_1[0])/D),((c_2[1]-c_1[1])/D)]

        # Tangential unit vector

        t = [(-(c_2[1]-c_1[1])/D),((c_2[0]-c_1[0])/D)]

        # Vector Maths

        # Tangential

        tangential_speed1 = dotproduct(u_1,t)
        tangential_speed2 = dotproduct(u_2,t)

        # Normal

        normal_speed1 = ((m_1-m_2)*dotproduct(u_1,n)+2*m_2*dotproduct(u_2,n))/(m_1+m_2)
        normal_speed2 = ((m_2-m_1)*dotproduct(u_2,n)+2*m_1*dotproduct(u_1,n))/(m_1+m_2)

        # Solving back to x and y coordinates

        a1 = n[0]
        b1 = n[1]
        
        c1 = normal_speed1
        d1 = tangential_speed1

        v_1 = [(c1*a1-b1*d1),(c1*b1+d1*a1)]

        a2 = n[0]
        b2 = n[1]
        
        c2 = normal_speed2
        d2 = tangential_speed2

        v_2 = [(c2*a2-b2*d2),(c2*b2+d2*a2)]

        # Update velocities

        Objects[n1][4] = v_1[0]
        Objects[n1][5] = v_1[1]

        Objects[n2][4] = v_2[0]
        Objects[n2][5] = v_2[1]

        
def Boundaries(List):

    for element in range(0, len(List)):

        if List[element][0] > 600 or List[element][0] < 250:

            List[element][4] = -List[element][4]
            
        if List[element][1] > 600 or List[element][1] < 20:

            List[element][5] = -List[element][5]
            



def dotproduct(vector1,vector2):

    # Vector cross product
    
    value = vector1[0]*vector2[0]+vector1[1]*vector2[1]
    
    return value


# MAIN PROGRAM =========================


dt = 0.005
Number_particles = 150
Objects = []

x = 300
y = 300

# (260,590)
for i in range(0, Number_particles):

    if x >= 590:
        
        x = 270
        y = y + 10

    else:
         
        x = x + 10

    v1 = random.randint(-300,300)
    v2 = random.randint(-300,300)
    
    Objects.append([x,y,4,1,v1,v2])

Objects.append([400,100,30,100,-10,-10])

# Main loop
running = True
while running:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Game logic and rendering
    Display(Objects, dt)
    Boundaries(Objects)
    Collisions = detectCollision(Objects)
    
    if Collisions != []:
        Collisioncalculator(Collisions)
        
    Objects = movementCalculator(Objects, dt)
    
    # Cap the frame rate
    clock.tick(200)

pygame.quit()

