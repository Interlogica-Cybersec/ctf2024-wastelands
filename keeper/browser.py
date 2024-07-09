import os
import time

from dotenv import load_dotenv
from flask import Flask, request
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

load_dotenv()
app = Flask(__name__)
valid_netlocs = [os.getenv('BROWSER_VALID_DESTINATION_NETLOC')]

driver = None
port = int(os.getenv('BROWSER_CONTROLLER_PORT'))

# NOTE: this implementation is inherently NOT concurrent, but whatever.

current_url = None
def request_interceptor(request):
    global current_url
    print(f'Request url {request.url}')
    if request.host not in valid_netlocs:
        request.abort()
        return
    if current_url == request.url or current_url == request.url + '/':
        print(f'Unsetting {current_url=}')
        current_url = None
        print(list(request.headers.keys()))

def visit_url(url):
    global current_url
    current_url = url
    try:
        driver.implicitly_wait(5)
        driver.get(url)
        while True:
            ready_state = driver.execute_script('return document.readyState')
            if ready_state == 'complete':
                break
            time.sleep(0.2)
    except Exception as e:
        print(e)


@app.route('/visit')
def visit():
    url = request.args.get('url')
    action = request.args.get('action')
    print(f'visiting url {url}')
    visit_url(url)
    if action:
        driver.execute_script(action)
    return ''


def start():
    global driver
    service = Service(executable_path='/chromedriver/chromedriver-linux64/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=800,600")
    driver = webdriver.Chrome(options=options, service=service)
    driver.request_interceptor = request_interceptor
    print('Browser spinned up')
    app.run(port=port, host='0.0.0.0')


if __name__ == '__main__':
    start()
