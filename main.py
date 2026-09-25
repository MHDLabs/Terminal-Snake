#!/usr/bin/env python3
import random
import sys
import time

try:
    import curses
except ImportError:
    sys.stderr.write("The curses module is required to run this game.\n")
    sys.exit(1)

STEP = 0.12

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

KEY_TO_DIR = {
    curses.KEY_UP: UP,
    curses.KEY_DOWN: DOWN,
    curses.KEY_LEFT: LEFT,
    curses.KEY_RIGHT: RIGHT,
    ord("w"): UP,
    ord("W"): UP,
    ord("s"): DOWN,
    ord("S"): DOWN,
    ord("a"): LEFT,
    ord("A"): LEFT,
    ord("d"): RIGHT,
    ord("D"): RIGHT,
}

KEY_RESIZE = getattr(curses, "KEY_RESIZE", -2)


def get_layout(scr):
    try:
        lines, cols = scr.getmaxyx()
    except curses.error:
        return 0, 0, 0, False

    if lines <= 0 or cols <= 0:
        return 0, 0, 0, False

    if lines >= 2:
        return cols, lines - 1, 1, True

    return cols, 1, 0, False


def create_snake(w, h, length):
    path = []

    for y in range(h):
        if y % 2 == 0:
            xs = range(w)
        else:
            xs = range(w - 1, -1, -1)

        for x in xs:
            path.append((y, x))
            if len(path) == length:
                path.reverse()
                return path

    path.reverse()
    return path


def choose_direction(snake, w, h):
    if not snake:
        return RIGHT

    body = snake[:-1]

    for d in (RIGHT, DOWN, LEFT, UP):
        ny = snake[0][0] + d[0]
        nx = snake[0][1] + d[1]

        if 0 <= ny < h and 0 <= nx < w and (ny, nx) not in body:
            return d

    if len(snake) >= 2:
        d = (snake[0][0] - snake[1][0], snake[0][1] - snake[1][1])
        if d in OPPOSITE:
            return d

    return RIGHT


def spawn_food(snake, w, h):
    cells = w * h
    if cells <= 0:
        return None

    occupied = set(snake)
    occupied_count = len(occupied)

    if occupied_count >= cells:
        return None

    empty_count = cells - occupied_count

    if empty_count > cells // 2:
        for _ in range(30):
            pos = (random.randrange(h), random.randrange(w))
            if pos not in occupied:
                return pos

    target = random.randrange(empty_count)
    idx = 0

    for y in range(h):
        for x in range(w):
            if (y, x) not in occupied:
                if idx == target:
                    return (y, x)
                idx += 1

    return None


def rebuild_state(w, h, score, previous_over):
    cells = w * h

    if cells <= 0:
        return [], RIGHT, RIGHT, score, None, True

    length = min(3 + max(0, score), cells)
    snake = create_snake(w, h, length)
    direction = choose_direction(snake, w, h)
    pending = direction

    if len(snake) >= cells:
        return snake, direction, pending, score, None, True

    food = spawn_food(snake, w, h)
    game_over = previous_over or food is None

    return snake, direction, pending, score, food, game_over


def step_game(snake, direction, food, score, w, h):
    if not snake:
        return snake, food, score, True

    head_y, head_x = snake[0]
    dy, dx = direction
    ny = head_y + dy
    nx = head_x + dx

    if ny < 0 or ny >= h or nx < 0 or nx >= w:
        return snake, food, score, True

    new_head = (ny, nx)
    grow = new_head == food
    body = snake if grow else snake[:-1]

    if new_head in body:
        return snake, food, score, True

    snake.insert(0, new_head)

    if grow:
        score += 1
        food = spawn_food(snake, w, h)
        if food is None:
            return snake, food, score, True
    else:
        snake.pop()

    return snake, food, score, False


def safe_refresh(scr):
    try:
        scr.refresh()
    except curses.error:
        pass


def safe_addstr(scr, y, x, text, attr=0, size=None):
    if y < 0 or x < 0:
        return

    if size is None:
        try:
            h, w = scr.getmaxyx()
        except curses.error:
            return
    else:
        h, w = size

    if y >= h or x >= w:
        return

    limit = w - x
    if y == h - 1:
        limit -= 1

    if limit <= 0:
        return

    if len(text) > limit:
        text = text[:limit]

    if not text:
        return

    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass


def safe_addch(scr, y, x, ch, size=None):
    if y < 0 or x < 0:
        return

    if size is None:
        try:
            h, w = scr.getmaxyx()
        except curses.error:
            return
    else:
        h, w = size

    if y >= h or x >= w:
        return

    if y == h - 1 and x == w - 1:
        try:
            scr.insch(y, x, ch)
        except curses.error:
            pass
    else:
        try:
            scr.addch(y, x, ch)
        except curses.error:
            try:
                scr.insch(y, x, ch)
            except curses.error:
                pass


def draw(scr, layout, snake, food, score, game_over):
    w, h, offset, show_score = layout

    try:
        scr.erase()
    except curses.error:
        pass

    try:
        screen_size = scr.getmaxyx()
    except curses.error:
        screen_size = (0, 0)

    if show_score:
        if game_over:
            status = "Score: {}  r: restart  q: quit".format(score)
        else:
            status = "Score: {}  q: quit".format(score)

        safe_addstr(scr, 0, 0, status, 0, screen_size)

    if food is not None:
        safe_addch(scr, food[0] + offset, food[1], "*", screen_size)

    for y, x in snake:
        safe_addch(scr, y + offset, x, "O", screen_size)

    if game_over:
        msgs = (
            "GAME OVER",
            "Final score: {}".format(score),
            "r: restart  q: quit",
        )

        start_y = offset + max(0, (h - len(msgs)) // 2)

        for i, msg in enumerate(msgs):
            x = max(0, (w - len(msg)) // 2)
            safe_addstr(scr, start_y + i, x, msg, 0, screen_size)

    safe_refresh(scr)


def draw_waiting(scr):
    try:
        scr.erase()
    except curses.error:
        pass

    safe_addstr(scr, 0, 0, "Waiting for enough terminal space...")
    safe_refresh(scr)


def main(stdscr):
    try:
        curses.curs_set(0)
    except Exception:
        pass

    try:
        stdscr.keypad(True)
    except curses.error:
        pass

    layout = get_layout(stdscr)
    w, h, offset, show_score = layout

    snake = []
    direction = RIGHT
    pending = RIGHT
    score = 0
    food = None
    game_over = False

    if w * h > 0:
        snake, direction, pending, score, food, game_over = rebuild_state(w, h, 0, False)

    next_move = time.monotonic() + STEP
    need_draw = True

    while True:
        new_layout = get_layout(stdscr)

        if new_layout != layout:
            layout = new_layout
            w, h, offset, show_score = layout

            if w * h > 0:
                snake, direction, pending, score, food, game_over = rebuild_state(
                    w, h, score, game_over
                )
                next_move = time.monotonic() + STEP
            else:
                snake = []
                food = None

            need_draw = True

        w, h, offset, show_score = layout

        if w * h <= 0:
            draw_waiting(stdscr)

            try:
                stdscr.timeout(200)
            except curses.error:
                pass

            try:
                ch = stdscr.getch()
            except curses.error:
                return

            if ch == 3 or ch == ord("q") or ch == ord("Q"):
                return

            continue

        now = time.monotonic()

        if not game_over and now >= next_move:
            direction = pending
            snake, food, score, game_over = step_game(snake, direction, food, score, w, h)
            next_move = time.monotonic() + STEP
            need_draw = True

        if need_draw:
            draw(stdscr, layout, snake, food, score, game_over)
            need_draw = False

        if game_over:
            try:
                stdscr.timeout(-1)
            except curses.error:
                pass
        else:
            remaining = next_move - time.monotonic()

            if remaining <= 0:
                ms = 0
            else:
                ms = int(remaining * 1000)
                if ms < 1:
                    ms = 1
                elif ms > 120:
                    ms = 120

            try:
                stdscr.timeout(ms)
            except curses.error:
                pass

        try:
            ch = stdscr.getch()
        except curses.error:
            return

        if ch == KEY_RESIZE:
            if hasattr(curses, "update_size"):
                try:
                    curses.update_size()
                except Exception:
                    pass

            need_draw = True
            continue

        if ch != -1:
            if ch == 3 or ch == ord("q") or ch == ord("Q"):
                return

            if game_over:
                if ch == ord("r") or ch == ord("R"):
                    snake, direction, pending, score, food, game_over = rebuild_state(
                        w, h, 0, False
                    )
                    next_move = time.monotonic() + STEP
                    need_draw = True
            else:
                new_dir = KEY_TO_DIR.get(ch)
                if new_dir is not None and new_dir != OPPOSITE[direction]:
                    pending = new_dir


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        sys.stderr.write("Error: {}\n".format(exc))
        sys.exit(1)