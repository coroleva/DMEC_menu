import tkinter as tk
from tkinter import messagebox
from pickle import load, dump

#Нейросеть GIGACHAT

# Настройки игры
game_width = 800
game_height = 600
menu_mode = False
menu_options = ["Возврат в игру", "Новая игра", "Сохранить", "Загрузить", "Выход"]
menu_current_index = 0
menu_options_id = []
player_size = 60
x1, y1 = 20, game_height // 2 - player_size // 2
x2, y2 = 40, game_height // 2 - player_size // 2
player1_color = "#FF0000"
player2_color = "#0000FF"
x_finish = game_width - 50
SPEED = 6
game_over = False
pause = False

# Константы для клавиш
KEY_UP = "<Up>"
KEY_DOWN = "<Down>"
KEY_ESC = "<Escape>"
KEY_ENTER = "<Return>"
KEY_PLAYER1 = "<Right>"
KEY_PLAYER2 = "<KeyPress-d>"
KEY_PAUSE = "<space>"

root = tk.Tk()
root.title("Гонка до финиша")
root.geometry(f"{game_width}x{game_height}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=game_width, height=game_height, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

player1 = canvas.create_rectangle(x1, y1, x1+player_size, y1+player_size, fill=player1_color)
player2 = canvas.create_rectangle(x2, y2, x2+player_size, y2+player_size, fill=player2_color)

status_label = tk.Label(root, text="", fg="#FF00FF", font=("Helvetica", 16))
status_label.place(relx=0.05, rely=0.02, anchor="nw")

menu_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1)
menu_items = {}
for i, option in enumerate(menu_options):
    label = tk.Label(menu_frame, text=option, font=("Helvetica", 14))
    label.grid(row=i, column=0, pady=5)
    menu_items[option] = label

root.bind_all(KEY_UP, lambda e: menu_up())
root.bind_all(KEY_DOWN, lambda e: menu_down())
root.bind_all(KEY_ENTER, lambda e: menu_enter())
root.bind_all(KEY_ESC, lambda e: menu_toggle())
root.bind_all(KEY_PAUSE, lambda e: pause_toggle())
root.bind_all(KEY_PLAYER1, lambda e: move_player(1))
root.bind_all(KEY_PLAYER2, lambda e: move_player(2))

def set_status(text, color="#FF00FF"):
    status_label.config(text=text, fg=color)

def pause_toggle():
    global pause
    if not game_over:
        pause = not pause
        if pause:
            set_status("Пауза")
        else:
            set_status("")

def menu_toggle():
    global menu_mode
    menu_mode = not menu_mode
    if menu_mode:
        menu_show()
    else:
        menu_hide()

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

def menu_enter():
    global menu_mode, x1, y1, x2, y2, game_over, pause
    selected_option = menu_options[menu_current_index]
    if selected_option == "Возврат в игру":
        menu_mode = False
        menu_hide()
        game_resume()
    elif selected_option == "Новая игра":
        game_new()
    elif selected_option == "Сохранить":
        game_save()
    elif selected_option == "Загрузить":
        game_load()
    elif selected_option == "Выход":
        root.destroy()

def game_new():
    global x1, y1, x2, y2, game_over, pause
    x1, y1 = 20, game_height // 2 - player_size // 2
    x2, y2 = 40, game_height // 2 - player_size // 2
    game_over = False
    pause = False
    set_status("")
    canvas.coords(player1, x1, y1, x1+player_size, y1+player_size)
    canvas.coords(player2, x2, y2, x2+player_size, y2+player_size)

def game_resume():
    global menu_mode
    menu_mode = False
    pause = False
    set_status("")
    menu_hide()

def game_save():
    with open("save.dat", "wb") as file:
        dump(f"{x1},{y1}\n{x2},{y2}", file)

def game_load():
    global x1, y1, x2, y2
    try:
        with open("save.dat", "rb") as file:
            data = load(file).splitlines()
            x1, y1 = map(int, data[0].split(","))
            x2, y2 = map(int, data[1].split(","))
            canvas.coords(player1, x1, y1, x1+player_size, y1+player_size)
            canvas.coords(player2, x2, y2, x2+player_size, y2+player_size)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл сохранения не найден.")

def menu_show():
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")
    menu_update()

def menu_hide():
    menu_frame.place_forget()

def menu_update():
    for option, label in menu_items.items():
        if option == menu_options[menu_current_index]:
            label.config(bg="yellow")
        else:
            label.config(bg="SystemButtonFace")

def move_player(player_num):
    global x1, x2, y1, y2
    if not pause and not game_over:
        if player_num == 1:
            x1 += SPEED
            canvas.coords(player1, x1, y1, x1+player_size, y1+player_size)
        elif player_num == 2:
            x2 += SPEED
            canvas.coords(player2, x2, y2, x2+player_size, y2+player_size)

def check_finish():
    global game_over
    if x1 >= x_finish or x2 >= x_finish:
        game_over = True
        winner = "Первый" if x1 >= x_finish else "Второй"
        set_status(f"Победил {winner} игрок!", "green")

def game_loop():
    if not menu_mode and not pause and not game_over:
        check_finish()
    root.after(10, game_loop)

game_loop()
root.mainloop()