# Imported libaries

import turtle
import numpy as np

# Setting up the code

turtle.bgcolor('white')
r = 300
bob = turtle.Turtle()
bob.hideturtle()
turtle.screensize(1000,1000)
bob.radians()
n = 1.331
d = 0
divisions = 20
collision1 = False
collision2 = False
theta = 0
alpha = 0
angle = 10
intensity = 0

# Circle Creation

bob.speed(1000)
bob.width(1)
bob.penup()
bob.goto(0,-r)
bob.pendown()
bob.circle(r)

# Caculations

for number in range(0,divisions+1):
    bob.seth(0)
    bob.penup()
    bob.goto(-(r+d),(r/divisions)*number)
    collision1 = False
    collision2 = False
    bob.pendown()
    x = (number/divisions)*r
    bob.forward(((x**2)/(2*r)))
    
    while collision1 == False:
        distance = ((bob.xcor()**2)+(bob.ycor()**2))**(1/2)
        bob.pendown()
        bob.forward(r/100)
        if distance <= (r+0.000000001*r):
            collision1 = True
            
    theta = np.abs(np.arctan((bob.ycor())/(bob.xcor())))
    alpha = np.abs(np.arcsin(np.sin(theta)/n))
    bob.rt(theta-alpha)
    bob.forward(r*1.2)
    
    while collision2 == False:
        distance = ((bob.xcor()**2)+(bob.ycor()**2))**(1/2)
        bob.pendown()
        bob.forward(r/100)
        if distance >= r:
            collision2 = True
    delta = -alpha + np.arcsin(n*np.sin(alpha))
    bob.pendown()
    bob.rt(delta)
    bob.forward(1000)

    if (delta+theta-alpha) > (np.pi*(angle/180)-0.012) and (delta+theta-alpha) < (np.pi*(angle/180)+0.012):
        intensity = intensity + 1
        print(delta+theta-alpha)

print (intensity)
    
