import sys
import os
import json
from robobrowser import RoboBrowser
from requests.utils import dict_from_cookiejar, add_dict_to_cookiejar

# @todo create a proper cli
# @todo oop
# @todo tests

def _save_session_cookie(cookie, file):
    # convert cookie jar to json serializable format
    cookie_dict = dict_from_cookiejar(cookie)
    with open(file, 'w') as f:
        json.dump(cookie_dict, f)


def main():
    if os.path.isfile("config.json"):
        config_file = "config.json"
    else:
        config_file = ".example.config.json"

    # Read config file
    with open(config_file, 'r') as f:
        config = json.load(f)

        # browser instance
    browser = RoboBrowser(history=True)

    if os.path.isfile(config['cookiefile']):
        with open(config['cookiefile'], 'r') as cookie_file:
            # set session cookies
            browser.session.cookies = add_dict_to_cookiejar(
                json.load(cookie_file),
                browser.session.cookies
            )
    else:
        # Browse to sammobile login page
        browser.open("https://www.sammobile.com/login/")
        form = browser.get_form(id="loginform-custom")
        form["log"] = config['username']
        form["pwd"] = config['password']
        firmware_file_path = sys.argv[1]
        firmware_file_url = sys.argv[2]

        browser.submit_form(form)
        if browser.url == "https://www.sammobile.com":
            _save_session_cookie(browser.session.cookies, config['cookiefile'])
            browser.open(firmware_file_url)
            a = browser.find("a", {"id": "regular"})
            request = browser.session.get(a['href'], stream=True)

            with open(firmware_file_path, "wb") as firmware_file:
                firmware_file.write(request.content)

if __name__ == "__main__":
    main()
