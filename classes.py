# Square VS Eggman
# Классы


from init import *
import random, os, copy
import load_scale_image as lsi


class GroupWithGetItem(pg.sprite.AbstractGroup):
    def __getitem__(self, index):
        return self.sprites()[index]


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
                button_is_press = False
                for i in pg.event.get():
                    if i.type == pg.MOUSEBUTTONDOWN:
                        button_is_press = pg.mouse.get_pressed()[0]
                        
                if a == 0 and button_is_press:
                    return self.press_on_sprite
                else:
                    if (r, g, b) == self.alphacolor:
                        pass
                    elif pg.mouse.get_pressed()[0]:
                        return self.press_on_sprite

class objMiniTime(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(get_file("Graphics", "Images", "microtime.png"))
        self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen.get_width() - 50)
        self.rect.y = random.randint(top_panel_h, screen.get_height() - 50)

        self.type = "objMiniTime"

class PlayerHide(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pg.image.load(get_file("Graphics", "Images", "empty.png"))
        self.rect = img.get_rect()

    def update(self, player_x, player_y):
        self.rect.x = player_x
        self.rect.y = player_y

class Hp(pg.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pg.image.load(get_file("Graphics", "Images", "hp.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.__screen_width = screen.get_width()

    @property
    def geo_x(self):
        # self.screen_width * get / 100 == self.rect.x Это уравнение!

        preliminaryGet = 100 * self.rect.x

        # self.screen_width * get == preliminaryGet

        get = preliminaryGet / self.screen_width
        return get

    @property
    def screen_width(self):
        return self.__screen_width


def loading_Cristall():
    surface = pg.Surface((screen.get_width(), screen.get_height()))
    font1 = pg.font.Font(get_file("Graphics", "Fonts", "load_text.otf"), 50)
    text1 = font1.render("ЗАГРУЗКА", True, (0, 0, 0))
    font2 = pg.font.Font(None, 80)
    text2 = font2.render(". . .", True, (0, 0, 0))
    surface.fill(COLOR_FILL_START)
    surface.blit(text1, (surface.get_width() / 2 - text1.get_width() / 2,
                       surface.get_height() / 2 - text1.get_height() / 2))
    surface.blit(text2, (surface.get_width() / 2 + text1.get_width() / 2,
                       surface.get_height() / 2 - text1.get_height() / 2))
    if screen != surface:
        font1 = pg.font.Font(get_file("Graphics", "Fonts", "load_text.otf"), 50)
        text1 = font1.render("ЗАГРУЗКА", True, (0, 0, 0))
        font2 = pg.font.Font(None, 60)
        text2 = font2.render(". . .", True, (0, 0, 0))
        screen.fill(COLOR_FILL_START)
        screen.blit(text1, (screen.get_width() / 2 - text1.get_width() / 2,
                        screen.get_height() / 2 - text1.get_height() / 2))
        screen.blit(text2, (screen.get_width() / 2 + text1.get_width() / 2,
                       screen.get_height() / 2 - text1.get_height() / 2))
    else:
        pass

    clock.tick(60)
    pg.display.flip()


class Cristall(pg.sprite.Sprite): 
    def __init__(self, x = 0, y = 0):
        super().__init__()

        self.images = []
        self.image = None
        self.next_image = 0
        self.next_image_reverse = False

        if hasattr(self, "class_images"):
            self.images = Cristall.class_images
        else:
            loading_Cristall()
            for i in range(1, 40):
                filename = f"{i:02d}.jpg"
                image = lsi.load_scaled_image(pg, get_file("Graphics", "Videos", "Cristall", filename), 50, 75)
                for i in range(5):
                    self.images.append(image)
            loading_Cristall()
            Cristall.class_images = copy.copy(self.images)

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
        self.image = pg.image.load(get_file("Graphics", "Images", "eggm.png"))
        self.rect = self.image.get_rect()
    
    def move(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y