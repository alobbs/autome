import plugin
import webest as w

when = '4pm'
lapse = '24h'
telegram = plugin.get("telegram")


def run():
    with w.browser.new_auto("http://dilbert.com/") as b:
        img = w.get_objs(b, "img.img-comic")[0]
        src = img.get_attribute('src')
    telegram.send_me_picture(src, tmp_suffix='.gif')
