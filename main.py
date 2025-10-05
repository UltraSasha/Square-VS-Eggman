import pygame, random, time
import tkinter as tk

import instruction


pygame.init()


try:

    def resolution():
        root = tk.Tk()
        root.withdraw()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        return (screen_width, screen_height)

    def topPanelHeight():
        testFont = pygame.font.Font(size=50)
        text = testFont.render(f"Test", True, (255, 255, 255))
        return text.get_height()

    screen_w = 80
    screen_y = 80
    MON_W, MON_H = resolution()
    current_w = MON_W * screen_w / 100
    current_h = MON_H * screen_y / 100
    font = pygame.font.Font(size=50)
    clock = pygame.time.Clock()


    top_panel_h = topPanelHeight() + 20

    screen = pygame.display.set_mode((current_w , current_h), pygame.RESIZABLE)

    pygame.display.set_caption("Squares And Coins")

    try:
        pygame.display.set_icon(pygame.image.load('icon.png'))
    except pygame.error:
        pass


    def level_up(curr_level, score): runMain(curr_level + 1, score + 3)

    def end(font, score, color_time, text = "Игра завершена!"):
        screen.fill((255, 255, 71))
        text_over1 = font.render(text + f" Очки: {score}.", True,
                                (color_time['R'], color_time['G'], color_time['B']))
        text_over2 = font.render(f"Что бы играть по новой, тыкни по пробелу.", True,
                                (color_time['R'], color_time['G'], color_time['B']))

        screen.blit(text_over1, (350, 350))
        screen.blit(text_over2, (350, 400))

        pygame.display.flip()
        expectation = bool(True)

        while expectation:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    expectation = False
                    exit()

            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE]:
                runMain()



    def start():
        global screen
        screen = pygame.display.set_mode((current_w, current_h))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    import sys
                    sys.exit()
            

            screen.fill((255, 255, 71))
            

            text1 = font.render("Игра вот-вот начнётся! Тебе", True, (0, 0, 0))
            text2 = font.render("нужно только нажать пробел!", True, (0, 0, 0))

            big_font = pygame.font.Font(size=75)
            text_welcome = big_font.render("Squares And Coins", True, (0, 0, 0))

            mini_font = pygame.font.Font(None, 25)
            text_instruction1 = mini_font.render(f"Что бы увидеть инструкцию,", True, (0, 0, 0))
            text_instruction2 = mini_font.render(f"            нажми i.", True, (0, 0, 0))
            


            text1_rect = text1.get_rect(center=(current_w // 2, current_h // 2 - 30))
            text2_rect = text2.get_rect(center=(current_w // 2, current_h // 2 + 30))
            
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text_instruction1, (screen.get_width() / 2 - 95, screen.get_height() - 40))
            screen.blit(text_instruction2, (screen.get_width() / 2 - 100, screen.get_height() - 20))
            screen.blit(text_welcome, (screen.get_width() / 3, screen.get_height() / 4))
            

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                screen = pygame.display.set_mode((current_w, current_h), pygame.RESIZABLE)
                return
            
            elif pygame.key.get_pressed()[pygame.K_i]: instruction.instruction()

            pygame.display.flip()
            clock.tick(60)

    def runMain(lvl = 1, score = 0):
        global current_w, current_h

        r = resolution()
        P_SIZE = 40
        p = pygame.Rect(180, 180, P_SIZE, P_SIZE)
        standart_speed_p = 5
        speed_p = 5
        turbo_speed = 9
        p_is_turbo = False
        turbo_lst = []

        E_SIZE = 40
        eggm = pygame.Rect(400, 400, E_SIZE, E_SIZE)
        drive_e = standart_speed_p / 3

        coin_xBegin = 10
        coin_xFinish = int(current_w - 10)

        coin_yBegin = int(top_panel_h + 10)
        coin_yFinish = int(current_h - 10)

        coins_types = [{'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)), 'color': (255, 240, 0), 'plus': 3, 'minus': 0, 'size': random.randint(10, 20)},
                    {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)), 'color': (127, 255, 0), 'plus': 1, 'minus': 0, 'size': random.randint(10, 20)}, 
                    {'geo': (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)), 'color': (255, 255, 71), 'plus': 0, 'minus': -1, 'size': random.randint(10, 15)}]

        coinY = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
        coinG = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
        coinR = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))

        last_score = score
        start_time = int(time.time())

        remaining_time = 120
        last_time = start_time

        color_time = {'R': 0, 'G': 0, 'B': 0}

        run = bool(1)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.VIDEORESIZE:
                    current_w, current_h = event.size
                    coin_xFinish = int(current_w - 10)
                    coin_yBegin = int(top_panel_h + 10)
                    coin_yFinish = int(current_h - 10)

            now = int(time.time())
            difference = now - start_time

            if difference >=1 and now > last_time:
                last_time = now
                remaining_time -= 1

            if remaining_time <= 5:
                color_time['R'] = 255


            key = pygame.key.get_pressed()

            if key[pygame.K_a] or key[pygame.K_KP4] or key[pygame.K_LEFT]:
                p.x -= speed_p

            if key[pygame.K_d] or key[pygame.K_KP6] or key[pygame.K_RIGHT]:
                p.x += speed_p

            if key[pygame.K_w] or key[pygame.K_KP8] or key[pygame.K_UP]:
                p.y -= speed_p

            if key[pygame.K_s] or key[pygame.K_KP5] or key[pygame.K_DOWN]:
                p.y += speed_p

            if key[pygame.K_SPACE]: 
                speed_p += 9
                p_is_turbo = True

            else: speed_p = 5; p_is_turbo = False

            if key[pygame.K_i]:
                instruction.instruction()

            p.x = max(0, p.x)
            p.x = min(current_w - P_SIZE, p.x)

            p.y = max(top_panel_h, p.y)
            p.y = min(current_h - P_SIZE, p.y)

            for i in coins_types:
                if p.collidepoint(i['geo']): 
                    i['geo'] = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish)); i['size'] = random.randint(10, 30)

                    if i['minus'] == -1:
                        end(font, score, color_time, "Ты подорвался на мине!")

                    else: score += i['plus']; score -= i['minus']



            if eggm.x < p.x:
                eggm.x += drive_e
            else:
                eggm.x -= drive_e

            if eggm.y < p.y:
                eggm.y += drive_e
            else:
                eggm.y -= drive_e

            eggm.x = max(0, eggm.x)
            eggm.x = min(current_w - E_SIZE, eggm.x)

            eggm.y = max(top_panel_h, eggm.y)
            eggm.y = min(current_h - E_SIZE, eggm.y)

            if score - last_score >= 5:
                speed_p += 5; standart_speed_p += 5
                last_score = score

            drive_e = standart_speed_p / 3

            if score < 0:
                run = False
                end(font, score, color_time)


            if p.collidepoint(eggm.x, eggm.y) and p_is_turbo == bool(False): end(font, score, color_time)
            
            elif p.collidepoint(eggm.x, eggm.y) and p_is_turbo: level_up(lvl, score); score += 3


            screen.fill((255, 255, 71))


            if p_is_turbo:
                if len(turbo_lst) <= 40:
                    turbo_lst.append(pygame.rect.Rect(p.x, p.y, 45, 25))
                else:
                    for i in range(0, 1):
                        turbo_lst.pop(0)

            for i in turbo_lst:
                pygame.draw.rect(screen, (0, 140, 240), i)

            pygame.draw.rect(screen,(0, 255, 0), p)
            pygame.draw.rect(screen, (255, 0, 0), eggm)

            for i in coins_types:
                pygame.draw.circle(screen, i['color'], i['geo'], i['size'])


            PADDING_LEFT_RIGHT = current_w * 2 / 100

            remaining_minutes = remaining_time // 60
            remaining_seconds = remaining_time % 60

            text_time = font.render(f"Оставшееся время: {remaining_minutes:02d}:{remaining_seconds:02d}", True, (color_time['R'], color_time['G'], color_time['B']))
            screen.blit(text_time, (PADDING_LEFT_RIGHT, 20))

            text_level = font.render(f"Уровень {lvl}", True, (0, 0, 0))
            screen.blit(text_level, (screen.get_width() / 2, text_level.get_height() + 20))

            text_score = font.render(f"Очки: {score}", True, (0, 0, 0))
            text_width = text_score.get_width()
            screen.blit(text_score, (current_w - text_width - PADDING_LEFT_RIGHT,  20))

            mini_font = pygame.font.Font(None, 25)
            text_instruction1 = mini_font.render(f"Что бы увидеть инструкцию,", True, (0, 0, 0))
            text_instruction2 = mini_font.render(f"            нажми i.", True, (0, 0, 0))
            screen.blit(text_instruction1, (screen.get_width() / 2 - 95, screen.get_height() - 40))
            screen.blit(text_instruction2, (screen.get_width() / 2 - 100, screen.get_height() - 20))

            if remaining_time <= 0:
                end(font, score, color_time)

            pygame.display.flip()
            clock.tick(60)

    start()
    runMain()


except:
    pass