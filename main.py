from tkinter import *
from pickle import load, dump

# область функций
def set_status():
    pass

def pause_toggle():
    global pause
    pause = not pause
    if pause:
        set_status('Пауза')
    else:
        set_status('Вперед!')


def menu_toggle():
    pass


def key_handler(event):
    if game_over:
        return
    if event.keycode == KEY_PAUSE:
        pause_toggle()
    if pause:
        return

    set_status()

    if event.keycode == KEY_UP:
        canvas.move(player1 , SPEED, 0)

def check_finish():
    global game_over
    


def menu_enter():
    if menu_current_index == 0:
        game_resume()
    elif menu_current_index == 1:
        game_new()
    elif menu_current_index == 2:
        game_save()
    elif menu_current_index == 3:
        game_load()
    elif menu_current_index == 4:
        game_exit()
    menu_hide()



def game_new():
    print('Начинаем новую игру')


def game_resume():
    print('Возобновляем старую игру')


def game_save():
    print('Сохраняем игру')


def game_load():
    print('Загружаем игру')


def game_exit():
    print('Вычодим из игры')
    exit()


def menu_show():
    global menu_mode
    menu_mode = True
    menu_update()


def menu_hide():
    global menu_mode
    menu_mode = False
    menu_update()


def menu_up():
    global menu_current_index
    menu_current_index -= 1
    if menu_current_index < 0:
        menu_current_index = 0
    menu_update()


def menu_down():
    global menu_current_index
    menu_current_index += 1
    if menu_current_index > len(menu_options) - 1:
        menu_current_index = len(menu_options) - 1
    menu_update()



def menu_update():
    for menu_index in range(len(menu_options_id)):
        element_id = menu_options_id[menu_index]
        if menu_mode:
            canvas.itemconfig(element_id , state='normal')
            if menu_index == menu_current_index:
                canvas.itemconfig(element_id , fill='blue')
            else:
                canvas.itemconfig(element_id, fill='black')
        else:
            canvas.itemconfig(element_id, state='hidden')


def menu_create(canvas):
    offset = 0
    for menu_option in menu_options:
        option_id = canvas.create_text(400,200 + offset,
anchor=CENTER, font=('Arial','25'), text = menu_option,fill='black')
        menu_options_id.append(option_id)
        offset +=50
    menu_update()


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
