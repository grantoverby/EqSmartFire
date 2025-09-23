import keyboard
import pydirectinput
import sys
import time
import win32api
import win32event
import win32gui


# Prevent Multiple Instances

mutex = win32event.CreateMutex(None, False, "Global\\EqSmartFire")
if win32api.GetLastError() == 183:
    print('''
Another instance of EqSmartFire is running.
This instance will exit.''')
    time.sleep(5)
    sys.exit(1)


# Constants

HOTKEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
DELAYS = {
    '1': 0.5,
    '2': 0.75,
    '3': 1,
    '4': 2,
    '5': 10,
    '6': 60,
}
DEFAULT_DELAY = '1'


# Variables

keys = []
typing = False
paused = False
delay = DELAYS.get(DEFAULT_DELAY)
last_loop_epoch_ms = 0


# Print Help

print('''
https://github.com/grantoverby/EqSmartFire

CTRL + hotkey        : Toggle firing for corresponding hotkey
CTRL + [             : Pause firing
CTRL + ]             : Resume firing
/                    : Enter typing mode
r                    : Enter typing mode
ENTER                : Exit typing mode
CTRL + /             : Exit typing mode
CTRL + SHIFT + delay : Sets delay between key presses
CTRL + `             : Reset all settings

Firing hotkeys is suppressed if paused, typing, a modifier key is held, or if EverQuest is not the foreground window.
If multiple hotkeys are enabled, they will be fired in the order they were enabled.
Input is ignored if EverQuest is not the foreground window.''')

hotkeys_descriptions = ''
for key in HOTKEYS:
    hotkeys_descriptions += f'{key} '
hotkeys_descriptions = hotkeys_descriptions[:-1]
print(f'Available hotkeys: {hotkeys_descriptions}')

delay_descriptions = ''
for key, val in DELAYS.items():
    delay_descriptions += f'{key} = {val}s, '
delay_descriptions = delay_descriptions[:-2]
print(f'Available delays: {delay_descriptions}')
print(f'Default delay: {DEFAULT_DELAY} = {DELAYS.get(DEFAULT_DELAY)}s')

print('\n')


# Utility Functions

def is_everquest_foreground():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'EverQuest'


# Toggle Hotkeys

def toggle_key(val):
    global keys
    if is_everquest_foreground():
        if val in keys:
            keys.remove(val)
        else:
            keys.append(val)
        print(f'Keys: {keys}')

for key in HOTKEYS:
    keyboard.add_hotkey('ctrl+' + key, toggle_key, args=(key,))


# Delay

def set_delay(val):
    global delay
    global DELAYS
    if is_everquest_foreground():
        delay = DELAYS.get(val)
        print(f'Delay: {delay}s')

for key in DELAYS:
    keyboard.add_hotkey('ctrl+shift+' + key, set_delay, args=(key,))


# Typing

def set_typing(val):
    global typing
    if is_everquest_foreground():
        typing = val
        print(f'Typing: {typing}')

keyboard.add_hotkey('/', set_typing, args=(True, ))
keyboard.add_hotkey('r', set_typing, args=(True, ))
keyboard.add_hotkey('ctrl+/', set_typing, args=(False, ))
keyboard.add_hotkey('enter', set_typing, args=(False, ))


# Pause

def set_paused(val):
    global paused
    if is_everquest_foreground():
        paused = val
        print(f'Paused: {paused}')

keyboard.add_hotkey('ctrl+[', set_paused, args=(True, ))
keyboard.add_hotkey('ctrl+]', set_paused, args=(False, ))


# Reset

def reset():
    global keys
    global typing
    global paused
    global delay
    global DELAYS
    global DEFAULT_DELAY
    if is_everquest_foreground():
        keys.clear()
        typing = False
        paused = False
        delay = DELAYS.get(DEFAULT_DELAY)
        print('Reset')

keyboard.add_hotkey('ctrl+`', reset)


# Core Loop

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

def sleep():
    global delay
    global last_loop_epoch_ms
    current_time_ms = time.time_ns() // 1_000_000
    sleep_time_ms = last_loop_epoch_ms + (delay * 1_000) - current_time_ms
    if sleep_time_ms > 0:
        time.sleep(sleep_time_ms / 1_000)
    last_loop_epoch_ms = time.time_ns() // 1_000_000

try:
    while True:
        sleep()
        keys_copy = keys[:]
        for key in keys_copy:
            if is_active() and key in keys:
                pydirectinput.press(key)
                time.sleep(0.1)
except KeyboardInterrupt:
    pass

print('Exit')
