import plugin
import webest as w

when = '9am'
lapse = '24h'
telegram, smtp = plugin.get("telegram", "smtp")
TMP = "/tmp/qwertee.png"


def run():
    crop = (0, 100, 1350, 735)
    w.screenshot.save("https://www.qwertee.com/", TMP, crop=crop)
    telegram.send_me_picture(TMP)
    smtp.send_files("alvaro@alobbs.com", TMP)
