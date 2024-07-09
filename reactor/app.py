import datetime
import hashlib
import json
import os.path
import random
import sqlite3

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, abort, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager = LoginManager(app)
login_manager.login_view = 'index'
db_file = 'db.db'
flag = os.getenv('FLAG')


class User:
    def __init__(self, *, id, name=None, username=None, password=None):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.is_active = True
        self.is_authenticated = True

    def get_id(self):
        return self.id


@app.route('/')
def reactor():
    glitch = False
    if request.args.get('gl1tch') is not None:
        print('hehehe')
        glitch = True
    if get_team_variable('started', False):
        return render_template('activation_sequence.html', flag=flag, glitch=glitch)
    return render_template("reactor_off.html", glitch=glitch)


@app.route('/gl34tch')
def gl34tch():
    return render_template("glitch2.html")


@app.route('/control-panel')
def index():
    if current_user.is_authenticated:
        if request.args.get('logout'):
            logout_user()
            return redirect(url_for('index'))
        if get_team_variable('started', False):
            return redirect(url_for('activation_started'))
        return redirect(url_for('maintenance'))
    else:
        if get_team_variable('started', False):
            return redirect(url_for('activation_started'))
        return render_template("index.html", started=get_team_variable('started', False))


@app.route('/control-panel/maintenance', methods=['GET'])
@login_required
def maintenance():
    if get_team_variable('started', False):
        return redirect(url_for('activation_started'))
    return render_template('maintenance.html', username=current_user.name, started=get_team_variable('started', False))


@app.route('/control-panel/api/request-otp', methods=['POST'])
@login_required
def request_otp():
    # super mega giga cryptographically secure otp generation
    otp = str(random.randint(0, 99999999)).zfill(8)
    session['otp'] = otp
    write_log(current_user.id, f'OTP {otp} sent to user {current_user.name}.')
    return {'message': 'An OTP has been sent to your mobile, insert it here to perform the operation.'}

@app.route('/control-panel/api/scram', methods=['POST'])
@login_required
def scram():
    started = get_team_variable('started', False)
    write_log(current_user.id, f'SCRAM emergency shutdown invoked by user {current_user.name}.')
    if started:
        write_log(current_user.id, 'SCRAM emergency shutdown failed. Reason: reactor already shut down.')
    else:
        write_log(current_user.id, 'SCRAM emergency shutdown failed. Reason: user must be joking.')

    return {'error': 'SCRAM failed - You rascal'}


@app.route('/control-panel/api/confirm-otp', methods=['POST'])
@login_required
def confirm_otp():
    otp = request.form['otp']
    success = 'otp' in session and otp == session['otp']
    if 'otp' in session:
        del session['otp']
    else:
        return {'message': f'No OTP. Please request one.'}, 403
    if success:
        write_log(current_user.id, 'Reactor activation sequence started.')
        set_team_variable('started', True)
        return {'message': f'Activation sequence started.', 'url': '/'}
    else:
        write_log(current_user.id, f'Wrong OTP used by user {current_user.name}.')
        return {'message': f'Wrong OTP.'}, 403


def apply_dumb_filter(value: str):
    prohibited_chars = ["'", " ", "\t", "-", ";", "/", "*"]
    for c in prohibited_chars:
        if c in value:
            return False
    return True


def write_log(user_id: str, value: str, seconds_before=0):
    with open(get_log_file(user_id), 'a') as f:
        now = datetime.datetime.now()
        now = now.replace(year=2075)
        if seconds_before:
            now = now - datetime.timedelta(seconds=seconds_before)
        f.write(f'{now:%d.%m.%Y (%H:%M:%S)}: {value}\n')


def get_team_variable(name: str, default: any):
    status_file_name = get_team_status_file()
    with open(status_file_name, 'r') as f:
        status = json.loads(f.read())
    return status[name] if name in status else default

def set_team_variable(name: str, value: any):
    status_file_name = get_team_status_file()
    with open(status_file_name, 'r') as f:
        status = json.loads(f.read())
    status[name] = value
    with open(status_file_name, 'w') as f:
        f.write(json.dumps(status))


@app.route('/control-panel/api/login', methods=['POST'])
def login():
    conn = sqlite3.connect(db_file, uri=True)
    username = request.form['username']
    password = request.form['password']
    system_id = request.form['systemId']
    if not username or not username.strip():
        return {'error': 'No username specified.'}, 400
    if not password or not password.strip():
        return {'error': 'No password specified.'}, 400
    if not system_id or not system_id.strip():
        return {'error': 'No system_id specified.'}, 400
    if not apply_dumb_filter(username):
        return {'error': 'The username contains prohibited characters.'}, 400
    if not apply_dumb_filter(password):
        return {'error': 'The password contains prohibited characters.'}, 400
    if not apply_dumb_filter(system_id):
        return {'error': 'The systemId parameter contains prohibited characters.'}, 400
    rows = []
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}' AND (system_id IS NULL OR system_id = {system_id})")
        rows = cursor.fetchall()
    except Exception as e:
        print(e)
        conn.close()
    finally:
        conn.close()
    if not len(rows):
        return {'error': 'Wrong username or password.'}, 401
    user_id = rows[0][0]
    if not user_id:
        return {'error': 'Null ID? Weird.'}, 400
    user = load_user(user_id)
    login_user(user)
    write_log(user_id, f'User {user.name} ({user.username}) logged in')
    return jsonify({'message': f'Oh hi {user.name}!'})


@login_manager.user_loader
def load_user(sub):
    conn = sqlite3.connect(db_file, uri=True)
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM users WHERE id = ?', [sub])
        rows = cursor.fetchall()
    finally:
        conn.close()
    if rows and len(rows) > 0:
        return User(
            id=rows[0][0],
            name=rows[0][1],
            username=rows[0][2],
            password=rows[0][3],
        )
    return None


def get_log_file(user_id) -> str:
    log_file = os.path.join(get_team_folder(), 'debug.log')
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
        write_log(user_id, 'SCRAM emergency shutdown invoked by user Mark.', 1872)
        write_log(user_id, 'SCRAM emergency shutdown completed.', 1860)

    return log_file


def get_team_status_file() -> str:
    status_file = os.path.join(get_team_folder(), 'status.json')
    if not os.path.exists(status_file):
        with open(status_file, 'w') as f:
            f.write('{}')
    return status_file


def get_team_folder():
    folder_name = get_team_folder_name()
    tmp = 'tmp'
    if not os.path.exists(tmp):
        os.mkdir(tmp)
    sub_logs_folder = os.path.join(tmp, folder_name)
    if not os.path.exists(sub_logs_folder):
        os.mkdir(sub_logs_folder)
    return sub_logs_folder


def get_team_folder_name():
    auth_header = request.headers.get('authorization')
    if not auth_header:
        auth_header = request.headers.get('Authorization')
    if not auth_header:
        auth_header = '<no auth>'  # ok I really need an auth header tho
        print('!!! MISSING AUTHORIZATION HEADER! I NEED IT !!!')
    return hashlib.md5(auth_header.encode()).hexdigest()


@app.route('/control-panel/logs', methods=['GET'])
def logs():
    return abort(401)


@app.route('/control-panel/logs/debug.log', methods=['GET'])
@login_required
def debug_logs():
    return send_file(get_log_file(current_user.id))


def setup():
    if os.path.exists(db_file):
        return
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, system_id INT NOT NULL)')
    cursor.execute("INSERT INTO users (id, name, username, password, system_id) VALUES (?, ?, ?, ?, ?)",
                   ('b496c4e6-b892-47a5-bd41-18097f32e866', 'Mark', 'maintenance', '!?M41nt3n4nc3?!', 1337))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5045)
