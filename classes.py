# Square And Coins
# Классы


from init import *
import random, os
import load_scale_image as lsi

class Exit(Exception):
    pass

class ButtonSprite(pg.sprite.Sprite):
    def __init__(self, img: pg.Surface, alphacolor: tuple, x, y, in_sprite = None, press_on_sprite = None):
        super().__init__()
        self.image = img
        self.alphacolor = alphacolor
        if alphacolor == ("is png",):
            pass
        else:
            self.image.convert_alpha()
            self.image.set_colorkey(self.alphacolor)

        self.rect = self.image.get_rect(); self.rect.x = x; self.rect.y = y
        self.in_sprite = in_sprite; self.press_on_sprite = press_on_sprite

    def update(self):
        x, y = pg.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            xs = x - self.rect.x
            ys = y - self.rect.y
            r, g, b, a = self.image.get_at((xs, ys))

            if self.in_sprite is not None:
                if self.alphacolor == ("is png"):
                    if a == 0:
                        return  self.in_sprite()
                else:
                    if (r, g, b) == self.alphacolor:
                        pass
                    else:
                        return self.in_sprite
            
            if self.press_on_sprite is not None:
                if a == 0 and pg.mouse.get_pressed()[0]:
                    return self.press_on_sprite
                else:
                    if (r, g, b) == self.alphacolor:
                        pass
                    elif pg.mouse.get_pressed()[0]:
                        return self.press_on_sprite

class objMiniTime(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("Images", "microtime.png"))
        self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen.get_width() - 50)
        self.rect.y = random.randint(top_panel_h, screen.get_height() - 50)

        self.type = "objMiniTime"

class PlayerHide(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pg.image.load(os.path.join("Images", "empty.png"))
        self.rect = img.get_rect()

    def update(self, player_x, player_y):
        self.rect.x = player_x
        self.rect.y = player_y

class Hp(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(os.path.join("Images", "hp.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cristall(pg.sprite.Sprite): 
    def __init__(self, x = 0, y = 0):
        super().__init__()

        self.images = []
        self.image = None
        self.next_image = 0
        self.next_image_reverse = False

        for i in range(1, 40):
            filename = f"{i:02d}.jpg"
            image = lsi.load_scaled_image(pg, os.path.join("Videos/Cristall", filename), 50, 75)
            for i in range(5):
                self.images.append(image)

        self.image = self.images[self.next_image]
        self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        try:
            self.image = self.images[self.next_image]
            self.image.convert_alpha()
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        except IndexError:
            if not self.next_image_reverse:
                self.next_image_reverse = True
                self.next_image = len(self.images) - 2
            else:
                self.next_image_reverse = False
                self.next_image = 1
        else: 
            if not self.next_image_reverse: 
                self.next_image += 1
            else: 
                self.next_image -= 1
    
    def move(self, pl_x = 0, pl_y = 0, min_x = 0, min_y = 0):
        self.rect.x += pl_x
        self.rect.x -= min_x
        self.rect.y += pl_y
        self.rect.y -= min_y

class Eggman(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("Images", "eggm.png"))
        self.rect = self.image.get_rect()
    
    def move(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y