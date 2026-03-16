import turtle
import random
import tkinter as tk

# ---------- GUI Window ----------
root = tk.Tk()
root.title("Snake Game GUI")
root.resizable(False, False)

canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

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
high_score = 0
pen = turtle.RawTurtle(screen)
pen.speed(0)
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, 260)
pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 24, "bold"))

# ---------- Controls ----------
def go_up():    global head; head.direction = "up" if head.direction != "down" else head.direction
def go_down():  global head; head.direction = "down" if head.direction != "up" else head.direction
def go_left():  global head; head.direction = "left" if head.direction != "right" else head.direction
def go_right(): global head; head.direction = "right" if head.direction != "left" else head.direction

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# ---------- Move Function ----------
def move():
    if head.direction == "up": head.sety(head.ycor() + 20)
    elif head.direction == "down": head.sety(head.ycor() - 20)
    elif head.direction == "left": head.setx(head.xcor() - 20)
    elif head.direction == "right": head.setx(head.xcor() + 20)

# ---------- Screen Wrap ----------
def wrap_turtle(t):
    if t.xcor() > 290: t.setx(-290)
    elif t.xcor() < -290: t.setx(290)
    if t.ycor() > 290: t.sety(-290)
    elif t.ycor() < -290: t.sety(290)

# ---------- Restart ----------
def restart_game():
    global segments, score
    head.goto(0, 0)
    head.direction = "stop"
    for seg in segments: seg.hideturtle()
    segments.clear()
    score = 0
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 24, "bold"))

start_button = tk.Button(root, text="Restart / Start Game", command=restart_game)
start_button.pack()

# ---------- Main Game Loop ----------
def game_loop():
    global score, high_score

    move()
    wrap_turtle(head)

    # Move segments from tail to head
    for i in range(len(segments)-1, 0, -1):
        segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    # Food collision
    if head.distance(food) < 20:
        x = random.randrange(-280, 280, 20)
        y = random.randrange(-280, 280, 20)
        food.goto(x, y)

        # Add new segment at last segment or behind head
        segment = turtle.RawTurtle(screen)
        segment.speed(0)
        segment.shape("square")
        segment.color("lime")
        segment.penup()
        if segments:
            last = segments[-1]
            segment.goto(last.xcor(), last.ycor())
        else:
            # first segment behind head
            segment.goto(head.xcor(), head.ycor())
        segments.append(segment)

        score += 1
        if score > high_score: high_score = score
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 24, "bold"))

    # Self-collision: only check if more than 4 segments to prevent false positives
    if len(segments) > 4:
        for seg in segments[1:]:
            if head.distance(seg) < 20:
                restart_game()
                break

    screen.update()
    screen.ontimer(game_loop, 100)

game_loop()
root.mainloop()