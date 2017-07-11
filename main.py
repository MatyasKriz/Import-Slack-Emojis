import argparse
import re
import time
import sys
import signal
from os import walk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Emoji:
    name = ""
    path = ""

    def __init__(self, name, path):
        self.name = name
        self.path = path


def signal_handler(signal, frame):
    if signal is signal.SIGINT:
        print('That\'s okay, see you later!')
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)


def add_emoji(driver, emoji):
    file_element = driver.find_element_by_id('emojiimg')
    file_element.send_keys(emoji.path)

    text_element = driver.find_element_by_id('emojiname')
    text_element.send_keys(emoji.name, Keys.RETURN)


team = input('Team name: ')
path = input('Path: /Users/')
driver = webdriver.Chrome()
driver.get('https://{}.slack.com/customize/emoji'.format(team))

while "Custom Emoji" not in driver.title:
    time.sleep(1)

_, _, filenames = next(walk(path), (None, None, []))
no_extension = re.compile(r"^([^.]*).*")
for filename in filenames:
    emoji_name = re.search(no_extension, filename).group(1)
    emoji = Emoji(emoji_name, path + '/' + filename)
    add_emoji(driver, emoji)
