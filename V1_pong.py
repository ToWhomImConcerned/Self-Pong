import turtle
import os
import random
import math
import time

# -------------------------------
# GAME STATE / GLOBAL VARIABLES
# -------------------------------

player_1_score = 0
player_2_score = 0
round_number = 0

game_active = False  # Controls whether the ball is moving

# Ball velocity components
dx_ball = 0
dy_ball = 0

START_SPEED = 3.2
speed = START_SPEED

dy_ratio = 0.5  # Determines vertical vs horizontal movement ratio
bounce_count = 0
high_score = 0

# -------------------------------
# WINDOW SETUP
# -------------------------------

window = turtle.Screen()
window.title("Game of Pong")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)  # Manual frame updates (important for game loop control)

# -------------------------------
# SCORE DISPLAY OBJECTS
# -------------------------------

score_left = turtle.Turtle()
score_left.color("blue")
score_left.speed(0)
score_left.hideturtle()
score_left.penup()
score_left.goto(-200, 260)

score_label = turtle.Turtle()
score_label.color("grey")
score_label.speed(0)
score_label.hideturtle()
score_label.penup()
score_label.goto(0, 260)

score_right = turtle.Turtle()
score_right.color("orange")
score_right.speed(0)
score_right.hideturtle()
score_right.penup()
score_right.goto(200, 260)

# Initial score text
score_left.write("0", align="center", font=("Arial", 24, "normal"))
score_label.write("Score", align="center", font=("Arial", 20, "normal"))
score_right.write("0", align="center", font=("Arial", 24, "normal"))

# High score display
high_score_display = turtle.Turtle()
high_score_display.color("grey")
high_score_display.speed(0)
high_score_display.hideturtle()
high_score_display.penup()
high_score_display.goto(0, 235)

# Start prompt
prompt = turtle.Turtle()
prompt.color("grey")
prompt.speed(0)
prompt.hideturtle()
prompt.penup()
prompt.goto(0, -270)
prompt.write("Start: space", align="center", font=("Arial", 16, "normal"))

# Bounce counter display
bounce_display = turtle.Turtle()
bounce_display.color("grey")
bounce_display.speed(0)
bounce_display.hideturtle()
bounce_display.penup()
bounce_display.goto(0, -270)

# -------------------------------
# GAME OBJECTS (BALL + PADDLES)
# -------------------------------

ball = turtle.Turtle()
ball.color("red")
ball.shape("circle")
ball.speed(0)
ball.penup()
ball.goto(0, 0)

rightpaddle = turtle.Turtle()
rightpaddle.color("white")
rightpaddle.shape("square")
rightpaddle.speed(0)
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)  # Tall paddle
rightpaddle.penup()
rightpaddle.goto(350, 0)

leftpaddle = turtle.Turtle()
leftpaddle.color("white")
leftpaddle.shape("square")
leftpaddle.speed(0)
leftpaddle.shapesize(stretch_wid=5, stretch_len=1)
leftpaddle.penup()
leftpaddle.goto(-350, 0)

# -------------------------------
# ROUND INITIALIZATION
# -------------------------------

def start_round():
    """
    Starts a new round if the game is inactive.
    Initializes ball direction, speed, and resets counters.
    """
    global game_active, dx_ball, dy_ball, round_number, speed, dy_ratio, bounce_count

    if not game_active:
        round_number += 1
        game_active = True

        speed = START_SPEED
        bounce_count = 0

        # Clear UI elements from previous round
        prompt.clear()
        high_score_display.clear()
        bounce_display.clear()

        bounce_display.write("Bounces: 0", align="center", font=("Arial", 16, "normal"))

        # Randomize vertical movement ratio
        dy_ratio = random.choice([0.3, 0.5, 0.7])
        dx_ratio = math.sqrt(1 - dy_ratio**2)  # Keep total speed consistent

        # Randomize vertical direction, alternate horizontal start direction
        dy_ball = speed * dy_ratio * random.choice([-1, 1])
        dx_ball = speed * dx_ratio * (1 if round_number % 2 == 1 else -1)

# -------------------------------
# INPUT HANDLING SYSTEM
# -------------------------------

# Tracks currently held keys (allows smooth continuous movement)
keys_held = set()

def key_press(key):
    keys_held.add(key)

def key_release(key):
    keys_held.discard(key)

# Key bindings
window.onkeypress(lambda: key_press("w"), "w")
window.onkeypress(lambda: key_press("s"), "s")
window.onkeypress(lambda: key_press("i"), "i")
window.onkeypress(lambda: key_press("k"), "k")
window.onkeypress(lambda: key_press("space"), "space")

window.onkeyrelease(lambda: key_release("w"), "w")
window.onkeyrelease(lambda: key_release("s"), "s")
window.onkeyrelease(lambda: key_release("i"), "i")
window.onkeyrelease(lambda: key_release("k"), "k")
window.onkeyrelease(lambda: key_release("space"), "space")

window.listen()

# Prevents spacebar from retriggering every frame
space_was_held = [False]

# -------------------------------
# MAIN GAME LOOP
# -------------------------------

try:
    while True:
        time.sleep(0.01)  # Controls frame rate (~100 FPS)
        window.update()

        # -----------------------
        # PLAYER MOVEMENT
        # -----------------------

        if "w" in keys_held:
            leftpaddle.sety(min(leftpaddle.ycor() + 6.5, 250))
        if "s" in keys_held:
            leftpaddle.sety(max(leftpaddle.ycor() - 6.5, -250))

        if "i" in keys_held:
            rightpaddle.sety(min(rightpaddle.ycor() + 6.5, 250))
        if "k" in keys_held:
            rightpaddle.sety(max(rightpaddle.ycor() - 6.5, -250))

        # -----------------------
        # START ROUND INPUT
        # -----------------------

        space_is_held = "space" in keys_held
        if space_is_held and not space_was_held[0]:
            start_round()
        space_was_held[0] = space_is_held

        # -----------------------
        # GAME LOGIC (only when active)
        # -----------------------

        if game_active:
            # Move ball
            ball.setx(ball.xcor() + dx_ball)
            ball.sety(ball.ycor() + dy_ball)

            # -------------------
            # WALL COLLISIONS
            # -------------------

            if ball.ycor() > 290:
                ball.sety(290)
                dy_ball = -abs(dy_ball)  # Reflect downward

            if ball.ycor() < -290:
                ball.sety(-290)
                dy_ball = abs(dy_ball)  # Reflect upward

            # -------------------
            # SCORING LOGIC
            # -------------------

            if ball.xcor() > 390:  # Right side miss → Player 1 scores
                ball.goto(0, 0)
                leftpaddle.goto(-350, 0)
                rightpaddle.goto(350, 0)

                dx_ball = 0
                dy_ball = 0
                game_active = False
                space_was_held[0] = True

                if bounce_count > high_score:
                    high_score = bounce_count

                high_score_display.clear()
                high_score_display.write(
                    "High Score: {}".format(high_score),
                    align="center",
                    font=("Arial", 14, "normal")
                )

                bounce_display.clear()
                prompt.write("Start: space", align="center", font=("Arial", 16, "normal"))

                player_1_score += 1
                score_left.clear()
                score_left.write(str(player_1_score), align="center", font=("Arial", 24, "normal"))

            if ball.xcor() < -390:  # Left side miss → Player 2 scores
                ball.goto(0, 0)
                leftpaddle.goto(-350, 0)
                rightpaddle.goto(350, 0)

                dx_ball = 0
                dy_ball = 0
                game_active = False
                space_was_held[0] = True

                if bounce_count > high_score:
                    high_score = bounce_count

                high_score_display.clear()
                high_score_display.write(
                    "High Score: {}".format(high_score),
                    align="center",
                    font=("Arial", 14, "normal")
                )

                bounce_display.clear()
                prompt.write("Start: space", align="center", font=("Arial", 16, "normal"))

                player_2_score += 1
                score_right.clear()
                score_right.write(str(player_2_score), align="center", font=("Arial", 24, "normal"))

            # -------------------
            # PADDLE COLLISIONS
            # -------------------
            
            # Right paddle
            if (
                (ball.xcor() > 340)
                and (ball.xcor() < 350)
                and (rightpaddle.ycor() - 50 < ball.ycor() < rightpaddle.ycor() + 50)
            ):
                ball.setx(340)
                speed *= 1.05  # Increase difficulty

                dx_ball = -speed * math.sqrt(1 - dy_ratio**2)
                dy_ball = speed * dy_ratio * (1 if dy_ball > 0 else -1)

                bounce_count += 1
                bounce_display.clear()
                bounce_display.write(
                    "Bounces: {}".format(bounce_count),
                    align="center",
                    font=("Arial", 16, "normal")
                )

            # Left paddle
            if (
                (ball.xcor() < -340)
                and (ball.xcor() > -350)
                and (leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50)
            ):
                ball.setx(-340)
                speed *= 1.05

                dx_ball = speed * math.sqrt(1 - dy_ratio**2)
                dy_ball = speed * dy_ratio * (1 if dy_ball > 0 else -1)

                bounce_count += 1
                bounce_display.clear()
                bounce_display.write(
                    "Bounces: {}".format(bounce_count),
                    align="center",
                    font=("Arial", 16, "normal")
                )

# Graceful exit if window closes
except (turtle.Terminator, Exception):
    pass