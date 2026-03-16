import turtle
import random
import tkinter as tk

# ---------- GUI Window ----------
root = tk.Tk()
root.title("Snake Game GUI")
root.resizable(False, False)

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

# Integrate turtle with Tkinter
screen = turtle.TurtleScreen(canvas)
screen.bgcolor("black")
screen.tracer(0)

# ---------- Snake Head ----------
head = turtle.RawTurtle(screen)
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ---------- Food ----------
food = turtle.RawTurtle(screen)
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# ---------- Score ----------
score = 0
pen = turtle.RawTurtle(screen)
pen.speed(0)
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Arial", 24, "bold"))

# ---------- Controls ----------
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

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# ---------- Move Function ----------
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

# ---------- Restart Function ----------
def restart_game():
    global segments, score
    head.goto(0, 0)
    head.direction = "stop"
    for seg in segments:
        seg.hideturtle()
    segments.clear()
    score = 0
    pen.clear()
    pen.write(f"Score: {score}", align="center", font=("Arial", 24, "bold"))

# ---------- Start Button ----------
start_button = tk.Button(root, text="Restart / Start Game", command=restart_game)
start_button.pack()

# ---------- Main Game Loop ----------
def game_loop():
    global score

    move()

    # Screen wrap
    if head.xcor() > 290:
        head.setx(-290)
    if head.xcor() < -290:
        head.setx(290)
    if head.ycor() > 290:
        head.sety(-290)
    if head.ycor() < -290:
        head.sety(290)

    # Food collision
    if head.distance(food) < 20:
        x = random.randrange(-280, 280, 20)
        y = random.randrange(-280, 280, 20)
        food.goto(x, y)

        segment = turtle.RawTurtle(screen)
        segment.speed(0)
        segment.shape("square")
        segment.color("lime")
        segment.penup()
        segments.append(segment)

        score += 1
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Arial", 24, "bold"))

    # Move body segments
    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    screen.update()
    screen.ontimer(game_loop, 100)  # call again after 100ms

# Start the game loop
game_loop()

# Run Tkinter
root.mainloop()