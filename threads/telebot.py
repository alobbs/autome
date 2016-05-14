import glob
import os
import re
import time
import types

import plugin
import telepot
import telepot.namedtuple

when = '9am'
telegram, util = plugin.get("telegram", "util")


def msg_cb(self, msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("content_type, chat_type, chat_id", content_type, chat_type, chat_id)

    k = telegram.Keyboard()
    if content_type == 'location':
        print("location", msg['location'])
        k.hide_keyboard()
        self.bot.sendMessage(chat_id, **k.get_message_params("Got it!"))

    # Youtube-dl
    #
    elif content_type == 'text' and msg['text'].startswith("/youtube-dl "):
        tmp = re.findall(r'(http.+?)(?:s|$)', msg['text'], re.M)
        if tmp:
            telegram.send_video(chat_id, tmp[0])
            k.hide_keyboard()
            self.bot.sendMessage(chat_id, **k.get_message_params('youtube-dl'))

    elif content_type == 'text' and 'http' in msg['text']:
        tmp = re.findall(r'(http.+?)(?:s|$)', msg['text'], re.M)
        if tmp:
            url = tmp[0]
            if any([d in url for d in telegram.youtube_dl_sites]):
                k.add("/youtube-dl " + tmp[0])
                self.bot.sendMessage(chat_id, **k.get_message_params('Sent'))

    else:
        k.add('Plain text')
        k.add('Phone', request_contact=True)
        k.add('Location', request_location=True)
        self.bot.sendMessage(chat_id, **k.get_message_params("This is custom keyboard"))


def run():
    telegram.msg_received_cb = types.MethodType(msg_cb, telegram)

    while True:
        time.sleep(60)
