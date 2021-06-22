import cli_ui
from requests.api import head

import requests
import json
import random
import base64
import time
import urllib3

from time import sleep
from termcolor import cprint
from pyfiglet import figlet_format
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cli_ui.setup(color="always")


register_link = "https://discordapp.com/api/auth/register"
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
PASSWORD = "12390@43hjfdx6"

API_KEY = "YOUR API KEY HERE"
SITE_KEY = "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34"


def title():
    cprint(figlet_format(("discord gen by Zeczero"), font='roman', width=300),
           'cyan', attrs=['bold'], end='')


def gen_email():
    new_mail = ""
    i = 0
    length = random.randint(4, 10)
    while(i < length):
        new_mail += random.choice(alphabet)
        i += 1

    return new_mail + "@gmail.com"


def get_username():
    response = requests.get(
        "https://raw.githubusercontent.com/dominictarr/random-name/master/names.json")
    response_json = response.json()
    random_index = random.randint(0, 8000)
    username = response_json[random_index]

    return username


def get_super_properties(os, browser, useragent, browser_version, os_version, client_build):
    return {
        "os": os,
        "browser": browser,
        "device": "",
        "browser_user_agent": useragent,
        "browser_version": browser_version,
        "os_version": os_version,
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": client_build,
        "client_event_source": None
    }


def get_user_agent():
    return ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0")


def get_headers():
    return {
        'Host': 'discordapp.com',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Referer': 'https://discordapp.com/register',
        'Origin': 'https://discordapp.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'user-agent': "",
        'X-Fingerprint': "",
        'X-Super-Properties': ''
    }


def get_user_agent():
    return ("Windows", "Firefox", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0", "54.0", "7")


def register():
    headers = get_headers()
    cli_ui.info_2("Fetching all important data..")
    os, browser, headers['user-agent'], browserver, osvers = get_user_agent()
    r = requests.Session()
    fingerprint_json = requests.get("https://discordapp.com/api/v6/experiments",
                                    timeout=15000, headers=get_headers(), verify=False).json()
    fingerprint = fingerprint_json["fingerprint"]
    xsuperprop = base64.b64encode(json.dumps(get_super_properties(
        os, browser, headers['user-agent'], browserver, osvers, 36127), separators=",:").encode()).decode()
    headers['X-Super-Properties'] = xsuperprop

    email = gen_email()
    username = get_username()

    payload = {
        'fingerprint': fingerprint,
        'email': email,
        'username': username,
        'password': PASSWORD,
        'invite': None,
        'captcha_key': None,
        'consent': True,
        "date_of_birth": "2001-01-01",
        'gift_code_sku_id': None
    }
    messages = f'--------------------\nMail: {email}\nUsername: {username}\nPassword: {PASSWORD}\n--------------------\n'
    sleep(5)
    cli_ui.info_3(messages)

    response = r.post('https://discordapp.com/api/v6/auth/register',
                      json=payload, headers=headers, timeout=15000, verify=False)

    cli_ui.error(response.text)

    if 'captcha-required' in response.text:
        session = requests.Session()
        sleep(2)
        captcha_id = session.get(
            # change this shitty link
            f"http://2captcha.com/in.php?key={API_KEY}&method=hcaptcha&sitekey={SITE_KEY}&pageurl={register_link}").text.split('|')[1]

        recaptcha_answer = session.get(
            f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}").text

        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            sleep(5)
            cli_ui.warning(recaptcha_answer)
            recaptcha_answer = session.get(
                f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}").text

        recaptcha_answer = recaptcha_answer.split('|')[1]
        cli_ui.info_1("Solved captcha successfully: " + recaptcha_answer)
        payload['captcha_key'] = recaptcha_answer
        cli_ui.info_2("resending payload..")
        time.sleep(15)
        response = r.post('https://discordapp.com/api/v6/auth/register',
                          json=payload, headers=headers, timeout=15000, verify=False)
        token = response.json()
        print(token)


title()
register()
