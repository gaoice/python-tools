import win32clipboard as cb
import win32con


# python3

class ClipboardHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_unicode_text():
        cb.OpenClipboard()
        try:
            cb_text = cb.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
            cb_text = None
        finally:
            cb.CloseClipboard()
        return cb_text

    @staticmethod
    def set_unicode_text(cb_text):
        cb.OpenClipboard()
        cb.EmptyClipboard()
        cb.SetClipboardData(win32con.CF_UNICODETEXT, cb_text)
        cb.CloseClipboard()
