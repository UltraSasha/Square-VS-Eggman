# Square VS Eggman
# Версия 3.3.


from init import *
from tkinter import messagebox

import random, time, os, json, sys

import instruction
import classes as cls




sys.setrecursionlimit(10_000_000)


have_hack = False


def save(bests_scores: dict) -> None:
    try:
        with open("bests.json", 'r') as file:
            data = json.load(file)
    except:
        with open("bests.json", 'w') as file:
            json.dump({"bests_scores": bests_scores}, 
                      file)
    else:
        try:
            if data["bests_scores"][0][current_name] >= bests_scores[current_name]: 
                with open("bests.json", "w"):
                    json.dump({"bests_scores": data["bests_scores"][0]},
                              file)
            else:
                with open("bests.json", 'w') as file:
                    json.dump({"bests_scores": bests_scores}, 
                              file)
        except:
            with open("bests.json", 'w') as file:
                    json.dump({"bests_scores": bests_scores}, file)



current_name = "Steve"
current_sound = "🔊"

screen_w = 80
screen_y = 80
MON_W, MON_H = resolution()
current_w = int(MON_W * screen_w / 100)
current_h = int(MON_H * screen_y / 100)
font = pg.font.Font(size=50)
try:
    pg.mixer.music.load(get_file("Graphics", "Music", "music.mp3"))
    pg.mixer.music.set_volume(1000)
except pg.error:
    current_sound = False
try:
    sound_money = pg.mixer.Sound(get_file("Graphics", "Sounds", "plus_money.mp3"))
except:
    current_sound = False




def level_up(complexity_index, curr_level, score):
    runMain(complexity_index, curr_level + 1, score + 3)

def end(complexity_index, current_name, font: pg.font.Font, score, color_time, text="Игра завершена!"):
    global current_sound
    if current_sound == "🔊":
        pg.mixer.music.fadeout(3000)

    if load() != {}:
        bests = load()["bests_scores"]
        sum_score = load()["bests_scores"][current_name][1]
    else:
        bests = {current_name: (score, score)}
        sum_score = score
    
    if current_name not in bests or score > bests[current_name][0]:
        bests[current_name][0] = score
        bests[current_name][1] = sum_score + score
        save(bests)
    

    text_over1 = font.render(text + f" Очки: {score}.", True,
                             (color_time['R'], color_time['G'], color_time['B']))
    text_over2 = font.render(f"Что бы играть по новой, жми на кнопку ниже.", True,
                             (color_time['R'], color_time['G'], color_time['B']))
    text_over3 = font.render(f"Твой рекорд: {bests[current_name][0]}, твой общий счёт: {bests[current_name][1]}", True, 
                             (color_time['R'], color_time['G'], color_time['B']))
    text_over4 = font.render(f"Другие рекорды:  ", True, 
                            (color_time['R'], color_time['G'], color_time['B']))
    

    current_name = "Steve" if current_name == "" else current_name
    

    butt_down = pg.rect.Rect(float(current_w * 24 / 100), 
                             float(current_h * 74 / 100),
                             font.render("следующая пара", True, (255, 255, 255)).get_width() + 15, 
                             font.render("следующая пара", True, (255, 255, 255)).get_height())
    
    image_for_play_button = pg.image.load(get_file("Graphics", "Images", "Play_Button.png"))
    play_button = cls.ButtonSprite(
                                   image_for_play_button,
                                   ("is png",),
                                   current_w / 2 - image_for_play_button.get_width() / 2,
                                   current_h * 75 / 100, 
                                   None, "pressed"
                                   )


    see_bests = []
    try:
        other_bests = bests.copy()
        if current_name in other_bests:
            other_bests.pop(current_name)
        
        see_bests = sorted(other_bests.items(), key=lambda x: x[1], reverse=True)
        
    except Exception as e:
        messagebox.showerror(f"Ошибка при загрузке рекордов: {e}")
        see_bests = []
    
    index_bests = 0
    expectation = True

    while expectation:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if not os.path.exists(os.path.join(os.getcwd(), "bests.json")) or load()["bests_scores"] != bests:
                    if messagebox.askyesno("Рекорды не сохранены!", "Рекорды ещё не сохранены. Желаете ли вы их сохранить перед закрытием?", 
                                           icon='question'):
                        save(bests)

                pg.quit()
                expectation = False
                raise SystemExit
                return

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if butt_down.collidepoint(mouse_pos) and see_bests:
                    index_bests = (index_bests + 1) % len(see_bests)

        if play_button.update() == "pressed":
            runMain(complexity_index)
            

        if see_bests:
            text_over5 = f"{see_bests[index_bests][0]}: {see_bests[index_bests][1]}"
        else:
            text_over5 = "<никто кроме вас ещё не играл:(>"


        screen.fill((0, 128, 0))
        
        screen.blit(play_button.image, (play_button.rect.x, play_button.rect.y))

        screen.blit(text_over1, (current_w / 2 - text_over1.get_width() / 2,
                                 current_h / 2 - text_over1.get_height() / 2))
        screen.blit(text_over2, (current_w / 2 - text_over1.get_width() / 2,
                                 current_h / 2 - text_over1.get_height() / 2 + text_over1.get_height() + 10))
        screen.blit(text_over3, (current_w / 2 - text_over1.get_width() / 2,
                                 current_h / 2 - text_over1.get_height() / 2 + text_over1.get_height() + text_over2.get_height() + 20))
        

        screen.blit(text_over4, (current_w * 4 / 100, current_h * 68 / 100))
        screen.blit(font.render(text_over5, True, (0, 0, 0)), 
                   (text_over4.get_rect().right + 50, current_h * 68 / 100))
        

        if see_bests and len(see_bests) > 1:
            pg.draw.rect(screen, (0, 0, 0), butt_down)
            screen.blit(font.render("следующая пара", True, (255, 255, 255)), 
                       (butt_down.x + 5, butt_down.y))

        pg.display.flip()
        clock.tick(60)
        

def start(contn_group: pg.sprite.Group) -> int:
    global screen, current_name, current_sound, current_sound_volume, have_hack

    screen = pg.display.set_mode((current_w, current_h))

    buttons = pg.sprite.Group()
    complexity = ("Easy", "Normal", "Hard")
    complexity_index = 0

    buttons_font = pg.font.Font(get_file("Graphics", "Fonts", "start_buttons_font.otf"), 60)

    contn_group.add(cls.ButtonSprite(buttons_font.render("ИНСТРУКЦИЯ", True, (254, 254, 254)), 
                                     (255, 255, 255), 
                                     30, 
                                     current_h * 92 / 100,
                                     None, "pressed2"))
    
    try:
        with open("password.txt", encoding="utf-8") as file:
            password_for_hack = file.read().lower()
            if len(password_for_hack) > 8:
                raise Exception("Длина пароля для активации читов не должна превышать 8 символов!")
    except FileNotFoundError:
        password_for_hack = " "
        
    index_for_passHack = 0
        
    
    """
    contn_group.add(
                   cls.ButtonSprite(
                                    buttons_font.render("МАГАЗИН", True, (254, 254, 254)), 
                                    (255, 255, 255), current_w - buttons_font.render("МАГАЗИН", True, (254, 254, 254)).get_width() - 30, 
                                    current_h * 92 / 100, None, "pressed3"
                                    )
                    )
    """

    settbutton = cls.ButtonSprite(pg.transform.scale(pg.image.load(get_file("Graphics", "Images", "setting.png")), (80, 80)),
                                    ("is png",),
                                    current_w / 2 - 250 / 2 / 2 + 28,
                                    current_h - pg.image.load(get_file("Graphics", "Images", "Instruct_Button.jpg")).get_height() - 40,
                                    None, "pressed1")
    buttons.add(settbutton)

    strelki = (
                cls.ButtonSprite(pg.image.load(get_file("Graphics", "Images", "strelkaUP.png")),
                                ("is png",),
                                current_w / 2 - 250 / 2 / 2 + 59.5,
                                current_h * 90 / 100,
                                None, "pressed"),
              )


    run = True
    settings_complexty_is_open = False
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: raise SystemExit

            if event.type == pg.KEYUP:
                try:
                    expected_letter = password_for_hack[index_for_passHack]
                    if event.key == pgConstantsDict[f"K_{expected_letter}"]:
                        index_for_passHack += 1
                    else:
                        index_for_passHack = 0
                except:
                    index_for_passHack = 0

        screen.blit(pg.image.load(get_file("Graphics", "Images", "background_start.png")), screen.get_rect())

        big_font = pg.font.Font(get_file("Graphics", "Fonts", "load_text.otf"), 50)
        text_welcome = big_font.render("Square VS Eggman", True, (0, 0, 0))

        mini_font = pg.font.Font(None, 25)
        text_instruction1 = mini_font.render(f"Что бы увидеть инструкцию,", True, (0, 0, 0))
        text_instruction2 = mini_font.render(f"            нажми i.", True, (0, 0, 0))


        # screen.blit(text_instruction1, (current_w / 2 - 95, current_h - 40))
        # screen.blit(text_instruction2, (current_w / 2 - 100, current_h - 20))
        screen.blit(text_welcome, (current_w / 2 - text_welcome.get_width() / 2, 
                                   current_h / 2 - text_welcome.get_height() / 2 - current_h * 25 / 100))
        for item in contn_group:
            result_update_contn = item.update()
            if result_update_contn == "pressed1":
                screen = pg.display.set_mode((current_w, current_h), pg.RESIZABLE)
                if complexity_index is not None:
                    try:
                        return complexity_index, purchased # type: ignore
                    except:
                        return complexity_index
                else:
                    try:
                        return 0, purchased # type: ignore
                    except: 
                        return 0
            
            if result_update_contn == "pressed2":
                current_name, current_sound, current_sound_volume = instruction.instruction(current_name, current_sound)
                pg.mixer.music.set_volume(current_sound_volume)

            """Пока убрал магазин.
            if result_update_contn == "pressed3":
                if load():
                    purchased = shop.open_shop(load()["bests_scores"][1][current_name])
                else:
                    purchased = shop.open_shop(0)
            """

        if strelki[0].update() == "pressed":
            complexity_index += 1


        if settings_complexty_is_open:
            try:
                complexity_text = font.render(complexity[complexity_index], True, (0, 0, 0))
                screen.blit(complexity_text,
                            (current_w / 2 - 250 / 2 / 2 + 59.5 - complexity_text.get_width() - 10,
                             current_h * 93 / 100))
            except IndexError:
                complexity_index = 0

        if settbutton.update() == "pressed1":
            buttons.remove(settbutton)
            buttons.add(strelki[0])
            settings_complexty_is_open = True

        if len(password_for_hack) - 1 == index_for_passHack:
            have_hack = True

        contn_group.draw(screen)
        buttons.draw(screen)

        pg.display.flip()
        clock.tick(60)



def runMain(complexity_index, # purchased={"щит": 0, "часы": 0, "нитро": 0, "удвоитель": 0},
            lvl=1, score=0):
    global current_name, current_sound, current_sound_volume, screen, current_w, current_h


    sprites = pg.sprite.Group()
    hide_sprites = pg.sprite.Group()
    hpes = cls.GroupWithGetItem()
    cristalles = pg.sprite.Group()
    contn_group = pg.sprite.Group()


    color_fill = COLOR_FILL_START

    PRESSED = "pressed"
    speeds_player = {"Easy": 5, "Normal": 9, "Hard": 15}


    complexity = ("Easy", "Normal", "Hard")[complexity_index if complexity_index else 0]


    if current_sound == "🔊":
        pg.mixer.music.play(-1)
    else:
        pg.mixer.music.stop()


    P_SIZE = 40
    p = pg.Rect(180, 180, P_SIZE, P_SIZE)
    p_isCollideEnemy = False
    standart_speed_p = speeds_player[complexity]
    speed_p = standart_speed_p
    turbo_speed = 9
    p_is_turbo = False
    turbo_ost = 100
    turbo_sekmer = time.time_ns() / 1_000_000_000
    turbo_lst = []
    player_hide = cls.PlayerHide()
    hide_sprites.add(player_hide)
    player_isCollide_cristalles = False
    p_is_drive_x = False
    p_is_drive_y = False
    hp1 = cls.Hp(current_w * 5 / 100, current_h * 8 / 100); 
    hp2 = cls.Hp(current_w * 10 / 100, current_h * 8 / 100); 
    hp3 = cls.Hp(current_w * 15 / 100, current_h * 8 / 100)
    hpes.add(hp1, hp2, hp3)

    E_SIZE = 40
    eggm = pg.rect.Rect(400, 400, E_SIZE, E_SIZE)
    eggman = cls.Eggman()
    eggman.move(eggm.x, eggm.y)
    sprites.add(eggman)
    drive_e = standart_speed_p / 2.3
    MINUS_DRIVE_EGGM = 2

    coin_xBegin = 10
    coin_xFinish = int(current_w - 10)

    coin_yBegin = int(top_panel_h + 10)
    coin_yFinish = int(current_h - 10)

    time_retarder = cls.objMiniTime()
    sprites.add(time_retarder)
    time_is_retach = bool(False)

    cristall = cls.Cristall(random.randint(40, current_w - 40), random.randint(top_panel_h, current_h - 40))
    cristalles.add(cristall)
    
    text_welcome = pg.font.Font(size=75).render("Square VS Eggman", True, (0, 0, 0))

    contn = cls.ButtonSprite(pg.image.load(get_file("Graphics", "Images", "Play_Button.png")),
                            ("is png",),
                            current_w / 2 - 250 / 2, 
                            current_h / 2 + text_welcome.get_height() + current_h * 0.1 / 100, None, PRESSED)
    contn_group.add(contn)

    if have_hack:
        p_help = pg.rect.Rect(current_w, current_h, P_SIZE, P_SIZE)
        alive_p_help = True
        speed_pHelp = 0.6

    coins_types = [{'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (255, 240, 0), 'plus': 3, 'minus': 0, 'size': random.randint(10, 20)},
                   {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (127, 255, 0), 'plus': 1, 'minus': 0, 'size': random.randint(10, 20)},
                   {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)),
                        'color': (0, 118, 0), 'plus': 0, 'minus': -1, 'size': random.randint(10, 15)},
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
    start_time3 = None

    timer_stay_time_start = 8
    timer_stay_time = None
    timer_stay_time_start2 = 0.2
    timer_stay_time2 = None


    counter = 0

    remaining_time = 120
    last_time = start_time

    color_time = {'R': 0, 'G': 0, 'B': 0}

    run = bool(1)

    pause = False
    # pause setting
    text_pause = font.render("Игра на паузе.", True, (0, 0, 0))
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if load():
                    try:
                        bests_scores[current_name]
                    except: 
                        bests_scores = load()["bests_scores"]
                        if current_name not in bests_scores:
                            bests_scores[current_name] = (score, score)

                    bests_scores[current_name] = (bests_scores[current_name][0], bests_scores[current_name][1])
                else:
                    bests_scores = {current_name: (score, score)}

                save({current_name: (score, score)}) # , purchased)

                run = False
                raise SystemExit

            if event.type == pg.VIDEORESIZE:
                current_w, current_h = event.size
                coin_xFinish = int(current_w - 10)
                coin_yBegin = int(top_panel_h + 10)
                coin_yFinish = int(current_h - 10)


        if pause:
            if current_sound == "🔊":
                pg.mixer.music.fadeout(3000)

            screen.fill((0, 128, 0))

            result_update_contn = contn.update()
            if result_update_contn == PRESSED:
                if current_sound == "🔊":
                    pg.mixer.music.play(-1)
                pause = False
            
            screen.blit(text_pause, (current_w / 2 - text_pause.get_width() / 2, 
                        current_h / 2 - text_pause.get_height() / 2))
            contn_group.draw(screen)

        else:
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
                p_is_drive_x = True
            else: p_is_drive_x = False

            if key[pg.K_d] or key[pg.K_KP6] or key[pg.K_RIGHT]:
                p.x += speed_p
                p_is_drive_x = True
            else: p_is_drive_x = False

            if key[pg.K_w] or key[pg.K_KP8] or key[pg.K_UP]:
                p.y -= speed_p
                p_is_drive_y = True
            else: p_is_drive_y = False

            if key[pg.K_s] or key[pg.K_KP5] or key[pg.K_DOWN]:
                p.y += speed_p
                p_is_drive_y = True
            else: p_is_drive_y = False

            if key[pg.K_SPACE]:
                if turbo_ost > 0:
                    speed_p += turbo_speed
                else:
                    speed_p = standart_speed_p
                if key[pg.K_d] or key[pg.K_KP6] or key[pg.K_RIGHT] or key[pg.K_w] or key[pg.K_KP8] or key[pg.K_UP] or key[pg.K_s] or key[pg.K_KP5] or key[pg.K_DOWN]:
                    if turbo_ost > 0:
                        p_is_turbo = True
                        turbo_ost -= 0.5
                    else: p_is_turbo = False
            else:
                speed_p = 5; p_is_turbo = False

            if key[pg.K_i]:
                current_name, current_sound, current_sound_volume = instruction.instruction(current_name, current_sound)
                pg.mixer.music.set_volume(current_sound_volume)

                if current_sound == "🔇":
                    pg.mixer.music.fadeout(3000)
                elif current_sound == "🔊" and pg.mixer.music.get_busy() == False:
                    pg.mixer.music.play()

            if key[pg.K_ESCAPE]:
                pause = True

            p.x = max(0, p.x)
            p.x = min(current_w - P_SIZE, p.x)

            p.y = max(top_panel_h, p.y)
            p.y = min(current_h - P_SIZE, p.y)

            if have_hack:
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


            if time.time_ns() / 1_000_000_000 - turbo_sekmer >= 2:
                turbo_sekmer = time.time_ns() / 1_000_000_000
                turbo_ost += 1.999999999999999999999999999999999999999999999999


            for i in coins_types:
                if p.collidepoint(i['geo']):
                    if current_sound == "🔊":
                        try:
                            sound_money.set_volume(current_sound_volume)
                        except NameError: sound_money.set_volume(100)

                    i['geo'] = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish));
                    i['size'] = random.randint(10, 30)

                    if i['minus'] == -1 and len(hpes) <= 1:
                        end(complexity_index, current_name, font, score, color_time, "Ты подорвался на мине!")
                    elif i['minus'] == -1:
                        hpes.remove(hpes.sprites()[-1])
                    else:
                        score += i['plus']; score -= i['minus']

            if eggm.x < p.x:
                eggm.x += drive_e
            elif eggm.x > p.x:
                eggm.x -= drive_e

            if eggm.y < p.y:
                eggm.y += drive_e
            elif eggm.y > p.y:
                eggm.y -= drive_e

            eggman.move(eggm.x - 40, eggm.y - 40)

            if have_hack:
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
                end(complexity_index, current_name, font, score, color_time)

            if p.colliderect(eggm) and p_is_turbo == bool(False):
                if p_isCollideEnemy == True: pass
                else:
                    p_isCollideEnemy = True
                    if len(hpes) == 1: 
                        end(complexity_index, current_name, font, score, color_time)
                    else: 
                        hpes.remove(hpes.sprites()[-1])
                        color_fill = (255, 0, 0)
                        start_time3 = time.time()
            else: p_isCollideEnemy = False

            if start_time3 is not None:
                difference3 = time.time() - start_time3
                timer_stay_time2 = timer_stay_time_start2 - difference3
                if timer_stay_time2 <= 0:
                    color_fill = COLOR_FILL_START

            if have_hack: 
                if p_help.colliderect(eggm):
                    alive_p_help = False

            if p.colliderect(eggm) and p_is_turbo: level_up(complexity_index, lvl, score); score += 3

            if time_retarder is not None and pg.sprite.spritecollide(time_retarder, hide_sprites, False):
                sprites.remove(time_retarder)
                time_retarder = None
                time_is_retach = True
                start_time2 = int(time.time())

            if pg.sprite.spritecollide(player_hide, cristalles, False):
                cristalles.remove(cristall)
                cristall = cls.Cristall(random.randint(40, current_w - 40), random.randint(top_panel_h, current_h - 40)) 
                cristalles.add(cristall)
                if player_isCollide_cristalles == False:
                    hpes.add(cls.Hp(hpes[-1].screen_width * (hpes[-1].geo_x + 5) / 100, 
                                    current_h * 8 / 100))
                    player_isCollide_cristalles = True
            else: player_isCollide_cristalles = False

            if time_is_retach:
                drive_e += MINUS_DRIVE_EGGM
                drive_e = min(0.6, drive_e)
            else: 
                drive_e = standart_speed_p / 2.3

            difference2 = None
            screen.fill(color_fill)

            if start_time2 != None:
                difference2 = int(time.time()) - start_time2
                timer_stay_time = timer_stay_time_start - difference2
                screen.blit(font.render(f"До обычного течения времени осталось: {timer_stay_time}", True, (0, 0, 0)), (0, current_h * 15 / 100))

            if timer_stay_time is not None and timer_stay_time <= 0:
                time_retarder = cls.objMiniTime()
                sprites.add(time_retarder)
                time_is_retach = False
                start_time2 = None
                timer_stay_time = None


            current_time_ms = time.time_ns() / 1_000_000

            turbo_lst = [el for el in turbo_lst if current_time_ms - el[0] <= 300]

            if p_is_turbo:
                turbo_lst.append((current_time_ms, pg.rect.Rect(p.x, p.y, 40, 25)))


            try:
                if p_is_drive_x:
                    pg.draw.polygon(
                                    screen, (0, 140, 240), ((turbo_lst[0][1].left, 
                                                            turbo_lst[0][1].top), 

                                                            (turbo_lst[-1][1].right, 
                                                            turbo_lst[-1][1].top), 

                                                            (turbo_lst[-1][1].right,
                                                            turbo_lst[-1][1].bottom), 

                                                            (turbo_lst[0][1].left, 
                                                            turbo_lst[0][1].bottom), 

                                                            (turbo_lst[0][1].left, 
                                                            turbo_lst[0][1].top))
                                    )
                elif p_is_drive_y:
                    pg.draw.polygon(
                                    screen, (0, 140, 240), ((turbo_lst[0][1].left, 
                                                            turbo_lst[0][1].top), 

                                                            (turbo_lst[0][1].right, 
                                                            turbo_lst[0][1].top), 

                                                            (turbo_lst[-1][1].right,
                                                            turbo_lst[-1][1].bottom), 

                                                            (turbo_lst[-1][1].left, 
                                                            turbo_lst[-1][1].bottom), 

                                                            (turbo_lst[0][1].left, 
                                                            turbo_lst[0][1].top))
                                   )
            except IndexError:
                pass

            cls.PlayerHide.update(player_hide, p.x, p.y)
            cls.Cristall.update(cristall)

            pg.draw.rect(screen, (0, 255, 0), p)
            pg.draw.rect(screen, (255, 0, 0), eggm)
            sprites.draw(screen)
            hpes.draw(screen)
            cristalles.draw(screen)


            if have_hack and alive_p_help:
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
            screen.blit(text_level, (current_w / 2, text_level.get_height() + 20))

            text_score = font.render(f"Очки: {score}", True, (0, 0, 0))
            text_width = text_score.get_width()
            screen.blit(text_score, (current_w - text_width - PADDING_LEFT_RIGHT, 20))


            if not load():
                best = score
            else:
                bests_scores = load()["bests_scores"]
                for i in bests_scores:
                    if i == current_name:
                        best = bests_scores[i][0]

            try:
                text_best = font.render(f"Твой рекорд: {best}", True, (0, 0, 0))                
            except:
                text_best = font.render(f"Твой рекорд: {score}", True, (0, 0, 0))            
            finally:
                try:
                    text_best = font.render(f"Твой рекорд: {best}", True, (0, 0, 0))                
                except:
                    text_best = font.render(f"Твой рекорд: {score}", True, (0, 0, 0))
                text_bestW = text_best.get_width()
                screen.blit(text_best, (current_w - text_bestW - 8, 
                                        text_score.get_height() + 28))
                
            
            text_tust = font.render(f"Запас нитро: {turbo_ost}", True, (0, 0, 255))
            screen.blit(text_tust, 
                        (text_tust.get_width() - 250, 
                         current_h - text_tust.get_height() - 25))

            mini_font = pg.font.Font(None, 25)
            text_instruction1 = mini_font.render(f"Что бы увидеть инструкцию,", True, (0, 0, 0))
            text_instruction2 = mini_font.render(f"            нажми i.", True, (0, 0, 0))
            screen.blit(text_instruction1, (current_w / 2 - 95, current_h - 40))
            screen.blit(text_instruction2, (current_w / 2 - 100, current_h - 20))

            if remaining_time <= 0:
                end(complexity_index, current_name, font, score, color_time)

        pg.display.flip()
        clock.tick(60)

try:
    runMain(start(pg.sprite.Group(cls.ButtonSprite(pg.image.load(get_file("Graphics", "Images", "play_button.png")),
                                    ("is png",),
                                    current_w / 2 - 250 / 2, 
                                    current_h / 2 + pg.font.Font(size=75).render("Square VS Eggman", 
                                    True, 
                                    (0, 0, 0)).get_height() + current_h * 0.1 / 100, 
                                    None, "pressed1"))))
except SystemExit:
    stopShopServer()
    pg.quit()