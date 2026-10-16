#!/usr/bin/env python3
"""LegacyBluke USB host bridge. Standard library only; Windows 10/11."""
import ctypes
import json
import socket
import sys
from ctypes import wintypes

HOST, PORT = "127.0.0.1", 27183
INPUT_MOUSE, INPUT_KEYBOARD = 0, 1
MOVE, LEFTDOWN, LEFTUP, RIGHTDOWN, RIGHTUP = 0x0001, 0x0002, 0x0004, 0x0008, 0x0010
MIDDLEDOWN, MIDDLEUP, WHEEL, KEYUP = 0x0020, 0x0040, 0x0800, 0x0002
ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT)]
class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD), ("u", INPUT_UNION)]

user32 = ctypes.WinDLL("user32", use_last_error=True)
user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
user32.SendInput.restype = wintypes.UINT
BUTTONS = {"left_down": LEFTDOWN, "left_up": LEFTUP, "right_down": RIGHTDOWN,
           "right_up": RIGHTUP, "middle_down": MIDDLEDOWN, "middle_up": MIDDLEUP}

def emit(item):
    if user32.SendInput(1, ctypes.byref(item), ctypes.sizeof(INPUT)) != 1:
        raise ctypes.WinError(ctypes.get_last_error())

def mouse(dx=0, dy=0, flags=0, data=0):
    emit(INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(int(dx), int(dy), int(data), flags, 0, 0)))

def handle(m):
    kind = m.get("type")
    if kind == "mouse_move":
        mouse(m.get("dx", 0), m.get("dy", 0), MOVE)
    elif kind == "mouse_button":
        name = str(m.get("button")) + "_" + str(m.get("action"))
        if name not in BUTTONS: raise ValueError("unknown mouse button/action")
        mouse(flags=BUTTONS[name])
    elif kind == "mouse_wheel":
        mouse(flags=WHEEL, data=int(m.get("delta", 0)))
    elif kind == "key":
        flags = 0 if bool(m.get("down")) else KEYUP
        emit(INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(int(m["vk"]), 0, flags, 0, 0)))
    elif kind == "gamepad":
        raise ValueError("gamepad is not implemented yet; Windows needs a virtual-controller backend")
    else:
        raise ValueError("unknown event type")

def main():
    if sys.platform != "win32":
        print("Windows only.", file=sys.stderr)
        return 2
    print("LegacyBluke USB receiver listening on 127.0.0.1:27183")
    print("Keep this window open. Only local ADB-reverse connections are accepted.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        while True:
            conn, address = server.accept()
            print("Bridge connected:", address[0])
            with conn:
                stream = conn.makefile("r", encoding="utf-8", newline="\n")
                for line in stream:
                    try:
                        if len(line) > 8192: raise ValueError("message too large")
                        handle(json.loads(line))
                        reply = {"ok": True}
                    except Exception as exc:
                        reply = {"ok": False, "error": str(exc)}
                    conn.sendall((json.dumps(reply) + "\n").encode("utf-8"))
            print("Bridge disconnected.")

if __name__ == "__main__":
    raise SystemExit(main())
