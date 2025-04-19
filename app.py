from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sos_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_name TEXT,
            quantity INTEGER,
            location TEXT
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            ngo TEXT
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS damage_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporter_name TEXT,
            location TEXT,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC')
    alerts = cursor.fetchall()
    conn.close()
    return render_template('index.html', alerts=alerts)

@app.route('/add_alert', methods=['POST'])
def add_alert():
    alert = request.form['alert']
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO alerts (alert) VALUES (?)', (alert,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/sos')
def sos():
    return render_template('sos.html')

@app.route('/submit_sos', methods=['POST'])
def submit_sos():
    name = request.form['name']
    location = request.form['location']
    message = request.form['message']
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sos_requests (name, location, message) VALUES (?, ?, ?)', (name, location, message))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/resources')
def resources():
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resources')
    resources = cursor.fetchall()
    conn.close()
    return render_template('resources.html', resources=resources)

@app.route('/add_resource', methods=['POST'])
def add_resource():
    resource_name = request.form['resource_name']
    quantity = request.form['quantity']
    location = request.form['location']
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resources (resource_name, quantity, location) VALUES (?, ?, ?)', (resource_name, quantity, location))
    conn.commit()
    conn.close()
    return redirect(url_for('resources'))

@app.route('/volunteers')
def volunteers():
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM volunteers')
    volunteers = cursor.fetchall()
    conn.close()
    return render_template('volunteers.html', volunteers=volunteers)

@app.route('/add_volunteer', methods=['POST'])
def add_volunteer():
    name = request.form['name']
    contact = request.form['contact']
    ngo = request.form['ngo']
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO volunteers (name, contact, ngo) VALUES (?, ?, ?)', (name, contact, ngo))
    conn.commit()
    conn.close()
    return redirect(url_for('volunteers'))

@app.route('/damage')
def damage():
    return render_template('damage.html')

@app.route('/submit_damage', methods=['POST'])
def submit_damage():
    reporter_name = request.form['reporter_name']
    location = request.form['location']
    description = request.form['description']
    conn = sqlite3.connect('disaster_relief.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO damage_reports (reporter_name, location, description) VALUES (?, ?, ?)', (reporter_name, location, description))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/resources_and_contacts')
def resources_and_contacts():
    kodagu_district_disaster_management_authority = {
        "name": "Kodagu District Disaster Management Authority (KDDMA)",
        "address": "Kodagu District Collectorate, Madikeri, Kodagu, Karnataka, India",
        "phone": "+91-8272-229001",
        "email": "dc.kodagu@nic.in",
        "website": "https://kodagu.nic.in/"
    }

    karnataka_state_disaster_management_authority = {
        "name": "Karnataka State Disaster Management Authority (KSDMA)",
        "address": "Revenue Department (Disaster Management), M.S. Building, Bengaluru, Karnataka, India",
        "phone": "+91-80-22032457",
        "email": "sdma.rev@karnataka.gov.in",
        "website": "https://ksdma.karnataka.gov.in/"
    }

    police = {
        "emergency_number": "100",
        "kodagu_district_police_headquarters": {
            "phone": "+91-8272-225555",
            "website": "https://kodagupolice.karnataka.gov.in/"
        }
    }

    fire_department = {
        "emergency_number": "101",
        "madikeri_fire_station": {
            "phone": "+91-8272-229299"
        }
    }

    medical_services = {
        "emergency_number": "108",
        "kodagu_institute_of_medical_sciences": {
            "address": "Madikeri, Kodagu, Karnataka, India",
            "phone": "+91-8272-220606",
            "website": "https://kims.karnataka.gov.in/"
        }
    }

    kodagu_relief_and_rehabilitation_trust = {
        "contact_person": "Mr. Ramesh Ponnappa",
        "phone": "+91-8272-227777",
        "email": "kodagurelief@trust.org",
        "website": "https://kodagurelief.org/"
    }

    coorg_wellness_foundation = {
        "contact_person": "Ms. Anitha Cariappa",
        "phone": "+91-8272-224444",
        "email": "info@coorgwellness.org",
        "website": "https://coorgwellness.org/"
    }

    online_resources = {
        "national_disaster_management_authority": "https://ndma.gov.in/",
        "karnataka_state_disaster_management_authority": "https://ksdma.karnataka.gov.in/",
        "kodagu_district_administration": "https://kodagu.nic.in/"
    }

    madikeri_relief_center = {
        "address": "Near Raja's Seat, Madikeri, Kodagu, Karnataka, India",
        "phone": "+91-8272-225111"
    }

    kushalnagar_shelter = {
        "address": "Main Road, Kushalnagar, Kodagu, Karnataka, India",
        "phone": "+91-8276-274555"
    }

    virajpet_relief_center = {
        "address": "College Road, Virajpet, Kodagu, Karnataka, India",
        "phone": "+91-8277-265555"
    }

    return render_template('resources_and_contacts.html',
                           kodagu_district_disaster_management_authority=kodagu_district_disaster_management_authority,
                           karnataka_state_disaster_management_authority=karnataka_state_disaster_management_authority,
                           police=police,
                           fire_department=fire_department,
                           medical_services=medical_services,
                           kodagu_relief_and_rehabilitation_trust=kodagu_relief_and_rehabilitation_trust,
                           coorg_wellness_foundation=coorg_wellness_foundation,
                           online_resources=online_resources,
                           madikeri_relief_center=madikeri_relief_center,
                           kushalnagar_shelter=kushalnagar_shelter,
                           virajpet_relief_center=virajpet_relief_center)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)