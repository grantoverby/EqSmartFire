import time
import pydirectinput
import win32gui
import keyboard


print('''
https://github.com/grantoverby/EqSmartFire

CTRL + hotkey        : Toggle spam for corresponding hotkey
CTRL + [             : Pause spamming
CTRL + ]             : Resume spamming
/                    : Enter typing mode
r                    : Enter typing mode
ENTER                : Exit typing mode
CTRL + /             : Exit typing mode
CTRL + SHIFT + delay : Sets delay between key presses
CTRL + `             : Reset all settings

Spamming is suppressed if paused, typing, a modifier key is held, or if EverQuest is not the foreground window.
If multiple hotkeys are enabled, they will be spammed in the order they were enabled.
Input is ignored if EverQuest is not the foreground window.
Available hotkeys: 1 2 3 4 5 6 7 8 9 0 - =''')


DEFAULT_DELAY = '1'
DELAYS = {
    '1': 0.5,
    '2': 0.75,
    '3': 1,
    '4': 2,
    '5': 10,
    '6': 60,
}


keys = []
typing = False
paused = False
delay = DELAYS.get(DEFAULT_DELAY)


delay_descriptions = ''
for key, val in DELAYS.items():
    delay_descriptions += f'{key} = {val}s, '
delay_descriptions = delay_descriptions[:-2]
print(f'Available delays: {delay_descriptions}')
print(f'Default delay: {DEFAULT_DELAY} = {DELAYS.get(DEFAULT_DELAY)}s')


def is_everquest_foreground():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'EverQuest'


def set_delay(val):
    global delay
    global DELAYS
    if is_everquest_foreground():
        delay = DELAYS.get(val)

for key in DELAYS:
    keyboard.add_hotkey('ctrl+shift+' + key, set_delay, args=(key,))


def toggle_key(val):
    global keys
    if is_everquest_foreground():
        if val in keys:
            keys.remove(val)
        else:
            keys.append(val)

for key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']:
    keyboard.add_hotkey('ctrl+' + key, toggle_key, args=(key,))


def set_typing(val):
    global typing
    if is_everquest_foreground():
        typing = val

keyboard.add_hotkey('/', set_typing, args=(True, ))
keyboard.add_hotkey('r', set_typing, args=(True, ))
keyboard.add_hotkey('ctrl+/', set_typing, args=(False, ))
keyboard.add_hotkey('enter', set_typing, args=(False, ))


def set_paused(val):
    global paused
    if is_everquest_foreground():
        paused = val

keyboard.add_hotkey('ctrl+[', set_paused, args=(True, ))
keyboard.add_hotkey('ctrl+]', set_paused, args=(False, ))


def reset():
    global keys
    global typing
    global paused
    global DEFAULT_DELAY
    if is_everquest_foreground():
        keys.clear()
        typing = False
        paused = False
        set_delay(DEFAULT_DELAY)

keyboard.add_hotkey('ctrl+`', reset)


def is_active():
    global typing
    global paused
    return (
            is_everquest_foreground()
            and not typing
            and not paused
            and not keyboard.is_pressed('ctrl')
            and not keyboard.is_pressed('alt')
            and not keyboard.is_pressed('shift')
            and not keyboard.is_pressed('windows')
    )


def sleep(last_time_ms):
    global delay
    current_time_ms = time.time_ns() // 1_000_000
    sleep_time_ms = last_time_ms + (delay * 1000) - current_time_ms
    if sleep_time_ms > 0:
        time.sleep(sleep_time_ms / 1000)
    return time.time_ns() // 1_000_000


try:
    last_loop = 0
    while True:
        last_loop = sleep(last_loop)
        keys_copy = keys[:]
        for key in keys_copy:
            if is_active() and key in keys:
                pydirectinput.press(key)
                time.sleep(0.1)
except KeyboardInterrupt:
    pass
