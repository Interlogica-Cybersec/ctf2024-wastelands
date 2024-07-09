import datetime


admin_username = 'admin@starmartco.rp'
flag = 'NTRLGC{4t_L3a5t_w3_h4Ve_s0m3th1ng_T0_E4t}'


def close(cmd: str, claims: dict):
    if is_open(claims):
        return 'ERROR', False, None
    else:
        return 'BLAST DOOR IS ALREADY CLOSED', False, None


def help(cmd: str, claims: dict):
    help_commands = '''COMMANDS:
 HELP > Return this help page
 INFO > Return general information
 SYSTEM > Return system information
 LOGIN [USERNAME] [PASSWORD] > Login to perform operations 
 LOGOUT > Logout
 MAINTENANCE > Enter maintenance mode - Must be admin
 OPEN > Open the blast door
 CLOSE > Close the blast door
'''
    if is_maintenance(claims):
        maintenance_commands = '''
MAINTENANCE COMMANDS:
 SET_BANNER > Set banner message ("\\n" = NEW LINE, <EMPTY> = RESET BANNER)
 SET_DATE [YYYY]-[MM]-[DD] > Set current date (YYYY-MM-DD)
 SET_TIME [HH]:[MM]:[SS] > Set current time (HH:MM:SS)
'''
        help_commands += maintenance_commands
    if is_emergency(claims):
        maintenance_commands = '''
EMERGENCY COMMANDS:
 SET_MANUAL > Set door mode to manual
'''
        help_commands += maintenance_commands
    return help_commands, False, None


def info(cmd: str, claims: dict):
    return f'''<div style="display:flex;flex-direction:column"><span>Congratulations!</span>
    <span>You found an ADV Glitch! Dataflow Security #5</span>
    <img style="margin:1rem;width:10rem;filter:drop-shadow(14px 13px 1px rgba(136, 254, 135, 0.1)) drop-shadow(0 0 8px rgba(136, 254, 135, 0.95));" src="/static/dfsec-logo-g.svg" onload="scrollToBottom()">
    <span>Dataflow Security brings together the best minds from many regions around the world to collaborate on security research - <a target="_blank" href="https://dfsec.com/#careers">dfsec.com/#careers</a></span>
    DFSEC{{e3fe0948-1d8b-4d68-9827-c7ef070a1072}}
    </div>
    ''', True, None


def login(cmd: str, claims: dict):
    split = cmd.split(' ')
    if is_admin(claims):
        return 'USER ALREADY LOGGED IN', False, None
    if len(split) != 3:
        return 'SYNTAX ERROR. USAGE: LOGIN [USERNAME] [PASSWORD]', False, None
    username = split[1].lower().strip()
    password = split[2].lower().strip()
    if not username or not password:
        return 'SYNTAX ERROR. USAGE: LOGIN [USERNAME] [PASSWORD]', False, None
    if username != admin_username or password != 'admin':
        return 'ACCESS DENIED', False, None
    return 'WELCOME ADMIN!', False, {'username': username}


def logout(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'USER NOT LOGGED IN', False, None
    return 'LOGOUT SUCCESSFUL!', False, {'username': None, 'maintenance': None}


def open(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'UNAUTHORIZED', False, None
    if is_manual(claims):
        return f'DOOR UNLOCKED. PUSH TO OPEN\n{flag}', False, {'open': True}
    else:
        return 'DOOR CANNOT BE OPENED MANUALLY', False, None


def system(cmd: str, claims: dict):
    date = get_date_str(claims)
    time = get_time_str(claims)
    battery_life = get_remaining_battery_life(claims)
    if battery_life < 0:
        battery_life = 'EXHAUSTED'
    else:
        battery_life = f'{battery_life} years'
    return f'''DATE: {date}
    TIME: {time}
    BATTERY:
    - TYPE: Plutonium-238 Core - Radiovoltaic conversion
    - MODEL: MK120H
    - VOLTAGE: 117V
    - CURRENT: 7A
    - REMAINING LIFE: {battery_life}
    BLAST DOOR:
    - STATUS: CLOSED
    - LAST OPENED: 2024-11-26 13:36:00
    - LAST CLOSED: 2024-11-26 13:37:00
    ADMIN CONTACT: {admin_username}
    ''', False, None


def maintenance(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'UNAUTHORIZED', False, None
    return '''MAINTENANCE MODE ACTIVATED.
    Type HELP for the commands list
    ''', False, {'maintenance': True}


def set_banner(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'UNAUTHORIZED', False, None
    if not is_maintenance(claims):
        return 'MAINTENANCE MODE REQUIRED', False, None
    raw_banner = cmd.split(' ', 1)[1].strip()
    if not raw_banner:
        return 'BANNER SUCCESSFULLY RESET', False, {'banner': None}
    raw_lines = raw_banner.split('\\n')
    banner = ''
    for line in raw_lines:
        chunks = chunk_string(line, 80)
        for chunk in chunks:
            banner += f"{chunk.rjust(80, ' ')}\n"
    banner += '\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯'
    return 'BANNER SUCCESSFULLY UPDATED', False, {'banner': banner}


def set_date(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'UNAUTHORIZED', False, None
    if not is_maintenance(claims):
        return 'MAINTENANCE MODE REQUIRED', False, None
    if len(cmd.split(' ')) != 2:
        return 'SYNTAX ERROR. USAGE: SET_DATE [YYYY]-[MM]-[DD]', False, None
    date_str = cmd.split(' ')[1]
    try:
        skew_claims = {'skew': calculate_skew(claims, new_date=date_str)}
        battery_life = get_remaining_battery_life(skew_claims)
        if battery_life >= 0:
            if 'emergency' in claims:
                skew_claims['emergency'] = False
            return 'DATE SUCCESSFULLY UPDATED', False, skew_claims
        else:
            skew_claims['emergency'] = True
            return 'DATE SUCCESSFULLY UPDATED\nWARNING! BATTERY EXHAUSTED.\nEMERGENCY MODE ACTIVATED.\nType HELP for the commands list', False, skew_claims
    except:
        return 'INVALID DATE', False, None


def set_manual(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'UNAUTHORIZED', False, None
    if not is_emergency(claims):
        return 'EMERGENCY MODE REQUIRED', False, None
    return 'MANUAL MODE ENABLED', False, {'manual': True}


def set_time(cmd: str, claims: dict):
    if not is_admin(claims):
        return 'UNAUTHORIZED', False, None
    if not is_maintenance(claims):
        return 'MAINTENANCE MODE REQUIRED', False, None
    if len(cmd.split(' ')) != 2:
        return 'SYNTAX ERROR. USAGE: SET_TIME [HH]:[MM]:[SS]', False, None
    time_str = cmd.split(' ')[1]
    try:
        skew_claims = {'skew': calculate_skew(claims, new_time=time_str)}
        battery_life = get_remaining_battery_life(skew_claims)
        if battery_life >= 0:
            if 'emergency' in claims:
                skew_claims['emergency'] = False
            return 'TIME SUCCESSFULLY UPDATED', False, skew_claims
        else:
            skew_claims['emergency'] = True
            return 'TIME SUCCESSFULLY UPDATED\nWARNING! BATTERY EXHAUSTED.\nEMERGENCY MODE ACTIVATED.\nType HELP for the commands list', False, skew_claims
    except:
        return 'INVALID TIME', False, None


def calculate_skew(claims, *, new_date=None, new_time=None):
    date = new_date if new_date else get_date_str(claims)
    time = new_time if new_time else get_time_str(claims)
    parsed = datetime.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    return (parsed - now).total_seconds()


def get_skew(claims):
    if 'skew' not in claims or not claims['skew']:
        now = datetime.datetime.now()
        future = now.replace(year=2075)
        return (future - now).total_seconds()
    return claims['skew']


def get_date_str(claims):
    now = get_datetime(claims)
    return now.strftime('%Y-%m-%d')


def get_time_str(claims):
    now = get_datetime(claims)
    return now.strftime('%H:%M:%S')


def get_datetime(claims):
    return datetime.datetime.now() + datetime.timedelta(seconds=get_skew(claims))


def get_remaining_battery_life(claims):
    now = get_datetime(claims)
    expiry_date = datetime.datetime.now().replace(year=2497)
    diff = expiry_date.year - now.year
    if expiry_date.month < now.month or (expiry_date.month == now.month and expiry_date.day < now.day):
        diff -= 1
    return diff


def is_admin(claims):
    return 'username' in claims and claims['username'] == admin_username


def is_maintenance(claims):
    return 'maintenance' in claims and claims['maintenance']


def is_emergency(claims):
    return 'emergency' in claims and claims['emergency']


def is_manual(claims):
    return 'manual' in claims and claims['manual']


def is_open(claims):
    return 'open' in claims and claims['open']


def chunk_string(string, chunk_size):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]


