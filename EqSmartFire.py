import time
import pydirectinput
import win32gui
import keyboard


print('''
CTRL + ALT + hotkey        : Toggle spam for corresponding hotkey
CTRL + ALT + [             : Pause spamming
CTRL + ALT + ]             : Resume spamming
/                          : Enter typing mode
r                          : Enter typing mode
ENTER                      : Exit typing mode
CTRL + ALT + /             : Exit typing mode
CTRL + ALT + SHIFT + delay : Sets delay between key presses
CTRL + ALT + `             : Reset all settings

Spamming is suppressed if paused, typing, a modifier key is held, or if EverQuest is not the foreground window.
Multiple hotkeys can be toggled simultaneously.
Available hotkeys: 1 2 3 4 5 6 7 8 9 0 - =''')


DEFAULT_DELAY = '2'
DELAYS = {
    '1': 0.25,
    '2': 0.5,
    '3': 0.75,
    '4': 1,
    '5': 2,
    '6': 10,
    '7': 60,
}


keys = []
typing = False
paused = False
delay = DELAYS.get(DEFAULT_DELAY)


delay_descriptions = ''
for key, val in DELAYS.items():
    delay_descriptions += f'{key}: {val}s, '
delay_descriptions = delay_descriptions[:-2]
print(f'Available delays: {delay_descriptions}')
print(f'Default delay: {DEFAULT_DELAY}: {DELAYS.get(DEFAULT_DELAY)}s')


def set_delay(val):
    global delay
    global DELAYS
    delay = DELAYS.get(val)

for key in DELAYS:
    keyboard.add_hotkey('ctrl+alt+shift+' + key, set_delay, args=(key,))


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
    global DEFAULT_DELAY
    keys.clear()
    typing = False
    paused = False
    set_delay(DEFAULT_DELAY)

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
        time.sleep(delay)
        for key in keys:
            if is_active():
                pydirectinput.press(key)
                time.sleep(delay / 10)
except KeyboardInterrupt:
    pass
