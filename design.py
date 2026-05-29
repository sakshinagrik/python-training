from turtle import *
speed(0)
bgcolor("black")
colors = ['red','yellow']
hideturtle()
for i in range(1222):
    goto(0,0)
    color(colors[i%2])
    forward(130)
    left(3)
    circle(40)
    forward(130)
done()