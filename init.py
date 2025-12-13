# Square And Coins
# Инициализация


import pygame as pg
import tkinter as tk
import json

try:
    import hak
    have_hak = True
except:
    have_hak = False

import os


def resolution():
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return (screen_width, screen_height)


os.environ['SDL_VIDEO_WINDOW_POS'] = f"{resolution()[0] * 10 // 100},{resolution()[1] * 10 // 100}"


pg.init()




def topPanelHeight():
    testFont = pg.font.Font(size=50)
    text0 = testFont.render(f"Test", True, (0, 0, 0))
    text1 = testFont.render(f"Test", True, (0, 0, 0))
    text2 = testFont.render(f"Test", True, (0, 0, 0))
    text3 = testFont.render(f"Test", True, (0, 0, 0))
    return text0.get_height() + text1.get_height() + text2.get_height() + text3.get_height()



def load() -> dict:
    try:
        with open("bests.json", "r") as file:
            return json.load(file)
    except: return {}




screen = pg.display.set_mode(resolution(), pg.RESIZABLE)
pg.display.set_caption("Squares And Coins")
try:
    pg.display.set_icon(pg.image.load('icon.png'))
except:
    pass


top_panel_h = topPanelHeight() + 15




COLOR_FILL_START = (0, 128, 0)
clock = pg.time.Clock()