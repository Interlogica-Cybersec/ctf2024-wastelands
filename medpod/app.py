import os.path
import sqlite3
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

load_dotenv()
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'NUKENUKE'  # lol yes it's in rockyou
app.config['JWT_COOKIE_SECURE'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365000)
jwt = JWTManager(app)
db_file = 'db.db'
flag = os.getenv('FLAG')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sponsor')
def sponsor():
    return render_template('sponsor.html')


@app.route('/api/v1/login', methods=['get'])
def guest_login():
    additional_claims = {
        'glitch1': 'Congratulations! You found an ADV Glitch! Result Consulting #1',
        'glitch2': 'Systematically acquire new customers with a digital, replicable and effective business development model.',
        'glitch3': 'Find out more on https://www.resultconsulting.it/',
        'glitch4': 'RESULT{c988a66b-2f5e-414e-af62-7af07788a49b}',
    }
    token = create_access_token(identity='940f8687-e53c-4011-acd9-fd60a3314726', additional_claims=additional_claims)
    return jsonify({'token': token})


@app.route('/api/v1/whoami', methods=['GET'])
@jwt_required()
def whoami():
    conn = sqlite3.connect(db_file, uri=True)
    try:
        cursor = conn.cursor()
        sub = get_jwt_identity()
        cursor.execute(f'SELECT d.name, d.can_start_therapy FROM doctors d WHERE id = ?', [sub])
        rows = cursor.fetchall()
    finally:
        conn.close()
    if rows and len(rows) > 0:
        return {'name': rows[0][0], 'canStartTherapy': rows[0][1]}
    return {'name': None}


@app.route('/api/v1/therapy-history', methods=['GET'])
@jwt_required()
def therapy_history():
    conn = sqlite3.connect(db_file, uri=True)
    history = []
    try:
        cursor = conn.cursor()
        sub = get_jwt_identity()
        cursor.execute(f"SELECT t.patient, t.therapy, d.name, d.id FROM therapy_history t join doctors d on d.id = t.doctor_id WHERE d.id = '{sub}'")
        rows = cursor.fetchall()
        for row in rows:
            history.append({
                'patient': row[0],
                'therapy': row[1],
                'doctor': row[2],
                'doctorId': row[3],
            })
    finally:
        conn.close()
    return jsonify(history), 200


@app.route('/api/v1/start-therapy', methods=['POST'])
@jwt_required()
def start_therapy():
    conn = sqlite3.connect(db_file, uri=True)
    can_start_therapy = False
    try:
        cursor = conn.cursor()
        sub = get_jwt_identity()
        cursor.execute(f'SELECT d.can_start_therapy FROM doctors d WHERE d.id = ?', [sub])
        rows = cursor.fetchall()
        if len(rows) > 0:
            can_start_therapy = rows[0][0]
    finally:
        conn.close()
    if can_start_therapy:
        return {'message': f'Therapy started. {flag}'}
    else:
        return {'message': 'You are not authorized to independently start a therapy.'}, 401

@app.route('/api/v1/current-patient', methods=['GET'])
@jwt_required()
def current_patient():
    return {
        'name': '- UNKNOWN -',
        'recommendedTherapy': 'RADIATION POISONING TREATMENT',
        'heartRate': '170 BPM',
        'oxygenSaturation': '76%',
        'status': 'CRITICAL',
        'weight': '72 Kg',
        'hydrationLevel': 'SEVERELY DEHYDRATED',
    }


def setup():
    if os.path.exists(db_file):
        return
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS doctors (id TEXT PRIMARY KEY, name TEXT NOT NULL, can_start_therapy BOOLEAN NOT NULL)')
    cursor.execute("INSERT INTO doctors (id, name, can_start_therapy) VALUES (?, ?, ?)",
                   ('940f8687-e53c-4011-acd9-fd60a3314726', 'Intern Alice Cooper', 0))
    cursor.execute("INSERT INTO doctors (id, name, can_start_therapy) VALUES (?, ?, ?)",
                   ('27ee1e79-0f7e-4c14-b780-af9f3da2ac55', 'Intern Jack Hammer', 0))
    cursor.execute("INSERT INTO doctors (id, name, can_start_therapy) VALUES (?, ?, ?)",
                   ('bc9a4742-937d-4553-8a07-dce4ecfc1ba6', 'Dr. Ino Mashet', 1))
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS therapy_history (id TEXT PRIMARY KEY, therapy TEXT NOT NULL, patient TEXT NOT NULL, doctor_id TEXT NOT NULL)')
    cursor.execute("INSERT INTO therapy_history (id, therapy, patient, doctor_id) VALUES (?, ?, ?, ?)", (
        '0f75eab4-ef95-48b8-9333-3879d97500d2', 'Random organ extraction', 'Mr. Willie Carveme',
        '940f8687-e53c-4011-acd9-fd60a3314726'))
    cursor.execute("INSERT INTO therapy_history (id, therapy, patient, doctor_id) VALUES (?, ?, ?, ?)", (
        '2954b9c7-a90f-430d-941f-c7f27ad6018c', 'Surprise euthanasia', 'Ms. Wayu Kilme',
        '940f8687-e53c-4011-acd9-fd60a3314726'))
    cursor.execute("INSERT INTO therapy_history (id, therapy, patient, doctor_id) VALUES (?, ?, ?, ?)", (
        '32100472-e947-4d2a-ac0c-dd2bf6a8f3da', 'Limb reconstruction', 'Ms. Anita Narm',
        '940f8687-e53c-4011-acd9-fd60a3314726'))
    cursor.execute("INSERT INTO therapy_history (id, therapy, patient, doctor_id) VALUES (?, ?, ?, ?)", (
        '629ee8a4-e107-4767-bbee-6223b6edf53a', 'Extraneous object removal', 'Mr. Mike Rotchburns',
        '940f8687-e53c-4011-acd9-fd60a3314726'))
    cursor.execute("INSERT INTO therapy_history (id, therapy, patient, doctor_id) VALUES (?, ?, ?, ?)", (
        '32353ef0-d09e-4451-a184-57c51b4ec098', 'Overdose treatment', 'Mr. Nick O\'Teen',
        'bc9a4742-937d-4553-8a07-dce4ecfc1ba6'))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5030)
