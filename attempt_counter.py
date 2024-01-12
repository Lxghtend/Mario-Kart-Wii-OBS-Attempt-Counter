import pyautogui
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
import time
import tkinter as tk

text_var = 0

def pixel_grab(x,y):
    # Get the pixel color at the specified coordinates
    screen = ImageGrab.grab()
    pixel_color = screen.getpixel((x, y))
    return pixel_color

def checker():

    restart = pyautogui.locateCenterOnScreen("restart.png", confidence=0.7)

    start_time = time.time()

    if restart is not None:
        print(restart)

        x_coord, y_coord = restart

        while True:
            if restart is not None:

                current_time = time.time()

                pixel_color = pixel_grab(x_coord, y_coord)

                print(pixel_color)

                # Checks if screen turns black to confirm the user pressed restart and isnt just pausing
                if pixel_color == (0, 0, 0):
                    return True
                
                # Breaks the loop after 3 seconds of restart button being visible and assumes user is just pausing, which will then repeat the process
                if current_time - start_time >= 10:
                    break

                #restart = pyautogui.locateCenterOnScreen("restart.png", confidence=0.7)

                time.sleep(0.2)

            else:
                break

def update_text():

    global text_var
    result = checker()

    if result:
        text_var = text_var +1
        label.config(text=f"Total Attempts: {text_var}")
        with open('text.txt', 'w') as file:
            file.write(f"Total Attempts: {text_var}")

    root.after(100, update_text)

root = tk.Tk()
root.wm_attributes('-alpha', 0)

# Toplevel window for the text
top_level = tk.Toplevel(root)
top_level.wm_attributes('-alpha', 1)
top_level.overrideredirect(True)

font_size = 25
custom_font = ("Helvetica", font_size)

label = tk.Label(top_level, text="Total Attempts:", bg='white', font=custom_font)
label.pack()

title = root.title("Attempt Counter")


update_text()

root.mainloop()