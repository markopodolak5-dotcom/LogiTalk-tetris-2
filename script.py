import random
import turtle


window = turtle.Screen()
window.title("Простий Тетріс на Turtle")
window.bgcolor("black")
window.setup(width=400, height=500)
window.tracer(0)


GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_SIZE = 20


START_X = -100
START_Y = 180


SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

COLORS = ["cyan", "yellow", "purple", "green", "red", "blue", "orange"]


grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


current_shape = None
current_color = None
current_x = 3
current_y = 0
score = 0



def draw_square(x, y, color):
    """Малює один квадратик на екрані."""
    pen.goto(START_X + x * GRID_SIZE, START_Y - y * GRID_SIZE)
    pen.color(color)
    pen.begin_fill()
    for _ in range(4):
        pen.forward(GRID_SIZE - 1)
        pen.right(90)
    pen.end_fill()


def draw_grid():
    """Малює всю сітку гри та поточну фігуру."""
    pen.clear()


    pen.color("white")
    pen.penup()
    pen.goto(START_X - 2, START_Y + 2)
    pen.pendown()
    for _ in range(2):
        pen.forward(GRID_WIDTH * GRID_SIZE + 4)
        pen.right(90)
        pen.forward(GRID_HEIGHT * GRID_SIZE + 4)
        pen.right(90)
    pen.penup()


    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col]:
                draw_square(col, row, grid[row][col])


    if current_shape:
        for r, row in enumerate(current_shape):
            for c, val in enumerate(row):
                if val:
                    draw_square(current_x + c, current_y + r, current_color)


    score_pen.clear()
    score_pen.goto(0, 200)
    score_pen.write(
        f"Рахунок: {score}", align="center", font=("Arial", 16, "bold")
    )

    window.update()



def can_move(shape, offset_x, offset_y):
    """Перевіряє, чи може фігура переміститися у вказане положення."""
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                new_x = offset_x + c
                new_y = offset_y + r


                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False

                if new_y >= 0 and grid[new_y][new_x] is not None:
                    return False
    return True


def spawn_shape():
    """Створює нову фігуру зверху."""
    global current_shape, current_color, current_x, current_y
    index = random.randint(0, len(SHAPES) - 1)
    current_shape = SHAPES[index]
    current_color = COLORS[index]
    current_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
    current_y = 0

    if not can_move(current_shape, current_x, current_y):

        return False
    return True


def lock_shape():
    """Фіксує фігуру в сітці та видаляє заповнені лінії."""
    global score
    for r, row in enumerate(current_shape):
        for c, val in enumerate(row):
            if val:
                grid[current_y + r][current_x + c] = current_color


    full_rows = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            full_rows.append(row)

    for row in full_rows:
        del grid[row]
        grid.insert(0, [None for _ in range(GRID_WIDTH)])
        score += 100


def rotate(shape):
    """Повертає фігуру за годинниковою стрілкою."""
    return [list(row) for row in zip(*shape[::-1])]



def move_left():
    global current_x
    if can_move(current_shape, current_x - 1, current_y):
        current_x -= 1
        draw_grid()


def move_right():
    global current_x
    if can_move(current_shape, current_x + 1, current_y):
        current_x += 1
        draw_grid()


def move_down():
    global current_y
    if can_move(current_shape, current_x, current_y + 1):
        current_y += 1
        draw_grid()


def rotate_shape():
    global current_shape
    rotated = rotate(current_shape)
    if can_move(rotated, current_x, current_y):
        current_shape = rotated
        draw_grid()



pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("white")

window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(move_down, "Down")
window.onkeypress(rotate_shape, "Up")



def game_loop():
    global current_y
    if can_move(current_shape, current_x, current_y + 1):
        current_y += 1
    else:
        lock_shape()
        if not spawn_shape():
            score_pen.goto(0, 0)
            score_pen.color("red")
            score_pen.write(
                "ГРА ЗАКІНЧЕНА", align="center", font=("Arial", 22, "bold")
            )
            return

    draw_grid()
    window.ontimer(game_loop, 500)



spawn_shape()
draw_grid()
game_loop()

turtle.done()