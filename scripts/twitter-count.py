import re
import time

import plugin
import webest as w

lapse = '1h'
gspreadsheet = plugin.get("gspreadsheet")


def get_twitter_count():
    with w.browser.new_auto("https://twitter.com/alobbs") as b:
        raw = w.get_text(b, ".ProfileNav-list")

    raw = raw.replace('\n', ' ').replace(',', '')
    fers = re.findall(r'FOLLOWERS (\d+)', raw)[0]
    fing = re.findall(r'FOLLOWING (\d+)', raw)[0]
    return (fers, fing)


def add_to_spreadsheet(fers, fing):
    s = gspreadsheet.open_sheet1("Twitter autome")
    s.append_row([time.strftime("%m/%d/%y %H:%M:%S"), fers, fing])


def run():
    add_to_spreadsheet(*get_twitter_count())
