# koch_snowflake.py
import argparse
import turtle

def koch(t, length, level):
    if level == 0:
        t.forward(length)
        return
    l = length / 3.0
    koch(t, l, level - 1)
    t.left(60)
    koch(t, l, level - 1)
    t.right(120)
    koch(t, l, level - 1)
    t.left(60)
    koch(t, l, level - 1)

def draw_snowflake(level, size, speed):
    screen = turtle.Screen()
    screen.title(f"Koch snowflake — level {level}")
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(speed)
    t.penup()
    t.goto(-size/2, size/3)
    t.pendown()
    for _ in range(3):
        koch(t, size, level)
        t.right(120)
    t.penup()
    t.goto(0, -size/2 - 20)
    t.pendown()
    screen.update()
    screen.exitonclick()

def parse_args():
    p = argparse.ArgumentParser(description="Draw Koch snowflake (recursively).")
    p.add_argument("-l", "--level", type=int, default=3, help="Recursion level (>=0).")
    p.add_argument("-s", "--size", type=float, default=400.0, help="Size (side length) in pixels.")
    p.add_argument("--speed", type=int, default=0, help="Turtle speed (0 = fastest).")
    return p.parse_args()

def main():
    args = parse_args()
    level = max(0, args.level)
    size = max(10.0, args.size)
    draw_snowflake(level, size, args.speed)

if __name__ == "__main__":
    main()