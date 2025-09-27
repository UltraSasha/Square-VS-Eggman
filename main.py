import pygame, random, time
import tkinter as tk

pygame.init()

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



top_panel_h = topPanelHeight() + 20

screen = pygame.display.set_mode((current_w , current_h), pygame.RESIZABLE)

pygame.display.set_caption("Square And Coins")

try:
    pygame.display.set_icon(pygame.image.load('icon.png'))
except pygame.error:
    pass

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

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            screen.fill((255, 255, 71))
            runMain()

def runMain():
    global current_w, current_h

    r = resolution()
    P_SIZE = 40
    p = pygame.Rect(180, 180, P_SIZE, P_SIZE)
    speed_p = 5
    E_SIZE = 40
    eggm = pygame.Rect(400, 400, E_SIZE, E_SIZE)
    drive_e = 1

    c = pygame.time.Clock()

    coin_xBegin = 10
    coin_xFinish = int(current_w - 10)

    coin_yBegin = int(top_panel_h + 10)
    coin_yFinish = int(current_h - 10)

    coinY = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
    coinG = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))
    coinR = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))

    score = 0
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

        p.x = max(0, p.x)
        p.x = min(current_w - P_SIZE, p.x)

        p.y = max(top_panel_h, p.y)
        p.y = min(current_h - P_SIZE, p.y)

        if p.collidepoint(coinY):
            score += 3
            coinY = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))

        elif p.collidepoint(coinG):
            score += 1
            coinG = (random.randint(coin_xBegin, coin_xFinish), random.randint(coin_yBegin, coin_yFinish))

        elif p.collidepoint(coinR):
            end(font, score, color_time, text="Ты подорвался на мине!")
           
        elif p.collidepoint((eggm.x, eggm.y)):
            end(font, score, color_time)

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
            speed_p += 5
            last_score = score

        drive_e = speed_p / 3

        if score < 0:
            run = False
            end(font, score, color_time)

        screen.fill((255, 255, 71))

        pygame.draw.rect(screen,(0, 255, 0), p)
        pygame.draw.rect(screen, (255, 0, 0), eggm)

        pygame.draw.circle(screen,(255, 255, 0), coinG, 10)
        pygame.draw.circle(screen, (255, 255, 0), coinY, 10)
        pygame.draw.circle(screen, (127, 255, 0), coinG, 10)
        pygame.draw.circle(screen, (255, 255, 71), coinR, 10)

        font = pygame.font.Font(size=50)

        PADDING_LEFT_RIGHT = current_w * 2 / 100

        remaining_minutes = remaining_time // 60
        remaining_seconds = remaining_time % 60

        text_time = font.render(f"Оставшееся время: {remaining_minutes:02d}:{remaining_seconds:02d}", True, (color_time['R'], color_time['G'], color_time['B']))
        screen.blit(text_time, (PADDING_LEFT_RIGHT, 20))

        text_score = font.render(f"Очки: {score}", True, (0, 0, 0))
        text_width = text_score.get_width()
        screen.blit(text_score, (current_w - text_width - PADDING_LEFT_RIGHT,  20))

        if remaining_time <= 0:
            end(font, score, color_time)

        pygame.display.flip()
        c.tick(60)

runMain()