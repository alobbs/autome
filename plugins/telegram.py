import os
import tempfile
import urllib.parse

import pluginconf
import requests
import telepot
from yapsy.IPlugin import IPlugin


ERROR_USER_UNKNOWN = ("I don't know you, but I'll tell you something. "
                      "Sometimes, I use words that I don't "
                      "know to make me seem more… photosynthesis.")

ERROR_NO_USERID = ("You gotta set yourself a name alias "
                   "if you wanna talk to me.")


class Keyboard:
    def __init__(self, items_per_line=3):
        self._markup = None
        self._keyboard = []
        self.items_per_line = items_per_line

    # Guts
    def _get_markup(self):
        if self._markup:
            return self._markup

        if self._keyboard:
            return telepot.namedtuple.ReplyKeyboardMarkup(keyboard=[self._keyboard])

    def get_message_params(self, text):
        return dict(text=text, reply_markup=self._get_markup())

    # Public
    def hide_keyboard(self):
        self._markup = telepot.namedtuple.ReplyKeyboardHide()

    def add(self, text, request_location=False, request_contact=False):
        if request_location:
            button = telepot.namedtuple.KeyboardButton(text=text, request_location=True)
            return self._keyboard.append(button)
        if request_contact:
            button = dict(text=text, request_contact=True)
            return self._keyboard.append(button)
        return self._keyboard.append(text)


class Telegram(IPlugin):
    # Embedded class refs
    Keyboard = Keyboard

    def __init__(self):
        super().__init__()

        # Read configuration
        self.conf = pluginconf.get('telegram')

        # Instance
        self.bot = telepot.Bot(self.conf['BOT_TOKEN'])
        self.bot.message_loop(self._msg_received)

    def reply_command(self, userid, command, live=True):
        # All in one message
        if not live:
            with os.popen(command) as f:
                self.send_msg(userid, f.read())
            return

        # Message per line
        with os.popen(command) as f:
            for line in f:
                if len(line.strip()):
                    self.send_msg(userid, line)

    def msg_received_cb(self, msg):
        None

    def _msg_received(self, msg):
        userid = msg['from'].get('id')
        username = msg['from'].get('username')

        if not username:
            self.send_picture(userid, "static/NoAlias.jpg")
            self.send_msg(userid, ERROR_NO_USERID)
            return

        if username != self.conf['ME_USER']:
            self.bot.sendMessage(userid, ERROR_USER_UNKNOWN)
            return

        self.msg_received_cb(msg)

        """
        first = msg['text'].split(' ')[0]
        if first == "ping":
            self._reply_command(userid, "ping -c 2 home.corp.redhat.com", False)
        else:
            self.bot.sendMessage(userid, "Am not sure what you want me to do")
        """

    def send_msg(self, user_id, msg):
        self.bot.sendMessage(user_id, msg)

    def send_picture(self, user_id, path, caption=None, tmp_suffix=None):
        # HTTP
        if path.startswith('http://') or path.startswith("https://"):
            r = requests.get(path)

            p = urllib.parse.urlparse(path)
            filename = os.path.basename(p.path)
            if not tmp_suffix:
                tmp_suffix = filename.split('.')[-1]

            tmp_dir = tempfile.gettempdir()
            tmp_fp = os.path.join(tmp_dir, filename + '.%s' % tmp_suffix)

            with open(tmp_fp, 'w+b') as f:
                f.write(r.content)
                f.seek(0)
                self.bot.sendPhoto(user_id, f, caption=caption)

            os.unlink(tmp_fp)
            return

        # Local file
        with open(path, 'rb') as f:
            self.bot.sendPhoto(user_id, f, caption=caption)

    # Me
    #
    def send_me_msg(self, *args, **kwargs):
        self.send_msg(self.conf['ME_ID'], *args, **kwargs)

    def send_me_picture(self, *args, **kwargs):
        return self.send_picture(self.conf['ME_ID'], *args, **kwargs)
