import plugin

when, lapse = '6am', '24h'
telegram, util = plugin.get("telegram", "util")


def run():
    with util.tmp_fp(suffix=".jpg") as tmp_fp:
        util.screenshot(tmp_fp)
        telegram.send_me_picture(tmp_fp, caption="Desktop")
