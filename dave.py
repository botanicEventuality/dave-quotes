#!/usr/bin/env python

import os
import sys
import random
import csv
import curses


script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
quotes_file = script_path + "/data/dave-quotes.csv"
menu = ['  what is your wisdom mr strider  ', '  quit  ']

longest_string = max(menu, key=len)

for i, option in enumerate(menu):
    if option != longest_string:
        menu[i] = menu[i].center(len(longest_string))


def print_menu(stdscr, current_row):
    h, w = stdscr.getmaxyx()

    for i, row, in enumerate(menu):
        x = w//2 - len(row[:w-2])//2
        y = h//2 - len(menu)//2 + i
        if i == current_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row[:w-2])
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row[:w-2])

    stdscr.refresh()


def get_quotes():
    quotes_group = 0
    quotes = []

    with open(quotes_file, 'r', newline='') as quote_list:
        csv_reader = csv.DictReader(quote_list)
        random_row = random.choice(list(csv_reader))
        quotes_group = random_row['group_id']

    with open(quotes_file, 'r', newline='') as quote_list:
        csv_reader = csv.DictReader(quote_list)
        for row in csv_reader:
            if row['group_id'] == quotes_group:
                text = row['text']
                text = text.replace('<span style="color: #e00707">', '')
                text = text.replace('</span>', '')
                quotes.append(text)
   
    return quotes


def print_quotes(stdscr, quotes):
    stdscr.clear()

    h, w = stdscr.getmaxyx()

    max_quotes = (h//4)
    quotes = quotes[-max_quotes:]
    for i, quote, in enumerate(quotes[-max_quotes:]):
        x = w//2 - len(quote[:w-2])//2
        y = i
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(y, x, quote[:w-2])
        stdscr.attroff(curses.color_pair(2))

    stdscr.refresh()


def c_main(stdscr):
    quotes = []
    running = True
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    current_row = 0

    print_menu(stdscr, current_row)
    while running:
        key = stdscr.getch()
 
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                quotes = get_quotes()
                print_quotes(stdscr, quotes)
            elif current_row == 1:
                break
        elif key == curses.KEY_RESIZE:
            stdscr.clear()
            print_quotes(stdscr, quotes)
            stdscr.refresh()
        print_menu(stdscr, current_row)
        stdscr.refresh()


def main():
    curses.wrapper(c_main)


if __name__ == '__main__':
    main()
