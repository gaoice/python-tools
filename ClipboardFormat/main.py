import configparser
import re
import clipboard_helper
import hook_helper

# python3
# ctrl+f1 exit

config = configparser.RawConfigParser()
config.read("format.ini", encoding='UTF-8')

append_top = config.get("DEFAULT", "append_top").replace("\\n", '\n')
pattern = config.get("DEFAULT", "pattern")
append_bottom = config.get("DEFAULT", "append_bottom").replace("\\n", '\n')

ch = clipboard_helper.ClipboardHelper()
hh = hook_helper.HookHelper()
key_set = []


def format_clipboard():
    text = ch.get_unicode_text()
    if text is None:
        return
    m = re.match(pattern, text)
    if m is not None:
        result = append_top
        for group in m.groups():
            result += group
        result += append_bottom
        ch.set_unicode_text(result)


def keyboard_proc(helper_self, n_code, w_param, l_param):
    key = 0xFFFFFFFF & l_param[0]
    event = 0xFFFFFFFF & w_param
    if event == 256:  # down
        key_set.append(key)
    elif event == 257:  # up
        if 67 in key_set and 162 in key_set:  # ctrl+c
            format_clipboard()
        if 112 in key_set and 162 in key_set:  # ctrl+f1
            helper_self.exit()
        key_set.remove(key)


hh.keyboard_proc = keyboard_proc
hh.hook_keyboard()
