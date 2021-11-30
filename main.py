import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to wpm Calculator:)")
    stdscr.addstr("\nPress any key to continue.")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM:{wpm}")

    for i, char in enumerate(current):
        correct = target[i]
        color = curses.color_pair(2)

        if char != correct:
            color = curses.color_pair(3)
        stdscr.addstr(0, i, char, color)


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    curr_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(curr_text) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, curr_text, wpm)
        stdscr.refresh()

        if "".join(curr_text) == target_text or len(curr_text)>len(target_text):
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        elif key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()
        elif len(curr_text) < len(target_text):
            curr_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
