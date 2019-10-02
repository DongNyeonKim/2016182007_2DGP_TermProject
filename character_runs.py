from pico2d import *
open_canvas()
background = load_image('background.png')
character = load_image('jet2.png')

x = 0
frame = 0
while x < 800:
    clear_canvas()
    background.draw(400,300)
    character.clip_draw(frame * 30, 0, 30, 60, x, 90)
    update_canvas()
    frame =(frame+1) % 6
    x += 5
    delay(0.1)
    get_events()


close_canvas()

