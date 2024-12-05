from telnetlib import FORWARD_X
from tkinter import *
from pickle import dump,load


# область функций
def set_status(status_text,color='black'):
    canvas.itemconfig(text_status_id,text=status_text, fill=color)

def pause_toggle():
    global pause
    pause = not pause
    if pause:
        set_status('ПАУЗА')
    else:
        set_status('Вперед')


def menu_toggle():
    pass


def key_handler(event):
    if game_over:
        return

    if event.keycode == KEY_PAUSE:
        pause_toggle()

    if pause:
        return

    if event.keycode == FORWARD1:
        canvas.move(player1_id, SPEED,0)
    elif event.keycode == KEY_FORWARD_X:
        canvas.move(player2_id, SPEED,0)
    check_finish()


def check_finish():
    global game_over
    coords_player1 = canvas.coords(player1_id)
    coords_player2 = canvas.coords(player2_id)
    coords_finish = canvas.coords(finish_id)

    x1_right = coords_player1[2]
    x1_right = coords_player2[2]
    x1_right = coords_finish[0]



    if x1_right >= x_finish:
        set_status('Победа верхнего игрока', player1_color)
        game_over=True
    if x2_right >= x_finish:
        set_status('Победа нижнего  игрока',player2_color)
        game_over = True

def menu_enter():
    pass


def game_new():
    pass


def game_resume():
    pass


def save_game(event):

    print('Сохроняем')



def load_game(event):

    print('Загружаем')


def game_exit():
    pass


def menu_show():
    pass


def menu_hide():
    pass


def menu_up():
    pass


def menu_down():
    pass


def menu_update():
    pass


def menu_create(canvas):
    pass



# область переменных
game_width = 800
game_height = 800
menu_mode = True
menu_options = ['Возврат в игру', 'Новая игра', 'Сохранить', 'Загрузить', 'Выход']
menu_current_index = 3
menu_options_id = []


KEY_UP = 87
KEY_DOWN = 83
KEY_ESC = 27
KEY_ENTER = 13

player_size = 100
x1, y1 = 50, 50
x2, y2 = x1, y1 + player_size + 100
player1_color = 'red'
player2_color = 'blue'

x_finish = game_width - 50

KEY_PLAYER1 = 39
KEY_PLAYER2 = 68
KEY_PAUSE = 19

SPEED = 12

game_over = False
pause = False

game_width = 800
game_height = 800

# Окно и объекты
window = Tk()
window.title('DMEC')

canvas = Canvas(window, width=game_width, height=game_height, bg='white')
canvas.pack()
menu_create(canvas)
player1 = canvas.create_rectangle(x1,
                                  y1,
                                  x1 + player_size,
                                  y1 + player_size,
                                  fill=player1_color)
player2 = canvas.create_rectangle(x2,
                                  y2,
                                  x2 + player_size,
                                  y2 + player_size,
                                  fill=player2_color)
finish_id = canvas.create_rectangle(x_finish,
                                    0,
                                    x_finish + 10,
                                    game_height,
                                    fill='black')

text_id = canvas.create_text(x1,
                             game_height - 50,
                             anchor=SW,
                             font=('Arial', '25'),
                             text='Вперед!')


# Функции обратного вызова
window.bind('<KeyRelease>', key_handler)
window.bind('<Control-Key-s', save_game)
window.bind('<Control-Key-o', load_game)

window.mainloop()
