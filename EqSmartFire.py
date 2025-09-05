import time
import pydirectinput
import win32gui
import keyboard


PRESS_DELAY = 100 # milliseconds
LOOP_DELAY = 1000 # milliseconds


keys = []
typing = False
paused = False


def toggle_key(val):
    global keys
    if val in keys:
        keys.remove(val)
    else:
        keys.append(val)

for key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']:
    keyboard.add_hotkey('ctrl+alt+' + key, toggle_key, args=(key,))


def set_typing(val):
    global typing
    typing = val

keyboard.add_hotkey('/', set_typing, args=(True, ))
keyboard.add_hotkey('r', set_typing, args=(True, ))
keyboard.add_hotkey('ctrl+alt+/', set_typing, args=(False, ))
keyboard.add_hotkey('enter', set_typing, args=(False, ))


def set_paused(val):
    global paused
    paused = val

keyboard.add_hotkey('ctrl+alt+[', set_paused, args=(True, ))
keyboard.add_hotkey('ctrl+alt+]', set_paused, args=(False, ))


def reset():
    global keys
    global typing
    global paused
    keys.clear()
    typing = False
    paused = False

keyboard.add_hotkey('ctrl+alt+`', reset)


def is_active():
    global typing
    global paused
    return (
            win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'EverQuest'
            and not typing
            and not paused
            and not keyboard.is_pressed('ctrl')
            and not keyboard.is_pressed('alt')
            and not keyboard.is_pressed('shift')
            and not keyboard.is_pressed('windows')
    )


try:
    while True:
        time.sleep(LOOP_DELAY / 1000)
        for key in keys:
            if is_active():
                pydirectinput.press(key)
                time.sleep(PRESS_DELAY / 1000)
except KeyboardInterrupt:
    pass
