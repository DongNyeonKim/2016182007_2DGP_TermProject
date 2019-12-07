import Game_Framework
import Start_state
import Title_state
import fly_high
from pico2d import *
import json

name = "GameOverState"
image = None
text = None
ani = None
font = None
rank_font = None
Total_font = None
Time = None
rank = []



def enter():
    global image, text, ani, Frame, font, rank_font, Total_font, blinkering, ending_bgm
    ending_bgm = load_music('resource/Sound/111.mp3')
    ending_bgm.set_volume(100)
    ending_bgm.repeat_play()

    image = load_image('resource/Aft_resource/GameoverState.png')
    text = load_image('resource/Aft_resource/gameover.png')
    ani = load_image('resource/Aft_resource/Gameout_ani.png')
    font = load_font('resource/ENCR10B.TTF', 45)
    rank_font = load_font('resource/ENCR10B.TTF', 25)
    Total_font = load_font('resource/ENCR10B.TTF', 30)
    Frame = 0
    blinkering = 0
    save_data()
    load_rank()


def exit():
    global image, text, ani, ending_bgm
    del image
    del text
    del ani
    del ending_bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
                Game_Framework.change_state(Start_state)


def draw():
    clear_canvas()
    image.draw(400, 300)
    text.draw(400, 500)
    if Frame != 5:
        ani.clip_draw(0, 600 * Frame, 800, 600, 400, 300)
    if Frame == 5 and 30 >= blinkering % 60 >= 1:
        font.draw(225, 400, 'LapTime:%3.2fsec' % Time, (255, 0, 128))

    count = 0
    ranking = 0
    if Frame ==5:
        Total_font.draw(250, 300, '[Total Ranking]', (123, 123, 0))
        for data in rank:
            count += 25
            ranking +=1
            if ranking <= 10:
                rank_font.draw(320, 260 - count, '#%d. %3.2f' % (ranking, data[0]), (43, 2, 52))
            pass

    update_canvas()


def update():
    global Frame, blinkering
    if Frame != 5:
        Frame = Frame + 1
        delay(0.5)
    blinkering += 1




def save_data():
    file = []
    with open('Laptime_data.json', 'r') as f:
        files = json.load(f)

    for z in files:
        file.append(z)

    Laptime_data = [float(Time)]
    file.append(Laptime_data)

    with open('Laptime_data.json', 'w') as f:
        json.dump(file, f)


def load_rank():
    global rank

    with open('Laptime_data.json', 'r') as f:
        rank = json.load(f)

    rank.sort(reverse=True)


def pause():
    pass


def resume():
    pass
