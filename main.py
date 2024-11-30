from tkinter import*

def menu_up():
    global menu_current_index
    menu_current_index -= 1
    if menu_current_index < 0:
        menu_current_index =  0
    menu_update()

def menu_down():
    global menu_current_index
    menu_current_index += 1
    if menu_current_index > len(menu_options) -1:
        menu_current_index = len(menu_options) - 1
    menu_update()

def menu_create(canvas):
    offest = 0
    for menu_option in menu_options:
        option_id = canvas.create_text(400, 200 + offset,
                                       anchor=CENTER, font = ('Arial', '25'),
                                       text=menu_option)
        menu_options_id.append(option_id)
        offest += 50
    menu_update()

def menu_hide():
    global menu_mode
    menu_mode = False
    menu_update()

def menu_show():
    global menu_mode
    menu_mode = True
    menu_update()

def menu_update():
    for menu_index in range(len(menu_options_id)):
        element_id = menu_options_id[menu_index]
        if menu_mode:
            canvas.itemconfig(element_id, state = 'normal')
            if menu_mode:
                canvas.itemconfig(element_id, state = 'normal')
                if menu_index == menu_current_index:
                    canvas.itemconfig(element_id, fill = 'blue')
                else:
                    canvas.itemconfig(element_id, fill = 'black')
        else:
            canvas.itemconfig(element_id, state = 'hidden')
def pause_toggle():
    global pause
    pause = not pause
    if pause:
        set_status("Пауза")
    else:
        set_status('Вперёд')

def save_game(event):
    x1 = canvas.coords(player1_id) [0]
    x2 = canvas.coords(player2_id)[0]
    data = [x1, x2]
    with open('save.dat', 'wb') as f:
        dump(data, f)
        set_status("Сохранено")

def load_game(event):
    global x1 , x2
    with open('save.dat', 'rb') as f:
        data = load(f)
        x1, x2 = data
        canvas.coords(player1_id, x1, y1, x1 + player_size, y1 + player_size)
        canvas.coords(player2_id, x2, y2, x2 + player_size, y2 + player_size)
        set_status("Загружено")

def key_handler(event):
    if game_over:
        return
    if event.keycode == KEY_PAUSE:
        pause_toggle()
    if pause:
        return

    set_status("Вперёд")

    if event.keycode == KEY_FORWARD1:
        canvas.move(player1_id, SPEED, 0)
    elif event.keycode == KEY_FORWARD2:
        canvas.move(player2_id, SPEED, 0)

    check_finish()

def set_status(status_text, color = 'BLACK'):
    canvas.itemconfig(text_status_id, text=status_text, fill=color)

def check_finish():
    global game_over
    coords_player1 = canvas.coords(player1_id)
    coords_player2 = canvas.coords(player2_id)
    coords_finish = canvas.coords(finish_id)

    x1_right = coords_player1[2]
    x2_right = coords_player2[2]
    x_finish = coords_finish[0]

    if x1_right >= x_finish:
        set_status('Победа верхнего игрока', player1_color)
        game_over = True
    if x2_right >= x_finish:
        set_status('Победа нижнего игрока', player2_color)
        game_over = True


KEY_FORWARD1 = 39
KEY_FORWARD2 = 68
KEY_PAUSE = 19

game_width = 800
game_height = 500

game_over = False
pause = False

player_size = 100
SPEED = 12
x1, y1 = 50, 50
x2, y2 = x1, y1 + player_size + 100
player1_color = 'red'
player2_color = 'blue'
x_finish = game_width - 50

window = Tk()
window.title('DMEC')

canvas = Canvas(window, width=game_width, height=game_height, bg='white')
canvas.pack()
player1_id = canvas.create_rectangle(x1,
                                   y1,
                                   x1 + player_size,
                                   y1 + player_size,
                                   fill=player1_color)
player2_id = canvas.create_rectangle(x2,
                                  y2,
                                  x2 + player_size,
                                  y2 + player_size,
                                  fill=player2_color)
finish_id = canvas.create_rectangle(x_finish,
                                    0,
                                    x_finish + 10,
                                    game_height,
                                    fill='black')

text_status_id = canvas.create_text(x1,
                             game_height - 50,
                             anchor=SW,
                             font=('Arial', '25'),
                             text='Вперед!')


# Функции обратного вызова
canvas.pack()
window.bind('<KeyRelease>', key_handler)
window.bind('<Control-Key-s>', save_game)
window.bind('<Control-Key-0>', load_game)
window.mainloop()
