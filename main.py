from tkinter import *
from pickle import load, dump

# область функций
def set_status(status_text,color = 'black'):
    canvas.itemconfig(text=status_text, fg=color)


def pause_toggle():
    global pause
    pause = not pause
    if pause:
        set_status("пауза")
    else:
        set_status("вперед")


def menu_toggle():
    pass


def key_handler(event):
    if game_over:
        return

    if event.keycode == KEY_PAUSE:
        pause_toggle()

    if pause:
        return

    set_status('вперед')

    if event.keycode == KEY_UP:
        canvas.move(player1,SPEED, 0 )
    if event.keycode == KEY_UP:
        canvas.move(player2,SPEED, 0 )

    check_finish()

def check_finish():
    global game_over
     coords_player1 = canvas.coords(player1)
     coords_player2 = canvas.coords(player2)
     coords_finish = canvas.coords(finish_id)



def menu_enter():
    pass


def game_new():
    pass


def game_resume():
    pass


def game_save(event):
    x1 = canvas.coords(player1)[0]
    x2 = canvas.coords(player2)[0]
    data = [x1,x2]
    with open('save.data', 'wb') as f:
        dump(data, f)
        set_status("сохранено")


def game_load():
    global x1, x2
    with open("save.data",'rb')as f:
        data = load(f)
        x1, x2 = data
        canvas.coords(player1, x1, y1, x1 + player_size, y1+player_size)
        canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)


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
window.mainloop()
