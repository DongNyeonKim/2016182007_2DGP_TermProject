import pico2d
import Game_Framework
import Start_state

pico2d.open_canvas(800,600,sync=True)
Game_Framework.run(Start_state)
pico2d.close_canvas()

