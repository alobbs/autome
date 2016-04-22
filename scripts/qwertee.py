import plugin
import webest as w

when, lapse = '9am', '24h'
telegram, smtp, util = plugin.get("telegram", "smtp", "util")


def run():
    crop = (0, 100, 1350, 735)
    with util.tmp_fp(suffix='.png') as tmp_fp:
        w.screenshot.save("https://www.qwertee.com/", tmp_fp, crop=crop)
        telegram.send_me_picture(tmp_fp)
        smtp.send_files("alvaro@alobbs.com", tmp_fp)
