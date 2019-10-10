from pico2d import *
import random

Window_width = 800
Window_height = 600

def Fire_Myjet():
    My_Fire.clip_draw(0, 0, 10, 12, 500, 500)

def handle_events():
    global running
    #내 제트기의 초기 좌표
    global My_x, MY_y
    #내 제트기위 움직임의 좌표
    global dir_x, dir_y
    #배경움직임을 위한 y축 값
    global background_y, background_y1
    #배경움직임에 사용되는 값
    global a, b
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
            elif event.key == SDLK_f:
                Fire_Myjet()
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1
            elif event.key == SDLK_f:
                Fire_Myjet()
    pass


open_canvas()
background = load_image('resource/Aft_resource/background.png')
background_1 = load_image('resource/Aft_resource/background.png')
MyJet = load_image('resource/Aft_resource/jet21.png')
character1 = load_image('resource/Aft_resource/jet2.png')
Enemy1 = load_image('resource/Aft_resource/EnemyJet1.png')
My_Fire = load_image('resource/Aft_resource/Fire_Myjet.png')

running = True
My_x = 800 // 2
My_y = 600 // 2
frame = 0
dir_x = 0
dir_y = 0
background_y, background_y1 = 0, 0
a, b = 900, 300

while running:
    clear_canvas()
    handle_events()
    background.clip_draw(0, 0, 800, 600, Window_width // 2, a + background_y)
    background_1.clip_draw(0, 0, 800, 600, Window_width // 2, b + background_y1)
    Enemy1.clip_draw(0, 0, 40, 80, 700, 300)
    MyJet.clip_draw(frame * 40, 0, 40, 80, My_x, My_y)
#    My_Fire.clip_draw(0, 0, 10, 12, 500, 500)
    update_canvas()


#배경의 움직이는 속도
    background_y -= 3
    background_y1 -= 3

#배경의 컨베이어벨트
    if a + background_y == -300:
        a = 900
        background_y = 0

    if b + background_y1 == -300:
        b = 900
        background_y1 = 0



    frame = (frame + 1) % 6
    My_x += dir_x * 20
    My_y += dir_y * 20
    delay(0.1)

# while x < 800:
#     clear_canvas()
#     background.draw(800,600)
#     character.clip_draw(frame * 40, 0, 40, 80, x, 90)
#     character1.clip_draw(frame * 30, 0, 30, 60, x, 200)
#     update_canvas()
#     frame =(frame+1) % 6
#     x += 5
#     delay(0.1)
#     get_events()


close_canvas()
