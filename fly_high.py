from pico2d import *


def handle_events():
    global running
    global x
    global dir_x
    global dir_y
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
    pass


open_canvas()
background = load_image('resource/Aft_resource/background.png')
character = load_image('resource/Aft_resource/jet21.png')
character1 = load_image('resource/Aft_resource/jet2.png')

x = 0
frame = 0

running = True
x = 800 // 2
y= 600//2
frame = 0
dir_x = 0
dir_y = 0

while running:
    clear_canvas()
    background.draw(400, 300)
    character.clip_draw(frame * 40, 0, 40, 80, x, y)
    update_canvas()

    handle_events()
    frame = (frame + 1) % 6
    x += dir_x * 20
    y += dir_y * 20
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
