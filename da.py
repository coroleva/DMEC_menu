from tkinter import *
from pickle import load, dump

from main import finish_id


# область функций
def set_status(text):
    canvas.itemconfig(text_id, text=text)

def pause_toggle():
    global pause
    pause = not pause
    set_status("Paused" if pause else "Game in Progress")

def menu_toggle():
    global menu_mode
    menu_mode = not menu_mode
    menu_show() if menu_mode else menu_hide()

def key_handler(event):
    global pause
    if event.keycode == KEY_ESC:
        menu_toggle()
    elif event.keycode == KEY_PAUSE:
        pause_toggle()
    elif not pause:
        if event.keycode == KEY_PLAYER1:
            move_player(player1, SPEED, 0)
        elif event.keycode == KEY_PLAYER2:
            move_player(player2, SPEED, 0)

def move_player(player, dx, dy):
    canvas.move(player, dx, dy)
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
        set_status('Победил красный игрок!')
        game_over = True
    if x2_right >= x_finish:
        set_status('Победил синий игрок!')
        game_over = True

def menu_enter():
    global menu_current_index
    if menu_current_index == 1:
        game_new()
    elif menu_current_index == 2:
        game_save()
    elif menu_current_index == 3:
        game_load()
    elif menu_current_index == 4:
        game_exit()

def game_new():
    canvas.delete("all")
    start_game()

def game_resume():
    pass

def game_save():
    with open('game_save.dat', 'wb') as f:
        dump((canvas.coords(player1), canvas.coords(player2)), f)
    set_status("Game Saved!")

def game_load():
    global player1, player2
    try:
        with open('game_save.dat', 'rb') as f:
            player_positions = load(f)
            canvas.coords(player1, *player_positions[0])
            canvas.coords(player2, *player_positions[1])
        set_status("Game Loaded!")
    except FileNotFoundError:
        set_status("No save file found!")

def game_exit():
    window.quit()

def menu_show():
    canvas.create_rectangle(100, 100, 700, 700, fill="grey", outline="black")
    for i, option in enumerate(menu_options):
        color = "black" if i == menu_current_index else "white"
        canvas.create_text(400, 150 + i * 50, text=option, fill=color, font=('Arial', '20'))

def menu_hide():
    canvas.delete("all")
    start_game()

def menu_up():
    global menu_current_index
    menu_current_index = (menu_current_index - 1) % len(menu_options)
    menu_update()

def menu_down():
    global menu_current_index
    menu_current_index = (menu_current_index + 1) % len(menu_options)
    menu_update()

def menu_update():
    menu_hide()
    menu_show()

def menu_create(canvas):
    pass

def start_game():
    global player1, player2
    player1 = canvas.create_rectangle(x1, y1, x1 + player_size, y1 + player_size, fill=player1_color)
    player2 = canvas.create_rectangle(x2, y2, x2 + player_size, y2 + player_size, fill=player2_color)
    canvas.create_rectangle(x_finish, 0, x_finish + 10, game_height, fill='black')
    set_status("Вперед!")

# область переменных
game_width = 800
game_height = 800
menu_mode = True
menu_options = ['Возврат в игру', 'Новая игра', 'Сохранить', 'Загрузить', 'Выход']
menu_current_index = 0
menu_options_id = []

KEY_UP = 87  # W
KEY_DOWN = 83  # S
KEY_ESC = 27  # Esc
KEY_ENTER = 13  # Enter
player_size = 100
x1, y1 = 50, 50
x2, y2 = x1, y1 + player_size + 100
player1_color = 'red'
player2_color = 'blue'
x_finish = game_width - 50
KEY_PLAYER1 = 39  # Right Arrow
KEY_PLAYER2 = 68  # D
KEY_PAUSE = 19  # Pause
SPEED = 12
game_over = False
pause = False

# Окно и объекты
window = Tk()
window.title('DMEC')

canvas = Canvas(window, width=game_width, height=game_height, bg='white')
canvas.pack()
menu_create(canvas)
text_id = canvas.create_text(x1, game_height - 50, anchor=SW, font=('Arial', '25'), text='Вперед!')
finish_id =()
start_game()

# Функции обратного вызова
window.bind('<KeyRelease>', key_handler)
window.bind('<KeyPress>', key_handler)
window.mainloop()
