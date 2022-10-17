import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def display_maze(maze, stdscr, track=[]):
    GREEN = curses.color_pair(1)
    YELLOW = curses.color_pair(2)


    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in track:
                stdscr.addstr(i, j*2, "X", YELLOW)
            else:
                stdscr.addstr(i, j*2, value, GREEN)
            


 
def get_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None



def get_track(maze, stdscr):
    start = "O"
    end = "X"
    start_point = get_start(maze, start)

    que = queue.Queue()
    que.put((start_point, [start_point]))

    visited = set()

    while not que.empty():
        current_point, track = que.get()
        r, c = current_point

        stdscr.clear()
        display_maze(maze, stdscr, track)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[r][c] == end:
            return track

        neighbours = get_neighbours(maze, r, c)
        for neighbour in neighbours:
            if neighbour in visited:
                continue

            row, col = neighbour
            if maze[row][col] == "#":
                continue

            new_track = track + [neighbour]
            que.put((neighbour, new_track))
            visited.add(neighbour)


def get_neighbours(maze, row, column):
    neighbours = []

    if row > 0:
        neighbours.append((row-1, column))
    if row + 1 < len(maze):
        neighbours.append((row+1, column)) 
    if column > 0:
        neighbours.append((row, column-1))
    if column + 1 < len(maze[0]):
        neighbours.append((row, column+1))

    return neighbours      


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    get_track(maze, stdscr)
    stdscr.getch()


wrapper(main)
