#================================== IMPORTS ====================================


import pygame

import math

import numpy as np

import matplotlib.pyplot as plt

import scipy.optimize


#============================== GlOBAL VARIABLES ===============================


BLACK = (0,0,0)

BLUE = (0,0,255)

GAME = pygame.display.set_mode((800,800))

clock = pygame.time.Clock()

pygame.init()

e = 2.718281828459


#================================= SUBPROGRAMS =================================


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

    # Draw endpoints

    pygame.draw.circle(GAME, BLUE, (Endpoints[0][0],Endpoints[0][1] ), 6)
    pygame.draw.circle(GAME, BLUE, (Endpoints[1][0],Endpoints[1][1] ), 6)

    # Update the display once after all circles have been drawn
    
    pygame.display.update()

def forceCaculator(element, List):

    # Centre of the masses

    # c_2 are the coordinates of the main mass

    # n is the normal unit vector

    # mag is magnitude

    # The numbers indicate the direction of the distance

    if element == 0:

        c_1 = Endpoints[0]
        c_2 = [List[0][0],List[0][1]]
        c_3 = [List[1][0],List[1][1]]

        D_12 = np.sqrt((c_2[0]-c_1[0])**2 + (c_2[1]-c_1[1])**2)
        D_23 = np.sqrt((c_3[0]-c_2[0])**2 + (c_3[1]-c_2[1])**2)

        mag12 = k*(np.sqrt((D_12-L)**2))      
        mag23 = k*(np.sqrt((D_23-L)**2))

        Fx = mag12*(c_1[0]-c_2[0])/D_12 + mag23*(c_3[0]-c_2[0])/D_23
        Fy = mag12*(c_1[1]-c_2[1])/D_12 + mag23*(c_3[1]-c_2[1])/D_23

        acc = [Fx/(List[element][3]),Fy/(List[element][3])]

    if element == len(List)-1:

        c_1 = [List[len(List)-2][0],List[len(List)-2][1]]
        c_2 = [List[len(List)-1][0],List[len(List)-1][1]]
        c_3 = Endpoints[1]

        D_12 = np.sqrt((c_2[0]-c_1[0])**2 + (c_2[1]-c_1[1])**2)
        D_23 = np.sqrt((c_2[0]-c_1[0])**2 + (c_2[1]-c_1[1])**2)

        mag12 = k*(np.sqrt((D_12-L)**2))      
        mag23 = k*(np.sqrt((D_23-L)**2))

        Fx = mag12*(c_1[0]-c_2[0])/D_12 + mag23*(c_3[0]-c_2[0])/D_23
        Fy = mag12*(c_1[1]-c_2[1])/D_12 + mag23*(c_3[1]-c_2[1])/D_23

        acc = [Fx/(List[element][3]),Fy/(List[element][3])]

    if element != 0 and element != len(List)-1:
        
        c_1 = [List[element-1][0],List[element-1][1]]
        c_2 = [List[element][0],List[element][1]]
        c_3 = [List[element+1][0],List[element+1][1]]

        D_12 = np.sqrt((c_2[0]-c_1[0])**2 + (c_2[1]-c_1[1])**2)
        D_23 = np.sqrt((c_3[0]-c_2[0])**2 + (c_3[1]-c_2[1])**2)

        mag12 = k*(np.sqrt((D_12-L)**2))
        mag23 = k*(np.sqrt((D_23-L)**2))

        Fx = mag12*(c_1[0]-c_2[0])/D_12 + mag23*(c_3[0]-c_2[0])/D_23
        Fy = mag12*(c_1[1]-c_2[1])/D_12 + mag23*(c_3[1]-c_2[1])/D_23

        acc = [Fx/(List[element][3]),Fy/(List[element][3])]
        
    return acc

def movementCalculator (List, dt):

    for element in range(0, len(List)):

        # Updating acceleration then velocity then position

        # Calculating acceleration

        acc = forceCaculator(element, List)
        
        accx = acc[0]
        accy = acc[1]+90.8

        velx = List[element][4] + accx*dt - dt*r*(List[element][4])
        vely = List[element][5] + accy*dt - dt*r*(List[element][5])

        positionx = List[element][0] + velx*dt
        positiony = List[element][1] + vely*dt

        List[element][0] = positionx
        List[element][1] = positiony

        List[element][4] = velx
        List[element][5] = vely
        
    return List


# ============================= MAIN PROGRAM ===================================


# Variables =============================================

dt = 0.0005 # Timestep value

L = 3.96 # Original leght of string

k = 50 # Hookes constant

r = 1 # Resistance to movement term

N = 20 # Number of balls

Endpoints = [[200,100],[600,100]]

Objects = []

# Main loop =============================================

spacing = np.abs(Endpoints[1][0]-Endpoints[0][0])/(N+1)

for xposition in range (1, N+1):
    new_object = [Endpoints[0][0]+xposition*spacing,100,3,1,0,0]
    Objects.append(new_object)

running = True
counter = 0
while running == True and counter < 400000:
    
    # Event processing
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Game logic and rendering
    
    Display(Objects, dt)    
    Objects = movementCalculator(Objects, dt)
    
    # Cap the frame rate
    
    clock.tick(100000)

    counter = counter + 1

pygame.quit()

# Optional Matching Functions ==================

final_pos_x = []
final_pos_y = []

# Going through every object and getting the x,y positions
for element in range(0, len(Objects)): 
    final_pos_x.append(round(Objects[element][0],10)-(Endpoints[0][0]+Endpoints[1][0])/2)
    final_pos_y.append(round(-Objects[element][1],10))

# Creating a "guess" function
def model_f(x, a, b, c):
    return(c*(e**(a*x)+e**(-a*x))/2+b)

# Optimization step
popt, pcov = scipy.optimize.curve_fit(model_f, final_pos_x,final_pos_y, p0=[0.01,-10,100])

a_opt = popt[0]
b_opt = popt[1]
c_opt = popt[2]

x_model = np.linspace(final_pos_x[0], final_pos_x[-1], 1000)
y_model = model_f(x_model, a_opt, b_opt, c_opt)

# Plotting
plt.plot(x_model, y_model, 'r--')
plt.plot(final_pos_x, final_pos_y, '.')
plt.show()
