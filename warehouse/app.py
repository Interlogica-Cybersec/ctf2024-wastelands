import os
import uuid
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from commands import cmd

load_dotenv()
app = Flask('Warehouse')
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
app.config['JWT_ACCESS_COOKIE_NAME'] = 'progress'
app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'
app.config['JWT_CSRF_CHECK_DEFAULT'] = False
app.config['JWT_CSRF_CHECK_FORM'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_CSRF_FIELD_NAME'] = 'csrf_token'
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

commands_mapping = {
    'close': cmd.close,
    'help': cmd.help,
    'info': cmd.info,
    'open': cmd.open,
    'login': cmd.login,
    'logout': cmd.logout,
    'system': cmd.system,
    'maintenance': cmd.maintenance,
    'set_banner': cmd.set_banner,
    'set_date': cmd.set_date,
    'set_time': cmd.set_time,
    'set_manual': cmd.set_manual,
}


@app.route('/')
@jwt_required(optional=True)
def room():
    claims = get_jwt()
    is_open = cmd.is_open(claims)
    flag = cmd.flag if is_open else None
    return render_template('room.html', banner=banner(claims), flag=flag)


def stdout(response: str, is_html: bool):
    return jsonify({'stdout': response, 'parse': is_html})


@app.route('/cmd', methods=['POST'])
@jwt_required(optional=True)
def post_cmd():
    if request.is_json:
        claims = get_jwt()
        json_data = request.get_json()
        command = json_data['cmd']
        if not command:
            return stdout('COMMAND NOT RECOGNIZED', is_html=False)
        command_key = command.lower().split(' ')[0]
        if command_key not in commands_mapping:
            return stdout('COMMAND NOT RECOGNIZED', is_html=False)
        cmd_stdout, is_html, new_claims = commands_mapping[command_key](command, claims)
        response = make_response(stdout(cmd_stdout, is_html=is_html))
        update_progress(response, claims, new_claims)
        return response
    return stdout('RESULT', is_html=False)


def update_progress(response, claims, updated_claims: dict):
    if updated_claims:
        claims.update(updated_claims)
        identity = get_jwt_identity()
        if not identity:
            identity = uuid.uuid4()
        progress_token = create_access_token(identity=identity, additional_claims=claims)
        response.set_cookie('progress', progress_token, httponly=True, secure=False)


def banner(claims: dict):
    if 'banner' in claims and claims['banner']:
        return claims['banner']
    username = claims['username'].upper() if 'username' in claims and claims['username'] else 'GUEST'
    return f'''________________________________________________________________________________

       STARMART CORP OS - VERSION 1.3.37
       COPYRIGHT 2024-2075 STARMART CORP
       WAREHOUSE TERMINAL 1

¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
Connecting to remote host...
Welcome, {username}!
Type HELP for the commands list'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5047)
