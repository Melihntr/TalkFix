import keyboard


def register_hotkey(hotkey_str, callback):
    keyboard.add_hotkey(hotkey_str, callback)
