import pygame , random
pygame.init()

window_width = 800
window_height = 800
dimension = (window_width , window_height)
screen = pygame.display.set_mode(dimension)
pygame.display.set_caption("Feed The Dragon")

WHITE = (255,255,255)
BLACK = (0,0,0)


font = pygame.font.Font("font.ttf",20)
font2 = pygame.font.Font("font.ttf", 18)
font3 = pygame.font.Font("font.ttf", 23)

apple = pygame.image.load("apple.png")
apple_rec = apple.get_rect()
apple = pygame.image.load("apple.png")
apple_rec = apple.get_rect()
apple_rec.center = (window_width // 2, random.randint(110, window_height - 80))

score = 0
score_text = font.render("Score : " + str(score), True, BLACK)
score_rec = score_text.get_rect()
score_rec.topleft = (10,10)

background = pygame.image.load("bluemountain.jpg")
dragon = pygame.image.load("dragon.png")
dragon_left = pygame.image.load("dragon_left.png")
dragon_right = pygame.image.load("dragon_right.png")
dragon = dragon_right
dragon_rec = dragon.get_rect()

title_text = font3.render("Feeding Dragon", True,BLACK)
title_rec = title_text.get_rect()
title_rec.centerx = window_width // 2
title_rec.y = 10

totalfood = 0
totalfood_text = font.render("Food Eaten : ", True,BLACK)
totalfood_rec = totalfood_text.get_rect()
totalfood_rec.centerx = window_width // 2
totalfood_rec.y = 40

lives = 5
lives_text = font.render("Lives : " + str(lives), True,BLACK)
lives_rec = lives_text.get_rect()
lives_rec.topright = (760,10)

boost = 0
boost_text = font.render("Boost : " + str(boost), True,BLACK)
boost_rec = boost_text.get_rect()
boost_rec.topright = (760,40)

foodpoint = 100
foodpoint_text = font.render("Food Points : " + str(foodpoint), True,BLACK)
foodpoint_rec = foodpoint_text.get_rect()
foodpoint_rec.topleft = (10,40)


gameover_text = font.render("GAME OVER ", True, BLACK, None)
gameover_rec = gameover_text.get_rect()
gameover_rec.center = (window_width//2,window_height//2)

continue_text = font2.render("press any key to continue !", True,BLACK,None)
continue_rec = continue_text.get_rect()
continue_rec.center = (window_width//2, 400)


dragon_rec.centery = 600
dragon_rec.centerx = window_width // 2
apple_y = 0

BOOST_DECAY = 0.01
BOOST_DURATION = 120 #2 second dalam 60 fps
boost_time = 0
FOOD_ACCEL = 0.25
FOOD_VEL = 4
VELOCITY = 5
BOOST_VELOCITY = 7
FPS = 60
clock = pygame.time.Clock()

pygame.mixer.music.load("bgm2.mp3")
pygame.mixer.music.play(-1,0,0)
pygame.mixer.music.set_volume(0.5)

running = True
while running:
    rect_surface = pygame.Surface((window_width,75))
    rect_surface.fill(WHITE)
    screen.blit(background,(0,0))
    screen.blit(dragon,dragon_rec)
    screen.blit(apple, apple_rec)
    rect_surface.blit(score_text,score_rec)
    rect_surface.blit(title_text,title_rec)
    rect_surface.blit(totalfood_text,totalfood_rec)
    rect_surface.blit(lives_text,lives_rec)
    rect_surface.blit(boost_text,boost_rec)
    rect_surface.blit(foodpoint_text,foodpoint_rec)

    screen.blit(rect_surface, (0,0))

    pygame.draw.line(screen, BLACK, (0,75), (window_width,75), 3)
    
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and dragon_rec.left >0 :
        dragon = dragon_left
        dragon_rec.x -= VELOCITY
    if keys[pygame.K_d] and dragon_rec.right <window_width:
        dragon = dragon_right
        dragon_rec.x += VELOCITY
    if keys[pygame.K_w] and dragon_rec.top >80:
        dragon_rec.y -= VELOCITY
    if keys[pygame.K_s] and dragon_rec.bottom <window_height:
        dragon_rec.y += VELOCITY
    if keys[pygame.K_SPACE] and boost >= 1:
        if dragon_rec.left > 0 and dragon_rec.right < window_width and dragon_rec.top > 80 and dragon_rec.bottom < window_height:
            if keys[pygame.K_a]:
                dragon = dragon_left
                dragon_rec.x -= BOOST_VELOCITY
            if keys[pygame.K_w]:
                dragon_rec.y -= BOOST_VELOCITY
            if keys[pygame.K_s]:
                dragon_rec.y += BOOST_VELOCITY
            if keys[pygame.K_d]:
                dragon = dragon_right
                dragon_rec.x += BOOST_VELOCITY
            boost = boost - 1
            boost_time = BOOST_DURATION
    if keys[pygame.K_SPACE] and boost_time > 0:
        boost_time -= 1
        boost_text = font.render("Boost : " + str(boost), True,BLACK)
    if keys[pygame.K_SPACE] and boost > 0 and boost_time == 0:
        boost -= BOOST_DECAY
        boost = max(0, boost)
        boost_text = font.render("Boost : " + str(int(boost)), True, BLACK)
    if dragon_rec.colliderect(apple_rec):
        score += foodpoint
        boost += 10
        apple_rec.x = window_width + 100
        apple_rec.y = random.randint(110, window_height - 80)
        FOOD_VEL += FOOD_ACCEL
        score_text = font.render("Score : " + str(score), True, BLACK)
        totalfood = totalfood + 1
        totalfood_text = font.render("Food Eaten : " + str(totalfood), True,BLACK)
        boost_text = font.render("Boost : " + str(boost), True,BLACK)
    if apple_rec.bottom == window_height:
        lives -= 1
        apple_rec.center = (random.randint(0, window_width), 0)
        apple_y = 0
        lives_text = font.render("Lives : " + str(lives), True, BLACK)

    apple_y += FOOD_VEL
    apple_rec.y = apple_y
    if apple_y > window_height:
        apple_rec.center = (random.randint(0, window_width), 0)
        apple_y = 0
    apple_rec.y = apple_y
    
    if lives == 0:
        screen.blit(gameover_text,gameover_rec)
        screen.blit(continue_text, continue_rec)        
        pygame.mixer_music.stop()
        pygame.display.update() 

        pausing = True
        while pausing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pausing == False
                    running == True

                if event.type == pygame.KEYDOWN:
                    pygame.mixer_music.play(-1,0,0)
                    running = True
                    pausing = False
                    lives = 5
                    score = 0
                    totalfood = 0
                    boost = 0
                    dragon_rec.centery = 600
                    dragon_rec.centerx = window_width // 2


                    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
