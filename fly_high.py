from pico2d import *
import Game_Framework
import Title_state
import Gameover_state
import random
import time


import Background
import Cloud
import Playtime
import My_jet
import My_bullet
import My_friend
import Enemy_jet_1
import Enemy_jet_2
import Enemy_jet_3

name = "Main_state"

Timer = 0
# 적들 숫자 설정(난이도 설정)
Enemy1_quantity = 0
Enemy2_quantity = 0
Enemy3_quantity = 0

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global background, my_jet, my_bullets, my_friend, my_friend_bullets, enemy_jets, enemy_bullets, enemy_jets_2
    global enemy_jets_3_L, enemy_jets_3_R, First_Time, Timer, clouds, playtime

    background = Background.BACKGROUND()
    clouds = Cloud.CLOUD()

    First_Time = 0.0
    playtime = Playtime.PLAYTIME()

    my_jet = My_jet.MY_JET()
    my_bullets = []

    my_friend = My_friend.MY_FRIEND()
    my_friend_bullets = []

    enemy_jets = [Enemy_jet_1.ENEMY_JET() for i in range(Enemy1_quantity)]
    enemy_jets_2 = [Enemy_jet_2.ENEMY_JET_2() for i in range(Enemy2_quantity)]
    enemy_jets_3_L = [Enemy_jet_3.ENEMY_JET_3_L() for i in range(Enemy3_quantity)]
    enemy_jets_3_R = [Enemy_jet_3.ENEMY_JET_3_R() for i in range(Enemy3_quantity)]
    enemy_bullets = []


def exit():
    global my_jet, background, my_bullets, my_friend, my_friend_bullets, enemy_jets, enemy_jets_2, enemy_jets_3_L, enemy_jets_3_R, clouds
    del my_jet
    del background
    del my_bullets
    del my_friend
    del enemy_jets
    del enemy_jets_2
    del enemy_jets_3_L
    del enemy_jets_3_R
    del my_friend_bullets
    del clouds


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Game_Framework.change_state(Title_state)
            elif event.key == SDLK_UP:
                my_jet.move_y += My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_DOWN:
                my_jet.move_y -= My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_RIGHT:
                my_jet.move_x += My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_LEFT:
                my_jet.move_x -= My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_z:
                bullet = My_bullet.MY_BULLET()
                my_bullets.append(bullet)
                My_bullet.fire_sound.play()
            elif event.key == SDLK_x:
                bullet = My_bullet.MY_BULLET()
                bullet.bullet_dir = 1
                my_bullets.append(bullet)
                bullet = My_bullet.MY_BULLET()
                bullet.bullet_dir = 2
                my_bullets.append(bullet)
                My_bullet.fire_sound.play()
                pass

            elif event.key == SDLK_a:
                my_friend.sign += 1
            elif event.key == SDLK_s:
                Gameover_state.Time = playtime.NowTime
                Game_Framework.change_state(Gameover_state)
            elif event.key == SDLK_d:
                if my_jet.no_die == 0:
                    my_jet.no_die = 1
                else:
                    my_jet.no_die = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                my_jet.move_y -= My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_DOWN:
                my_jet.move_y += My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_RIGHT:
                my_jet.move_x -= My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_LEFT:
                my_jet.move_x += My_jet.RUN_SPEED_PPS_JET
            elif event.key == SDLK_z:
                pass
            elif event.key == SDLK_x:
                pass
            elif event.key == SDLK_a:
                pass
            elif event.key == SDLK_s:
                pass


def update():
    global Timer, enemy_bullet, First_Time
    background.update()
    clouds.update()
    my_jet.update()
    if First_Time == 0:
        First_Time = time.time()
    # 내 총알의 충돌처리
    for bullet in my_bullets:
        bullet.update()
        # 적군과 충돌처리
        for enemy in enemy_jets:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        for enemy in enemy_jets_2:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        for enemy in enemy_jets_3_L:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        for enemy in enemy_jets_3_R:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        # 화면을 넘어갈 경우 삭제
        if bullet.y > 700 or bullet.L_y > 700 or bullet.R_y > 700:
            if bullet in my_bullets:
                my_bullets.remove(bullet)

    my_friend.update()

    # 일정 시간마다 아군 총알 발사
    Timer += 1
    if Timer % 50 == 0:
        sbullet = My_friend.MY_FRIEND_BULLET()
        sbullet.bullet_dir = 1
        my_friend_bullets.append(sbullet)
        sbullet = My_friend.MY_FRIEND_BULLET()
        sbullet.bullet_dir = 2
        my_friend_bullets.append(sbullet)

    # 아군 총알의 충돌처리
    for sbullet in my_friend_bullets:
        sbullet.update()
        if sbullet.a_y > 700 or sbullet.b_y > 700:
            if sbullet in my_friend_bullets:
                my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets:
            if collide(enemy, sbullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets_2:
            if collide(enemy, sbullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets_3_L:
            if collide(enemy, sbullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets_3_R:
            if collide(enemy, sbullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)
    # 적군 업데이트
    for enemy in enemy_jets:
        enemy.update()
        if Timer % random.randint(50, 100) == 0 and enemy.explode_check == 0:
            enemy_bullet = Enemy_jet_1.ENEMY_BULLET()
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0 and my_jet.no_die == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    for enemy in enemy_jets_2:
        enemy.update()
        if Timer % random.randint(100, 200) == 0 and enemy.explode_check == 0:
            enemy_bullet = Enemy_jet_2.ENEMY_BULLET_2()
            enemy_bullet.dir = random.randint(0, 2)
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullet.R_x = enemy.x1
            enemy_bullet.R_y = enemy.y1 - 25
            enemy_bullet.L_x = enemy.x1
            enemy_bullet.L_y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0 and my_jet.no_die == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    for enemy in enemy_jets_3_L:
        enemy.update()
        if Timer % random.randint(50, 100) == 0 and enemy.explode_check == 0:
            enemy_bullet = Enemy_jet_3.ENEMY_BULLET()
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0 and my_jet.no_die == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    for enemy in enemy_jets_3_R:
        enemy.update()
        if Timer % random.randint(50, 100) == 0 and enemy.explode_check == 0:
            enemy_bullet = Enemy_jet_3.ENEMY_BULLET()
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0 and my_jet.no_die == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    # 적군 총알 충돌처리
    for enemy_bullet in enemy_bullets:
        enemy_bullet.update()
        if collide(my_jet, enemy_bullet) and my_jet.explode_check == 0 and my_jet.no_die == 0:
            my_jet.explode_check = 1
            if enemy_bullet in enemy_bullets:
                enemy_bullets.remove(enemy_bullet)
        if enemy_bullet.y < -100:
            if enemy_bullet in enemy_bullets:
                enemy_bullets.remove(enemy_bullet)

    # 내 전투기기가 폭발하면 게임 종료
    if my_jet.game_over_sign == 1:
        Gameover_state.Time = playtime.NowTime
        Game_Framework.change_state(Gameover_state)
    pass


def draw():
    clear_canvas()
    background.draw()

    my_jet.draw()
    for bullet in my_bullets:
        bullet.draw()
    my_friend.draw()

    for bullet in my_friend_bullets:
        bullet.draw()

    for enemy in enemy_jets:
        enemy.draw()

    for bullet in enemy_bullets:
        bullet.draw()

    for enemy in enemy_jets_2:
        enemy.draw()

    for enemy in enemy_jets_3_L:
        enemy.draw()

    for enemy in enemy_jets_3_R:
        enemy.draw()
    clouds.draw()
    playtime.draw()
    update_canvas()
