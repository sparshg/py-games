#imports
import turtle
import time
import random

delay = 0.1

score = 0
high_score = 0

scrn = turtle.Screen()
scrn.title("Snake Game")
scrn.bgcolor('white')
scrn.setup(width=720, height=1080)
scrn.tracer(0)

#snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

#snake berry
berry= turtle.Turtle()
berry.speed(0)
berry.shape("circle")
berry.color("red")
berry.penup()
berry.goto(0,100)

segments = []

#scoreboards
scre = turtle.Turtle()
scre.speed(0)
scre.shape("square")
scre.color("red")
scre.penup()
scre.hideturtle()
scre.goto(0,260)
scre.write("Your Score: 0  High score: 0", align = "center", font=("ds-digital", 24, "normal"))

#Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_left():
    if head.direction != "right":
        head.direction = "left"
def go_right():
    if head.direction != "left":
        head.direction = "right"
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

#Keyboard bindings
scrn.listen()
scrn.onkeypress(go_up, "w")
scrn.onkeypress(go_down, "s")
scrn.onkeypress(go_left, "a")
scrn.onkeypress(go_right, "d")

#MainLoop
while True:
    scrn.update()

    #check collision with border area
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        #hide the segments of body
        for segment in segments:
            segment.goto(1000,1000) #out of range
        #clear the segments
        segments.clear()

        #reset score
        score = 0

        #reset delay
        delay = 0.1

        scre.clear()
        scre.write("score: {}  High score: {}".format(score, high_score), align="center", font=("ds-digital", 24, "normal"))

    #check collision with berry
    if head.distance(berry) <20:
        # move the berry to random place
        x = random.randint(-290,290)
        y = random.randint(-290,290)
        berry.goto(x,y)

        #add a new segment to the head
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("black")
        new_segment.penup()
        segments.append(new_segment)

        #shorten the delay
        delay -= 0.001
        #increase the score
        score += 10

        if score > high_score:
            high_score = score
        scre.clear()
        scre.write("score: {}  High score: {}".format(score,high_score), align="center", font=("ds-digital", 24, "normal")) 

    #move the segments in reverse order
    for index in range(len(segments)-1,0,-1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
    #move segment 0 to head
    if len(segments)>0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()

    #check for collision with body
    for segment in segments:
        if segment.distance(head)<20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"

            #hide segments
            for segment in segments:
                segment.goto(1000,1000)
            segments.clear()
            score = 0
            delay = 0.1

            #update the score     
            scre.clear()
            scre.write("score: {}  High score: {}".format(score,high_score), align="center", font=("ds-digital", 24, "normal"))
    time.sleep(delay)
scrn.mainloop()  