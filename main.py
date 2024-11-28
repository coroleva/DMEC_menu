import tkinter as tk
from time import sleep


#Размеры игрового поля
game_width = 800
game_height = 800

# Инициализация главного окна
root = tk.Tk()
root.title('Rase to the finish')
canvas = tk.Canvas(root, width=game_width, height=game_height)
canvas.pack()

# переменные для игроков
player_size = 100
x1, y1 = 20, game_height // 2 - player_size // 2
x2, y2 = 20, game_height // 2 + player_size * 2
player1_color = 'red'
player2_color = 'blue'

# финишная прямая
x_finish = game_width - 50

# Скорость перемещения игроков
SPEED = 12

# Состояние игры
game_over = False
pause = False
menu_mode = True

# Меню
menu_options = ["Возврат в игру", "Новая игра", "Сохранить", "Загрузить", "Выход"]
menu_current_index = 0
menu_options_id = []

def set_status(text, color='white'):
    canvas.create_text(10, 10, text=text, fill=color, anchor='nw', font=('Arial', 16))

def pause_toggle():
    global pause
    if not game_over:
        pause = not pause
        if pause:
            set_status("Пауза", '#C8C8C8')
        else:
            set_status('', '#000000')


def menu_toggle():
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        menu_show()
    else:
        menu_hide()


def key_handler(event):
    global menu_current_index, menu_mode, pause, game_over
#Управление в меню
    if menu_mode:
        if event.keysym == 'w':
            menu_up()
        elif event.keysym == 's':
            menu_down()
        elif event.keysym == 'Return':
            menu_enter()
# Игровые события
    else:
        if event.keysym == 'Escape':
            menu_toggle()
        elif event.keysym == 'space':
            pause_toggle()
        elif event.keysym == 'Right':
            move_player1()
        elif event.keysym == 'd':
            move_player2()

def check_finish():
    global game_over
    if x1 >= x_finish or x2 >= x_finish:
        game_over = True
        winner = "Player 1" if x1 > x2 else "Player 2"
        set_status(f"{winner} won!", '#00FF00')


def menu_enter():
    global menu_mode, game_over, x1, y1, x2, y2
    if menu_options[menu_current_index] == "Возврат в игру":
        menu_mode = False
    elif menu_options[menu_current_index] == "Новая игра":
        game_new()
    elif menu_options[menu_current_index] == "Сохранить":
        game_save()
    elif menu_options[menu_current_index] == "Загрузить":
        game_load()
    elif menu_options[menu_current_index] == "Выход":
        game_exit()


def game_new():
    global x1, y1, x2, y2, game_over
    x1, y1 = 20, game_height // 2 - player_size // 2
    x2, y2 = 20, game_height // 2 + player_size * 2
    game_over = False
    set_status('')
    menu_mode = False


def game_resume():
    global menu_mode
    menu_mode = False


def game_save():
    with open('save.dat', 'w') as f:
        f.write(f'{x1},{y1}\n')
        f.write(f'{x2},{y2}')


def game_load():
    try:
        with open('save.dat', 'r') as f:
            lines = f.readlines()
            x1, y1 = map(int, lines[0].strip().split(','))
            x2, y2 = map(int, lines[1].strip().split(','))
    except FileNotFoundError:
        print("Файл сохранения не найден.")


def game_exit():
    root.destroy()


def menu_show():
    for i in range(len(menu_options)):
        option_text = menu_options[i]
        text = option_text if i != menu_current_index else "> " + option_text
        text_pos = (300, 150 + i * 40)
        text_surface = canvas.create_text(text_pos, text=text, fill='white', font=('Arial', 14))
        menu_options_id.append(text_surface)


def menu_hide():
    for id in menu_options_id:
        canvas.delete(id)
    menu_options_id.clear()


def menu_up():
    global menu_current_index
    menu_current_index -= 1
    if menu_current_index < 0:
        menu_current_index = len(menu_options) - 1
    menu_update()


def menu_down():
    global menu_current_index


def menu_update():
    pass


def menu_create(canvas):
    pass


# область переменных



KEY_UP = 87
KEY_DOWN = 83
KEY_ESC = 27
KEY_ENTER = 13



KEY_PLAYER1 = 39
KEY_PLAYER2 = 68
KEY_PAUSE = 19






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
