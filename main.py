from tkinter import *
from pickle import load, dump

# Область функций
def set_status(text, color='black'):
    canvas.itemconfig(text_id, text=text, fill=color)

def pause_toggle():
    global pause
    pause = not pause
    set_status('Пауза' if pause else 'Вперед!')

def menu_toggle():
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        menu_show()
    else:
        menu_hide()

def key_handler(event):
    global x1, x2, game_over, pause
    if menu_mode:
        if event.keycode == KEY_UP:
            menu_up()
        elif event.keycode == KEY_DOWN:
            menu_down()
        elif event.keycode == KEY_ENTER:
            menu_enter()
    else:
        if not game_over and not pause:
            if event.keycode == KEY_PLAYER1:  # Игрок 1 (стрелка вправо)
                x1 += SPEED
                canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
            elif event.keycode == KEY_PLAYER2:  # Игрок 2 (клавиша D)
                x2 += SPEED
                canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
            check_finish()

        if event.keycode == KEY_ESC:
            menu_toggle()
        elif event.keycode == KEY_PAUSE:
            pause_toggle()

def check_finish():
    global game_over
    if x1 >= x_finish:
        game_over = True
        set_status("Игрок 1 победил!", 'red')
    elif x2 >= x_finish:
        game_over = True
        set_status("Игрок 2 победил!", 'blue')

def menu_enter():
    if menu_current_index == 0:  # Вернуться в игру
        game_resume()
    elif menu_current_index == 1:  # Новая игра
        game_new()
    elif menu_current_index == 2:  # Сохранить
        game_save()
    elif menu_current_index == 3:  # Загрузить
        game_load()
    elif menu_current_index == 4:  # Выход
        game_exit()

def game_new():
    global x1, x2, game_over, pause
    x1, y1 = 50, 50
    x2, y2 = 50, 200
    game_over = False
    pause = False
    canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
    canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
    set_status('Вперед!')

def game_resume():
    global pause, menu_mode
    pause = False
    menu_mode = False
    set_status('Вперед!')

def game_save():
    with open('save.dat', 'wb') as f:
        dump((x1, y1, x2, y2, game_over), f)
    set_status('Игра сохранена!')

def game_load():
    global x1, y1, x2, y2, game_over
    try:
        with open('save.dat', 'rb') as f:
            x1, y1, x2, y2, game_over = load(f)
        canvas.coords(player1, x1, y1, x1 + player_size, y1 + player_size)
        canvas.coords(player2, x2, y2, x2 + player_size, y2 + player_size)
        set_status('Игра загружена!')
    except FileNotFoundError:
        set_status('Сохранение не найдено!')

def game_exit():
    window.quit()

def menu_show():
    for option_id in menu_options_id:
        canvas.itemconfig(option_id, state='normal')

def menu_hide():
    for option_id in menu_options_id:
        canvas.itemconfig(option_id, state='hidden')

def menu_up():
    global menu_current_index
    if menu_current_index > 0:
        menu_current_index -= 1
    menu_update()

def menu_down():
    global menu_current_index
    if menu_current_index < len(menu_options) - 1:
        menu_current_index += 1
    menu_update()

def menu_update():
    for i, option_id in enumerate(menu_options_id):
        color = 'black' if i == menu_current_index else 'gray'
        canvas.itemconfig(option_id, fill=color)

def menu_create(canvas):
    global menu_options_id, option_id
    for i, option in enumerate(menu_options):
        option_id = canvas.create_text(game_width // 2, 100 + 30 * i, text=option, font=('Arial', 20), fill='black')
        canvas.itemconfig(option_id, state='hidden')
        menu_options_id.append(option_id)

# Область переменных
game_width = 800
game_height = 800
menu_mode = False
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

SPEED = 12

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