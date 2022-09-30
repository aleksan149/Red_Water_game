import pgzero
import pgzrun
import random
from pgzhelper import *


WIDTH = 800
HEIGHT = 600
TITLE = "RED WATER GAME"

scene = "menu_one"
main_enter = "newgame"
level = 1
behind_screen = (-200, -200)
timer = 0
current_time = 0
scene_timer = 0
score_enemy = 0
water = 0
need = 10
life = 100
game_over = False
go = False

###MENU###
main_logo = Actor("logo", topleft = (0,0))
main_menu = Actor("main_menu", pos = (400,700))
main_rw = Actor("rw", pos = (400,-50))
menu_empty = Actor("menu_2", topleft = (0,0))
menu_empty_2 = Actor("menu_empty", topleft = (0,0))
newgame_text = Actor("newgame_text", pos = (400, 800))
about_text = Actor("about_text", pos = (400, 700))
gameover_text = Actor("gameover_text", pos = (400, 300))
win_text = Actor("win_text", pos = (400, 300))
press_space = Actor("press_space", pos = (400, 700))
kursor = Actor("kursor", pos = (330,690))
health = Actor("health", pos = (35 ,30))
wat_botl = Actor("watbat", pos = (35, 85))


road = Actor("road", topleft = (0,0))
wall = Actor("fon", topleft = (0,0))
sky = Actor("sky", topleft = (0, 0))
lable = Actor("wall_zero", topleft = (0, 0))


player = Actor("armor_stay", pos = (300, 500))
player_idle = ["armor_stay"]
player_walk = ['armor_walk', 'armor_walkk']
player_attack = ["armor_fire"]
player.images = player_idle
player.fps = 4
player.life = life


bullet_speed = 10
enemy_speed = 1
bullets = []
enemys = []
botles = []
enemy_walk = [['green_run_1', 'green_run_2'], ['darkgray_run_1', 'darkgray_run_2'],
              ['blue_run_1', 'blue_run_2']]

bomb_animate = ['bomb_6', 'bomb_7', 'bomb_8', 'bomb_9', 'bomb_10']
bomb = Actor(bomb_animate[0], pos=behind_screen)
bomb.images = bomb_animate
bomb.fps = 5

blood_red = ['blood_2', 'blood_3', 'blood_4', 'blood_5']
blood_green = ['blood_2_green', 'blood_3_green', 'blood_4_green']
blood = Actor(blood_red[0], pos=behind_screen)
blood_gr = Actor(blood_red[0], pos=behind_screen)
blood.images = blood_red
blood_gr.images = blood_green
blood.fps = 4
blood_gr.fps = 4

window = Actor('window', pos=behind_screen)
wind_text = Actor('text_1', pos=behind_screen)

cap_talk = ['general_cl', 'general_op']
cap = Actor(cap_talk[0], pos=behind_screen)
cap.images = cap_talk

hide_mouse()  # Hides the mouse cursor

###SOUNDS###

track_duration = 0

music.set_volume(0.7)
music.play("main_theme")

def music_main_theme():
    music.fadeout(0.5)
    music.set_volume(0.7)
    music.play("main_theme")

def music_theme():
    music.fadeout(0.5)
    music.set_volume(0.2)
    music.play('not_alone')

def oh():
    sounds.bolno.play()


###RAZNOE###

def newgame():
    global go, scene_timer, score_enemy, timer, water, life, enemy_speed
    go = False
    score_enemy = 0
    scene_timer = 0
    timer = 0
    water = 0
    life = 100
    enemy_speed = 1
    botles.clear()
    enemys.clear()
    window.pos = behind_screen
    wind_text.pos = behind_screen
    cap.pos = behind_screen
    player.pos=(300, 500)
    player.image = "armor_stay"
    sky.topleft = (0, 0)
    wall.topleft = (0, 0)
    road.topleft = (0, 0)
    lable.topleft = (0, 0)


def tracker():  # Убрать всплывающее окно по окончании звучания трека
    if current_time + track_duration + 1 < timer:
        window.pos = behind_screen
        wind_text.pos = behind_screen
        cap.pos = behind_screen
        music.set_volume(0.2)

def gameov():
    global scene
    scene = "game_over"

def win():
   global scene
   scene = "menu_win"

def ship():
    global current_time, track_duration, go
    if water >= need and go == False:
        window.pos = (600, 80)
        cap.pos = (490, 105)
        wind_text.pos = (660, 100)
        wind_text.image = 'text_3'
        current_time = timer
        sounds.lets_go.play()
        track_duration = int(sounds.lets_go.get_length())
        clock.schedule_unique(fly, 0.5)
        go = True
        player.pos = behind_screen
    else:
        pass

def fly():
    sounds.rocket.play()
    clock.schedule_unique(win, 3.0)


def captain():
    global track_duration, current_time, timer
    window.pos = (600, 80)
    cap.pos = (490, 105)
    wind_text.pos = (660, 100)
    music.set_volume(0.1)
    if scene_timer == 0 and timer < 30:
        timer = 30
        current_time = timer
        wind_text.image = 'text_1'
        sounds.agent.play()
        track_duration = int(sounds.agent.get_length())
    elif water == need:
        wind_text.image = 'text_2'
        current_time = timer
        sounds.back_to_ship.play()
        track_duration = int(sounds.back_to_ship.get_length())

    else:
        pass






def blood_position():
    blood.pos = behind_screen
    blood_gr.pos = behind_screen

def bomb_position():
    bomb.pos = behind_screen

def create_botle():
    #print("botle created")
    botle = Actor('kanistra')
    botle.x = 1000
    botle.y = player.y
    botles.append(botle)

def move_botle():
    global water
    for botle in botles:
        if keyboard.right and player.images == player_walk:
            botle.x -= 5
        elif keyboard.left and player.images == player_walk:
            botle.x += 5
        if botle.colliderect(player):
            sounds.water_nalil.play()
            botles.remove(botle)
            water +=1
            if water >= 1:
                clock.schedule_unique(captain, 1.0)
            #print(f"Water {water}")


def move_bullets():
    for i in bullets:
        if i.flip_x == True:
            i.x -= bullet_speed
        else:
            i.x += bullet_speed
        if i.x < 0 or i.x > WIDTH:
            bullets.remove(i)


##### BACKGROUND #####
def movie_background():
    global scene_timer
    if go == True:
        lable.y -= 2
    if player.images != player_idle and player.images != player_attack and \
            player.image != "armor_off":
        if keyboard.right and scene_timer != 11:
            sky.x -= 0.5
            road.x -= 5
            wall.x -= 3
            lable.x -= 4
            if road.topleft < (-800, 0):
                road.topleft = (0, 0)
            if wall.topleft < (-1600, 0):
                scene_timer += 1
                wall.topleft = (0, 0)
                lable.topleft = (0, 0)
            if sky.topleft < (-800, 0):
                sky.topleft = (0, 0)


        if keyboard.left and scene_timer != -1:
            sky.x += 0.5
            road.x += 5
            wall.x += 3
            lable.x += 4
            if road.topleft > (0, 0):
                road.topleft = (-800, 0)
            if wall.topleft > (0, 0):
                scene_timer += -1
                wall.topleft = (-1600, 0)
                lable.topleft = (-1600, 0)
            if sky.topleft > (0, 0):
                sky.topleft = (-800, 0)


###PLAYER###
def life_remove():
    for enemy in enemys:
        if player.distance_to(enemy) < 30:
            global life
            life -= 1
            blood.pos = player.pos
            clock.schedule_unique(oh, 0.02)
            clock.schedule_unique(blood_position, 0.0)
    if life < 1:
        life = 0
        player.image = "armor_off"
        player.y = 570
        player.flip_x = False
        clock.schedule(gameov, 3.0)

def on_key_down(key):
    ##### MENU #####
    global scene
    if scene == "menu_one":  # Обработка нажатия клавиш в главном меню
        global main_enter
        if key == keys.UP:
            sounds.chok.play()
            if main_enter == "about":
                kursor.pos = (320, 230)
                main_enter = "newgame"
            elif main_enter == "quit":
                kursor.pos = (350, 290)
                main_enter = "about"
        elif key == keys.DOWN:
            sounds.chok.play()
            if main_enter == "newgame":
                kursor.pos = (350, 290)
                main_enter = "about"
            elif main_enter == "about":
                kursor.pos = (370, 345)
                main_enter = "quit"
        elif key == keys.SPACE:
            if main_enter == "newgame":
                sounds.bell.play()
                scene = "menu_two"
            elif main_enter == "about":
                sounds.bell.play()
                scene = "menu_about"
            elif main_enter == "quit":
                sounds.bell.play()
                music_main_theme()
                quit()
    elif scene == "menu_about":  # меню об игре
        if key == keys.SPACE:
            sounds.bell.play()
            scene = "menu_one"

    elif scene == "menu_two": # меню история, начало новой игры
        if key == keys.SPACE:
            sounds.bell.play()
            press_space.y = 700
            scene = "menu_level"

    elif scene == "menu_level":  # меню показывает номер уровня. Запуск игры!
        global timer, current_time, score
        if key == keys.SPACE:
            newgame()
            scene = "game"
            sounds.bell2.play()
            music_theme()

    elif scene == "menu_win":  # you win
        if key == keys.SPACE:
            press_space.y = 700
            kursor.image = "kursor"
            kursor.pos = (320, 230)
            scene = "menu_one"
            sounds.bell.play()
            music_main_theme()

    elif scene == "game_over":  # GAME OVER
        if key == keys.SPACE:
            press_space.y = 700
            kursor.image = "kursor"
            kursor.pos = (320, 230)
            scene = "menu_one"
            sounds.bell.play()
            music_main_theme()

    elif scene == "game":

        ###PLAYER###
        if key == keys.RIGHT and player.images == player_idle:
            player.flip_x = False
            player.images = player_walk
        elif key == keys.RIGHT and player.flip_x == True:
            player.images = player_idle

        if key == keys.LEFT and player.images == player_idle:
            player.flip_x = True
            player.images = player_walk
        elif key == keys.LEFT and player.flip_x == False:
            player.images = player_idle

        if key == keys.SPACE:
            player.images = player_attack
            sounds.gun.play()
            global bullet
            bullet = Actor("probka")
            bullet.x = player.x
            bullet.y = player.y + 18
            bullet.flip_x = player.flip_x
            if bullet.flip_x == True:
                bullet.x -= 50
            else:
                bullet.x += 50

            bullets.append(bullet)



def on_key_up(key):
    if key == keys.RIGHT and player.images == player_walk and player.flip_x == False:
        player.images = player_idle

    if key == keys.LEFT and player.images == player_walk and player.flip_x == True:
        player.images = player_idle

    if key == keys.SPACE:
        player.images = player_idle








###SCENE###
def scenario():
    if wall.topleft == (0, 0) and scene_timer == 0 or wall.topleft == (-1600, 0) and scene_timer == 0:
        lable.image = 'wall_start'
    elif wall.topleft == (0, 0) and scene_timer == 1 or wall.topleft == (-1600, 0) and scene_timer == 1:
        #print(scene_timer)
        lable.image = 'wall_zero'
        clock.schedule_unique(create_enemy, 0.5)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 2 or wall.topleft == (-1600, 0) and scene_timer == 2:
        #print(scene_timer)
        lable.image = 'wall_tarelka'
        clock.schedule_unique(create_enemy, 0.5)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 3 or wall.topleft == (-1600, 0) and scene_timer == 3:
        #print(scene_timer)
        lable.image = 'wall_zero'
        clock.schedule_unique(create_enemy, 0.5)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 4 or wall.topleft == (-1600, 0) and scene_timer == 4:
        #print(scene_timer)
        lable.image = 'wall_sptarelka'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 5 or wall.topleft == (-1600, 0) and scene_timer == 5:
        #print(scene_timer)
        lable.image = 'wall_meteor'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 6 or wall.topleft == (-1600, 0) and scene_timer == 6:
        #print(scene_timer)
        lable.image = 'wall_radiation'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 7 or wall.topleft == (-1600, 0) and scene_timer == 7:
        #print(scene_timer)
        lable.image = 'wall_zero'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 8 or wall.topleft == (-1600, 0) and scene_timer == 8:
        #print(scene_timer)
        lable.image = 'wall_shatl'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 9 or wall.topleft == (-1600, 0) and scene_timer == 9:
        #print(scene_timer)
        lable.image = 'wall_alienship'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
    elif wall.topleft == (0, 0) and scene_timer == 10 or wall.topleft == (-1600, 0) and scene_timer == 10:
        #print(scene_timer)
        global enemy_speed
        enemy_speed = 3
        lable.image = 'wall_zero'
        clock.schedule_unique(create_enemy, 1.0)
        clock.schedule_unique(create_botle, 2.0)
        clock.schedule_unique(create_botle, 3.0)
    if int(timer) % 20 == 0 and timer > 1:
        #print(int(timer))
        clock.schedule_unique(create_enemy, 1.0)


def colid_label():
    global life
    if player.collide_pixel(lable) and lable.image == 'wall_start' and player.images == player_idle:
        clock.schedule_unique(ship, 0.1)
    elif player.collide_pixel(lable) and timer < 30:
        clock.schedule_unique(captain, 1.0)
    elif player.collide_pixel(lable) and lable.image == 'wall_tarelka':
        life -= 0.1
        clock.schedule_unique(create_enemy, 3.0)
        clock.schedule_unique(oh, 0.02)
        blood.pos = player.pos
        clock.schedule_unique(blood_position, 0.3)
    elif player.collide_pixel(lable) and lable.image == 'wall_sptarelka':
        life -= 0.03
        clock.schedule_unique(create_enemy, 3.0)
        clock.schedule_unique(oh, 0.02)
        blood.pos = player.pos
        clock.schedule_unique(blood_position, 0.3)
    elif player.collide_pixel(lable) and lable.image == 'wall_radiation':
        life -= 0.03
        clock.schedule_unique(create_enemy, 3.0)
        clock.schedule_unique(oh, 0.02)
        blood.pos = player.pos
        clock.schedule_unique(blood_position, 0.3)
    elif player.collide_pixel(lable) and lable.image == 'wall_alienship':
        life -= 0.1
        clock.schedule_unique(create_enemy, 3.0)
        clock.schedule_unique(oh, 0.02)
        blood.pos = player.pos
        clock.schedule_unique(blood_position, 0.3)



###ENEMY###
def create_enemy():
    #print("Enemy created")
    global enemy
    enemy = Actor('green_run_1')
    enemy.images = random.choice(enemy_walk)
    enemy.fps = 4
    enemy.x = WIDTH + random.randint(200, 600)
    enemy.y = player.y
    enemy.flip_x = True
    enemy.life = random.randint(5,11)
    enemys.append(enemy)

def move_enemy():
    for enemy in enemys:
        enemy.animate()
        enemy.x -= enemy_speed
        if enemy.x < -100:
            enemys.remove(enemy)
        if keyboard.right and player.images == player_walk:
            enemy.x -= 3
        elif keyboard.left and player.images == player_walk:
            enemy.x += 3
        for bullet in bullets:
            if enemy.colliderect(bullet):
                blood_gr.pos = enemy.pos
                sounds.pul_metal.play()
                clock.schedule_unique(blood_position, 0.1)
                bullets.remove(bullet)
                enemy.life -= 1
        if enemy.life <= 0:
            bomb.pos = enemy.pos
            sounds.vzryv.play()
            enemys.remove(enemy)
            global score_enemy
            score_enemy += 1
            clock.schedule(bomb_position, 0.8)











###UPDATE###
def update(dt):
    if keyboard.f:
        toggle_fullscreen()
    global timer
    timer += dt
    ###MENU###
    if scene == "menu_one":
        if main_rw.y < 100:
            main_rw.y += 3
        elif main_menu.y > 300:
            main_menu.y -= 5
            kursor.pos = (320, 230)
        elif press_space.y > 550:
            press_space.y -= 3
    elif scene == "menu_about":
        if about_text.y > 300:
            about_text.y -= 1
    elif scene == "menu_two":
        press_space.y =  700
        if newgame_text.y > 300:
            newgame_text.y -= 1
    elif scene == "menu_level":
        if press_space.y > 40:
            press_space.y -= 20

    elif scene == "game":
        scenario()
        if player.image != "armor_off":
            movie_background()
            move_bullets()
            player.animate()
            move_enemy()
            bomb.animate()
            life_remove()
            blood.animate()
            blood_gr.animate()
            move_botle()
            colid_label()
            cap.animate()
            tracker()










###DRAW###
def draw():
    screen.clear()
    if scene == "menu_one":
        main_logo.draw()
        main_rw.draw()
        main_menu.draw()
        press_space.draw()
        kursor.draw()
    elif scene == "menu_about":
        menu_empty.draw()
        about_text.draw()

    elif scene == "menu_two":
        menu_empty.draw()
        newgame_text.draw()

    elif scene == "menu_level":
        menu_empty_2.draw()
        press_space.draw()
        screen.draw.text("LEVEL " + str(level), center=(400, 300), color=(255, 255, 255),
                         fontsize=70)

    elif scene == "game":

        sky.draw()
        wall.draw()
        lable.draw()
        road.draw()
        for botle in botles:
            botle.draw()
        for i in bullets:
            i.draw()
        for i in enemys:
            i.draw()
        bomb.draw()
        player.draw()
        blood.draw()
        blood_gr.draw()
        #Всплывающее окно
        window.draw()
        cap.draw()
        wind_text.draw()
        ###
        #screen.draw.text('Time: ' + str(int(timer)), (15, 10), color=(0, 0, 255), fontsize=30)
        health.draw()
        wat_botl.draw()
        screen.draw.text('      ' + str(int(life)) + "%", (15, 17), color=(255, 255, 255), owidth=1,
                         ocolor="black", fontsize=40)
        screen.draw.text('      ' + str(int(water)) + "/" + str(need), (15, 70), color=(255, 255, 255), owidth=1,
                         ocolor="black", fontsize=40)

    elif scene == "menu_win":
        menu_empty.draw()
        win_text.draw()

    elif scene == "game_over":
        menu_empty.draw()
        gameover_text.draw()
        screen.draw.text('You killed the enemies: ' + str(int(score_enemy)), (400, 500), color=(255, 255, 255), fontsize=30)

pgzrun.go()