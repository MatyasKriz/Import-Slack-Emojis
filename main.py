import argparse
import re
import time
import sys
import signal
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Emoji:
    name = ""
    path = ""

    def __init__(self, name, path):
        self.name = name
        self.path = path


def signal_handler(sig, frame):
    if sig is signal.SIGINT:
        print('See you later!')
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)


def add_emoji(driver, emoji):
    file_element = driver.find_element_by_id('emojiimg')
    file_element.send_keys(emoji.path)

    text_element = driver.find_element_by_id('emojiname')
    text_element.send_keys(emoji.name, Keys.RETURN)


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--team', help='Name of the team for which you wish to add emojis.')
parser.add_argument('-p', '--path', help='Path to the emoji directory.')
args = parser.parse_args()

if args.team:
    team = args.team
else:
    team = input('Team name: ')
team = team.replace(' ', '').lower()

while True:
    if args.path:
        path = args.path
    else:
        path = '/Users/'
        path += input('Path: /Users/')

    if os.path.exists(path):
        break
    else:
        print('Invalid path, try again')
        path = None
        args.path = None


print('Please log in when the browser opens.')
time.sleep(2)
driver = webdriver.Chrome()
driver.get('https://{}.slack.com/customize/emoji'.format(team))

while 'Custom Emoji' not in driver.title:
    if 'slack.com' not in driver.current_url:
        print('Navigated out of slack website, quitting...')
        driver.close()
        sys.exit(1)
    time.sleep(1)

known_extensions = ['png', 'jpg', 'gif']
_, _, files = next(os.walk(path), (None, None, []))
no_extension = re.compile(r"^([^.]*).*")
for file in files:
    filepath = path + '/' + file
    tmpArray = file.split('.')
    filename = tmpArray[0]
    extension = tmpArray[1]
    if extension not in known_extensions:
        print(extension)
        continue

    emoji = Emoji(filename, filepath)
    add_emoji(driver, emoji)

driver.close()