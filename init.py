# Square VS Eggman
# Инициализация


from pygame.constants import __dict__ as pgConstantsDict

import pygame as pg, shop


from tkinter import messagebox

import tkinter as tk
import json


import os, sys, threading, atexit


def resolution():
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return (screen_width, screen_height)


os.environ['SDL_VIDEO_WINDOW_POS'] = f"{resolution()[0] * 10 // 100},{resolution()[1] * 10 // 100}"


pg.init()
serverThread = threading.Thread(target=shop.go)
serverThread.start()
ADDRES_FOR_SHOP_ITEMS = "http://192.168.1.68:8000/items"


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


def get_file(*args):
    resolve_file = os.path.join(*args)

    try:
        if not os.path.exists(resolve_file):
            resolve_file = os.path.join("_internal", *args)
        if not os.path.exists(resolve_file):
            resolve_file = os.path.join(sys._MEIPASS, *args)
    except: pass

    return resolve_file
       

screen = pg.display.set_mode(resolution(), pg.RESIZABLE)
pg.display.set_caption("Square VS Eggman")
try:
    pg.display.set_icon(pg.image.load(get_file("Graphics", "Icon", "icon.png")))
except:
    pass


top_panel_h = topPanelHeight() + 15

COLOR_FILL_START = (0, 128, 0)
clock = pg.time.Clock()

@atexit.register
def stopShopServer():
    if shop.uvicorn_server is not None:
        shop.uvicorn_server.should_exit = True
        serverThread.join()
        shop.uvicorn_server = None