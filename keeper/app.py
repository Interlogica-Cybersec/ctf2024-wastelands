import os
import time
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory, abort

load_dotenv()
app = Flask(__name__)
keeper_token = os.getenv('KEEPER_TOKEN')
confirmation_message = os.getenv('CONFIRMATION_MESSAGE')
flag = os.getenv('FLAG')
base_url = os.getenv('BASE_URL')
browser_base_url = os.getenv('BROWSER_CONTROLLER_BASE_URL')
port = int(os.getenv('PORT'))
max_message_length = 60

keeper_busy = False
access_granted = False
prevent_loops = False

@app.route('/')
def index():
    return render_template('index.html', max_message_length=max_message_length)

@app.route('/.git/')
def git():
    abort(403)

@app.route('/.git/<path:filename>')
def git_contents(filename):
    root_dir = os.path.realpath('exposed_git')
    realpath = os.path.realpath(os.path.join(root_dir, filename))
    if os.path.commonprefix((realpath, root_dir)) != root_dir:
        abort(404)
    if os.path.isdir(realpath):
        abort(403)
    directory = 'exposed_git'
    return send_from_directory(directory, filename)


@app.route('/keeper/')
def keeper():
    global access_granted
    global prevent_loops
    token = request.args.get('token')
    if token != keeper_token:
        abort(401)
    message = request.args.get('message')
    message = message[:max_message_length] if message else ''
    confirmation = request.args.get('msg')
    if confirmation == confirmation_message:
        access_granted = True
        message = ''

    if prevent_loops:
        message = ''
    prevent_loops = True
    return render_template('keeper.html', message=message, confirmation_message=confirmation_message)


def wait_for_keeper_response(message):
    url = f'{base_url}/keeper?token={keeper_token}&message={quote(message)}'
    action = "document.getElementById('submit').click()"
    browser_command_url = f'{browser_base_url}/visit?action={quote(action)}&url={quote(url)}'
    requests.get(browser_command_url)
    time.sleep(2)
    if access_granted:
        return {
            'granted': True,
            'result': f'The keeper granted you access. {flag}'
        }
    else:
        return {
            'granted': False,
            'result': 'The keeper denied your request.'
        }


@app.route('/submit', methods=['POST'])
def submit_message():
    global keeper_busy
    global access_granted
    global prevent_loops
    if keeper_busy:
        return {
            'granted': False,
            'result': 'The keeper is evaluating another request'
        }
    try:
        keeper_busy = True
        message = request.form.get('message')
        if not message:
            message = ''
        if len(message) > max_message_length:
            return {
                'granted': False,
                'result': f'The max length of the message is {max_message_length} characters'
            }
        message = message[:max_message_length]
        keeper_response = wait_for_keeper_response(message)
    except Exception as e:
        keeper_response = {
            'granted': False,
            'result': 'The keeper denied your request.'
        }
        print(e)
    finally:
        keeper_busy = False
        access_granted = False
        prevent_loops = False
    return jsonify(keeper_response)


if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')
