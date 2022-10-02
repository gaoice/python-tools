import ctypes
import atexit
from ctypes import byref
from ctypes import wintypes
from ctypes import CFUNCTYPE, POINTER, c_int, c_void_p, c_uint

# python3

cfunctype = CFUNCTYPE(c_int, c_int, wintypes.HINSTANCE, POINTER(c_void_p))
GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
SetWindowsHookExA = ctypes.windll.user32.SetWindowsHookExA
CallNextHookEx = ctypes.windll.user32.CallNextHookEx
UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx
GetMessageW = ctypes.windll.user32.GetMessageW
TranslateMessage = ctypes.windll.user32.TranslateMessage
DispatchMessageW = ctypes.windll.user32.DispatchMessageW

GetModuleHandleA.restype = wintypes.HMODULE
GetModuleHandleA.argtypes = [wintypes.LPCWSTR]
SetWindowsHookExA.restype = c_int
SetWindowsHookExA.argtypes = [c_int, cfunctype, wintypes.HINSTANCE, wintypes.DWORD]
GetMessageW.argtypes = [POINTER(wintypes.MSG), wintypes.HWND, c_uint, c_uint]
TranslateMessage.argtypes = [POINTER(wintypes.MSG)]
DispatchMessageW.argtypes = [POINTER(wintypes.MSG)]


class HookHelper:
    def __init__(self):
        self.keyboard_hhook = None
        self.mouse_hhook = None

    def keyboard_proc(self, helper_self, n_code, w_param, l_param):
        pass

    def mouse_proc(self, helper_self, n_code, w_param, l_param):
        pass

    def msg_handler(self):
        msg = wintypes.MSG()
        while True:
            code = GetMessageW(byref(msg), 0, 0, 0)
            if code in [0, -1]:
                UnhookWindowsHookEx(self.keyboard_hhook)
                UnhookWindowsHookEx(self.mouse_hhook)
                break
            else:
                TranslateMessage(byref(msg))
                DispatchMessageW(byref(msg))

    def hook_keyboard(self):
        def keyboard_proc_proxy(n_code, w_param, l_param):
            try:
                self.keyboard_proc(self, n_code, w_param, l_param)
            finally:
                return CallNextHookEx(self.keyboard_hhook, n_code, w_param, l_param)

        fun = cfunctype(keyboard_proc_proxy)
        self.keyboard_hhook = SetWindowsHookExA(13, fun, GetModuleHandleA(None), 0)
        atexit.register(UnhookWindowsHookEx, self.keyboard_hhook)
        self.msg_handler()

    def hook_mouse(self):
        def mouse_proc_proxy(n_code, w_param, l_param):
            try:
                self.mouse_proc(self, n_code, w_param, l_param)
            finally:
                return CallNextHookEx(self.mouse_hhook, n_code, w_param, l_param)

        fun = cfunctype(mouse_proc_proxy)
        self.mouse_hhook = SetWindowsHookExA(14, fun, GetModuleHandleA(None), 0)
        atexit.register(UnhookWindowsHookEx, self.mouse_hhook)
        self.msg_handler()

    @staticmethod
    def exit():
        ctypes.windll.user32.PostQuitMessage(0)
