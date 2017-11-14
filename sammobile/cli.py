import sys
import os
import json
from robobrowser import RoboBrowser
from requests.utils import dict_from_cookiejar, add_dict_to_cookiejar
from tqdm import tqdm
import argparse
# @todo create a proper cli
# @todo oop
# @todo tests

def _save_session_cookie(cookie, file):
    # convert cookie jar to json serializable format
    cookie_dict = dict_from_cookiejar(cookie)
    with open(file, 'w') as f:
        json.dump(cookie_dict, f)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download firmwares from sammobile"
    )

    parser.add_argument(
        "-l",
        "--link",
        type=str,
        nargs=1,
        help="Link to the download page of the firmware"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        nargs=1,
        help="Output file name"
    )

    return parser


def download_firmware(browser, firmware_file_url, firmware_file_path):
    browser.open(firmware_file_url)
    a = browser.find("a", {"id": "regular"})

    request = browser.session.get(a['href'], stream=True)
    dir = "/".join(firmware_file_path.split("/")[:-1])
    os.makedirs(dir, exist_ok=True)
    with open(firmware_file_path, "wb") as firmware_file:
        for data in tqdm(request.iter_content(),
                         total=int(request.headers['Content-Length']),
                         unit='B', unit_scale=True):
            firmware_file.write(data)

def main():
    parser = parse_args()
    args = parser.parse_args()
    if not args.link or not args.output:
        parser.print_help()
        exit()

    if os.path.isfile("config.json"):
        config_file = "config.json"
    else:
        config_file = ".example.config.json"

    # Read config file
    with open(config_file, 'r') as f:
        config = json.load(f)

        # browser instance
    browser = RoboBrowser(history=True, parser="html.parser")
    firmware_file_path = args.output[0]
    firmware_file_url = args.link[0]
    if os.path.isfile(config['cookiefile']):
        with open(config['cookiefile'], 'r') as cookie_file:
            # set session cookies
            add_dict_to_cookiejar(browser.session.cookies, json.load(cookie_file))
            download_firmware(browser, firmware_file_url, firmware_file_path)
    else:
        # Browse to sammobile login page
        browser.open("https://www.sammobile.com/login/")
        form = browser.get_form(id="loginform-custom")
        form["log"] = config['username']
        form["pwd"] = config['password']

        browser.submit_form(form)
        if browser.url == "https://www.sammobile.com":
            _save_session_cookie(browser.session.cookies, config['cookiefile'])
            download_firmware(browser, firmware_file_url, firmware_file_path)


if __name__ == "__main__":
    main()