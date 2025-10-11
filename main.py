import pygame as pg

import random, time, os
import tkinter as tk

import instruction

try:
    import hak
    have_hak = True
except:
    have_hak = False

pg.init()


def resolution():
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return (screen_width, screen_height)


def topPanelHeight():
    testFont = pg.font.Font(size=50)
    text = testFont.render(f"Test", True, (255, 255, 255))
    return text.get_height()


screen_w = 80
screen_y = 80
MON_W, MON_H = resolution()
current_w = MON_W * screen_w / 100
current_h = MON_H * screen_y / 100
font = pg.font.Font(size=50)
clock = pg.time.Clock()

top_panel_h = topPanelHeight() + 20

screen = pg.display.set_mode((current_w, current_h), pg.RESIZABLE)

pg.display.set_caption("Squares And Coins")

try:
    pg.display.set_icon(pg.image.load('icon.png'))
except:
    pass


class objMiniTime(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("Images", "microtime.png"))
        self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, screen.get_width() - 50)
        self.rect.y = random.randint(50, screen.get_height() - 50)

        self.type = "objMiniTime"

class PlayerHide(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pg.image.load(os.path.join("Images", "empty.png"))
        self.rect = img.get_rect()

    def update(self, player_x, player_y):
        self.rect.x = player_x
        self.rect.y = player_y

def level_up(curr_level, score):
    runMain(curr_level + 1, score + 3)

def end(font, score, color_time, text="Игра завершена!"):
    screen.fill((255, 255, 71))
    text_over1 = font.render(text + f" Очки: {score}.", True,
                             (color_time['R'], color_time['G'], color_time['B']))
    text_over2 = font.render(f"Что бы играть по новой, тыкни по пробелу.", True,
                             (color_time['R'], color_time['G'], color_time['B']))

    screen.blit(text_over1, (350, 350))
    screen.blit(text_over2, (350, 400))

    pg.display.flip()
    expectation = bool(True)

    while expectation:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                expectation = False
                exit()

        key = pg.key.get_pressed()

        if key[pg.K_SPACE]:
            runMain()


def start():
    global screen
    screen = pg.display.set_mode((current_w, current_h))

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                import sys
                sys.exit()

        screen.fill((255, 255, 71))

        text1 = font.render("Игра вот-вот начнётся! Тебе", True, (0, 0, 0))
        text2 = font.render("нужно только нажать пробел!", True, (0, 0, 0))

        big_font = pg.font.Font(size=75)
        text_welcome = big_font.render("Squares And Coins", True, (0, 0, 0))

        mini_font = pg.font.Font(None, 25)
        text_instruction1 = mini_font.render(f"Что бы увидеть инструкцию,", True, (0, 0, 0))
        text_instruction2 = mini_font.render(f"            нажми i.", True, (0, 0, 0))

        text1_rect = text1.get_rect(center=(current_w // 2, current_h // 2 - 30))
        text2_rect = text2.get_rect(center=(current_w // 2, current_h // 2 + 30))

        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text_instruction1, (screen.get_width() / 2 - 95, screen.get_height() - 40))
        screen.blit(text_instruction2, (screen.get_width() / 2 - 100, screen.get_height() - 20))
        screen.blit(text_welcome, (screen.get_width() / 3, screen.get_height() / 4))

        if pg.key.get_pressed()[pg.K_SPACE]:
            screen = pg.display.set_mode((current_w, current_h), pg.RESIZABLE)
            return

        elif pg.key.get_pressed()[pg.K_i]:
            instruction.instruction()

        pg.display.flip()
        clock.tick(60)


def runMain(lvl=1, score=0):
    global current_w, current_h

    sprites = pg.sprite.Group()
    hide_sprites = pg.sprite.Group()

    r = resolution()
    P_SIZE = 40
    p = pg.Rect(180, 180, P_SIZE, P_SIZE)
    standart_speed_p = 5
    speed_p = 5
    turbo_speed = 9
    p_is_turbo = False
    turbo_lst = []

    E_SIZE = 40
    eggm = pg.rect.Rect(400, 400, E_SIZE, E_SIZE)
    drive_e = standart_speed_p / 2.3
    MINUS_DRIVE_EGGM = 2

    coin_xBegin = 10
    coin_xFinish = int(current_w - 10)

    coin_yBegin = int(top_panel_h + 10)
    coin_yFinish = int(current_h - 10)

    time_retarder = objMiniTime()
    sprites.add(time_retarder)

    player_hide = PlayerHide()
    hide_sprites.add(player_hide)

    time_is_retach = bool(False)

    if have_hak:
        p_help = pg.rect.Rect(current_w, current_h, P_SIZE, P_SIZE)
        alive_p_help = True
        speed_pHelp = 0.6

    coins_types = [{'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (255, 240, 0), 'plus': 3, 'minus': 0, 'size': random.randint(10, 20)},
                   {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (127, 255, 0), 'plus': 1, 'minus': 0, 'size': random.randint(10, 20)},
                   {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (255, 255, 71), 'plus': 0, 'minus': -1, 'size': random.randint(10, 15)},
                   {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (0, 131, 110), 'plus': 2, 'minus': 0, 'size': random.randint(10, 20)},
                   {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (255, 255, 255), 'plus': 5, 'minus': 0, 'size': random.randint(10, 20)},]

    # coinY = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
    # coinG = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
    # coinR = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))

    last_score = score
    start_time = int(time.time())
    start_time2 = None
    counter = 0

    remaining_time = 120
    last_time = start_time

    color_time = {'R': 0, 'G': 0, 'B': 0}

    run = bool(1)

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.VIDEORESIZE:
                current_w, current_h = event.size
                coin_xFinish = int(current_w - 10)
                coin_yBegin = int(top_panel_h + 10)
                coin_yFinish = int(current_h - 10)

        now = int(time.time())
        difference = now - start_time

        if difference >= 1 and now > last_time:
            last_time = now
            remaining_time -= 1

        if remaining_time <= 5:
            color_time['R'] = 255

        key = pg.key.get_pressed()

        if key[pg.K_a] or key[pg.K_KP4] or key[pg.K_LEFT]:
            p.x -= speed_p

        if key[pg.K_d] or key[pg.K_KP6] or key[pg.K_RIGHT]:
            p.x += speed_p

        if key[pg.K_w] or key[pg.K_KP8] or key[pg.K_UP]:
            p.y -= speed_p

        if key[pg.K_s] or key[pg.K_KP5] or key[pg.K_DOWN]:
            p.y += speed_p

        if key[pg.K_SPACE]:
            speed_p += 9
            if key[pg.K_d] or key[pg.K_KP6] or key[pg.K_RIGHT] or key[pg.K_w] or key[pg.K_KP8] or key[pg.K_UP] or key[pg.K_s] or key[pg.K_KP5] or key[pg.K_DOWN]:
                p_is_turbo = True

        else:
            speed_p = 5; p_is_turbo = False

        if key[pg.K_i]:
            instruction.instruction()

        p.x = max(0, p.x)
        p.x = min(current_w - P_SIZE, p.x)

        p.y = max(top_panel_h, p.y)
        p.y = min(current_h - P_SIZE, p.y)

        if have_hak:
            counter = 0
            if coins_types[counter]['geo'][0] < p_help.x:
                p_help.x -= speed_pHelp
            elif coins_types[counter]['geo'][1] < p_help.y:
                p_help.y -= speed_pHelp
            elif coins_types[counter]['geo'][0] > p_help.x:
                p_help.x += speed_pHelp
            elif coins_types[counter]['geo'][1] > p_help.y:
                p_help.y += speed_pHelp

            counter += 1

            for i in coins_types:
                if p_help.collidepoint(i['geo']):
                    i['geo'] = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
                    i['size'] = random.randint(10, 30)
                    if i['minus'] == -1:
                        pass
                    else:
                        score += i['plus']; score -= i['minus']

        counter = 0

        for i in coins_types:
            if p.collidepoint(i['geo']):
                i['geo'] = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish));
                i['size'] = random.randint(10, 30)

                if i['minus'] == -1:
                    end(font, score, color_time, "Ты подорвался на мине!")
                else:
                    score += i['plus']; score -= i['minus']

        if eggm.x < p.x:
            eggm.x += drive_e
        else:
            eggm.x -= drive_e

        if eggm.y < p.y:
            eggm.y += drive_e
        else:
            eggm.y -= drive_e

        if have_hak:
            if p_help.x < eggm.x:
                p_help.x += speed_pHelp
            else:
                p_help.x -= speed_pHelp

            if p_help.y < eggm.y:
                p_help.y += speed_pHelp
            else:
                p_help.y -= speed_pHelp

        eggm.x = max(0, eggm.x)
        eggm.x = min(current_w - E_SIZE, eggm.x)

        eggm.y = max(top_panel_h, eggm.y)
        eggm.y = min(current_h - E_SIZE, eggm.y)

        if score - last_score >= 5:
            speed_p += 5;
            standart_speed_p += 5
            last_score = score


        if score < 0:
            run = False
            end(font, score, color_time)

        if p.colliderect(eggm) and p_is_turbo == bool(False):
            end(font, score, color_time)

        elif have_hak: 
            if p_help.colliderect(eggm):
                alive_p_help = False

        if p.collidepoint(eggm.x, eggm.y) and p_is_turbo: level_up(lvl, score); score += 3


        if pg.sprite.spritecollide(time_retarder, hide_sprites, False):
            sprites.remove(time_retarder)
            time_retarder = objMiniTime()
            sprites.add(time_retarder)
            time_is_retach = True
            start_time2 = int(time.time())

        if time_is_retach:
            drive_e += MINUS_DRIVE_EGGM
            drive_e = min(0.6, drive_e)
        else: 
            drive_e = standart_speed_p / 2.3

        difference2 = None

        screen.fill((255, 255, 71))

        if start_time2 != None:
            difference2 = int(time.time()) - start_time2
            screen.blit(font.render(f"До обычного течения времени осталось: {difference2}", True, (0, 0, 0)), (0, screen.get_height() * 30 // 100))


        current_time_ms = time.time_ns() // 1_000_000

        turbo_lst = [el for el in turbo_lst if current_time_ms - el[0] <= 300]

        if p_is_turbo:
            turbo_lst.append((current_time_ms, pg.rect.Rect(p.x, p.y, 45, 25)))

        for item in turbo_lst:
            pg.draw.rect(screen, (0, 140, 240), item[1])

        PlayerHide.update(player_hide, p.x, p.y)
        pg.draw.rect(screen, (0, 255, 0), p)
        pg.draw.rect(screen, (255, 0, 0), eggm)
        sprites.draw(screen)


        if have_hak and alive_p_help:
            pg.draw.rect(screen, (0, 255, 0), p_help)

        for i in coins_types:
            pg.draw.circle(screen, i['color'], i['geo'], i['size'])

        PADDING_LEFT_RIGHT = current_w * 2 / 100

        remaining_minutes = remaining_time // 60
        remaining_seconds = remaining_time % 60

        text_time = font.render(f"Оставшееся время: {remaining_minutes:02d}:{remaining_seconds:02d}", True,
                                (color_time['R'], color_time['G'], color_time['B']))
        screen.blit(text_time, (PADDING_LEFT_RIGHT, 20))

        text_level = font.render(f"Уровень {lvl}", True, (0, 0, 0))
        screen.blit(text_level, (screen.get_width() / 2, text_level.get_height() + 20))

        text_score = font.render(f"Очки: {score}", True, (0, 0, 0))
        text_width = text_score.get_width()
        screen.blit(text_score, (current_w - text_width - PADDING_LEFT_RIGHT, 20))

        mini_font = pg.font.Font(None, 25)
        text_instruction1 = mini_font.render(f"Что бы увидеть инструкцию,", True, (0, 0, 0))
        text_instruction2 = mini_font.render(f"            нажми i.", True, (0, 0, 0))
        screen.blit(text_instruction1, (screen.get_width() / 2 - 95, screen.get_height() - 40))
        screen.blit(text_instruction2, (screen.get_width() / 2 - 100, screen.get_height() - 20))

        if remaining_time <= 0:
            end(font, score, color_time)

        pg.display.flip()
        clock.tick(60)



start()
runMain()