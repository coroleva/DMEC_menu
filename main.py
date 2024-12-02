from tkinter import *
from pickle import load, dump

# область функций
def set_status(status_text, color = 'black'):
    canvas.itemconfig(text_id, text = status_text, fill = color)

def pause_toggle():
    global pause
    pause = not pause
    if pause:
        set_status('Время пить чай!')
    else:
        set_status('Вперёд!')


def menu_toggle():
    pass


def key_handler(event):
    if game_over:
        return

    if event.keycode == KEY_PAUSE:
        pause_toggle()

    if pause:
        return

    set_status('Вперёд!')

    if event.keycode == KEY_PLAYER1:
        canvas.move(player1, SPEED, 0)

    elif event.keycode == KEY_PLAYER2:
        canvas.move(player2, SPEED, 0)

    check_finish()

def check_finish():
    global game_over

    coords_player1 = canvas.coords(player1)
    coords_player2 = canvas.coords(player2)
    coords_finish = canvas.coords(finish_id)

    x1_right = coords_player1[2]
    x2_right = coords_player2[2]
    x_finish = coords_finish[0]

    if x1_right >= x_finish:
        set_status('Победил красный игрок!', player1_color)
        print('Победил красный игрок!')
        game_over = True

    if x2_right >= x_finish:
        set_status('Победил синий игрок!', player2_color)
        print('Победил синий игрок!')
        game_over = True


def menu_enter():
    pass


def game_new():
    pass


def game_resume():
    pass


def game_save(event):
    x1 = canvas.coords(player1)[0]
    x2 = canvas.coords(player2)[0]
    data = [x1, x2]
    with open('save.dat', 'wb') as f:
        dump(data, f)
        set_status('Сохранено')


def game_load(event):
    global x1, x2
    with open('save.dat', 'rb') as f:
        data = load(f)
        x1, x2 = data
        canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
        canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
        set_status('Загружено')


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
KEY_PAUSE = 32

SPEED = 50

game_over = False
pause = False

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
