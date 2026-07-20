from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from datetime import date
import hashlib
import uuid
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, '../frontend/templates')
static_dir = os.path.join(base_dir, '../frontend/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'medibridge_ai_secret_key_hackathon_2024'

# ============================================================
# IN-MEMORY DATA STORE  (replace with DB in production)
# ============================================================

# --- HOSPITALS ---
hospitals = [
    {
        'id': 'h1', 'name': 'Mercy General Hospital', 'city': 'New York, USA',
        'specialty': ['General Medicine', 'Cardiology', 'Pediatrics'],
        'rating': 4.8, 'avg_cost': 200, 'waiting_time': 15,
        'available_specialists': ['Cardiologist', 'Pediatrician', 'GP']
    },
    {
        'id': 'h2', 'name': 'St. Jude Health Center', 'city': 'New York, USA',
        'specialty': ['General Medicine', 'Orthopedics', 'Neurology'],
        'rating': 4.5, 'avg_cost': 120, 'waiting_time': 25,
        'available_specialists': ['Orthopedician', 'Neurologist', 'GP']
    },
    {
        'id': 'h3', 'name': 'Oakridge Family Clinic', 'city': 'Boston, USA',
        'specialty': ['Pediatrics', 'Dermatology', 'General Medicine'],
        'rating': 4.6, 'avg_cost': 80, 'waiting_time': 10,
        'available_specialists': ['Pediatrician', 'Dermatologist', 'GP']
    },
    {
        'id': 'h4', 'name': 'Apollo Hospitals', 'city': 'Bangalore, India',
        'specialty': ['Cardiology', 'Neurology', 'Oncology'],
        'rating': 4.9, 'avg_cost': 50, 'waiting_time': 20,
        'available_specialists': ['Cardiologist', 'Neurologist', 'Oncologist']
    },
    {
        'id': 'h5', 'name': 'AIIMS', 'city': 'Delhi, India',
        'specialty': ['General Medicine', 'Pediatrics', 'Dermatology'],
        'rating': 4.7, 'avg_cost': 20, 'waiting_time': 45,
        'available_specialists': ['GP', 'Pediatrician', 'Dermatologist']
    },
    {
        'id': 'h6', 'name': 'Lilavati Hospital', 'city': 'Mumbai, India',
        'specialty': ['Orthopedics', 'Cardiology', 'General Medicine'],
        'rating': 4.8, 'avg_cost': 75, 'waiting_time': 30,
        'available_specialists': ['Orthopedician', 'Cardiologist', 'GP']
    },
    {
        'id': 'h7', 'name': 'St Thomas Hospital', 'city': 'London, UK',
        'specialty': ['Neurology', 'Pediatrics', 'General Medicine'],
        'rating': 4.6, 'avg_cost': 150, 'waiting_time': 20,
        'available_specialists': ['Neurologist', 'Pediatrician', 'GP']
    },
    {
        'id': 'h8', 'name': 'Toronto General Hospital', 'city': 'Toronto, Canada',
        'specialty': ['Cardiology', 'Oncology', 'Dermatology'],
        'rating': 4.9, 'avg_cost': 0, 'waiting_time': 40,
        'available_specialists': ['Cardiologist', 'Oncologist', 'Dermatologist']
    }
]

# --- USERS ---


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


users = [{'id': 'u1',
          'email': 'patient@medibridge.com',
          'password': hash_password('password'),
          'role': 'patient',
          'name': 'John Doe',
          'age': 35,
          'gender': 'Male',
          'medical_history': ['Hypertension']},
         {'id': 'u2',
          'email': 'doctor@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Elizabeth Blackwell',
          'specialty': 'Cardiology',
          'hospital_id': 'h1',
          'availability': ['Monday',
                           'Tuesday',
                           'Wednesday',
                           'Thursday',
                           'Friday'],
          'time_slots': ['09:00 AM',
                         '10:00 AM',
                         '11:00 AM',
                         '02:00 PM',
                         '03:00 PM',
                         '04:00 PM']},
         {'id': 'u3',
          'email': 'admin@medibridge.com',
          'password': hash_password('password'),
          'role': 'hospital_admin',
          'name': 'Hospital Admin',
          'hospital_id': 'h1'},
         {'id': 'u4',
          'email': 'superadmin@medibridge.com',
          'password': hash_password('password'),
          'role': 'super_admin',
          'name': 'Super Admin'},
         {'id': 'u5',
          'email': 'doctor2@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Gregory House',
          'specialty': 'Neurology',
          'hospital_id': 'h2',
          'availability': ['Monday', 'Wednesday', 'Friday'],
          'time_slots': ['10:00 AM', '01:00 PM', '03:00 PM']},
         {'id': 'u6',
          'email': 'doctor3@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Rohan Sharma',
          'specialty': 'Cardiology',
          'hospital_id': 'h4',
          'availability': ['Monday', 'Tuesday', 'Wednesday'],
          'time_slots': ['09:00 AM', '11:00 AM', '02:00 PM']},
         {'id': 'u7',
          'email': 'doctor4@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Anjali Desai',
          'specialty': 'Dermatology',
          'hospital_id': 'h5',
          'availability': ['Tuesday', 'Thursday', 'Saturday'],
          'time_slots': ['10:00 AM', '01:00 PM', '04:00 PM']},
         {'id': 'u8',
          'email': 'doctor5@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Vikram Singh',
          'specialty': 'Orthopedics',
          'hospital_id': 'h6',
          'availability': ['Monday', 'Wednesday', 'Friday'],
          'time_slots': ['09:00 AM', '12:00 PM', '03:00 PM']},
         {'id': 'u9',
          'email': 'doctor6@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Sarah Smith',
          'specialty': 'Pediatrics',
          'hospital_id': 'h7',
          'availability': ['Monday', 'Tuesday', 'Thursday'],
          'time_slots': ['08:00 AM', '10:00 AM', '01:00 PM']},
         {'id': 'u10',
          'email': 'doctor7@medibridge.com',
          'password': hash_password('password'),
          'role': 'doctor',
          'name': 'Dr. Michael Chen',
          'specialty': 'Oncology',
          'hospital_id': 'h8',
          'availability': ['Wednesday', 'Friday'],
          'time_slots': ['09:00 AM', '02:00 PM']},
         ]

# --- APPOINTMENTS ---
appointments = [{'id': 'a1',
                 'patient_id': 'u1',
                 'doctor_id': 'u2',
                 'hospital_id': 'h1',
                 'date': str(date.today()),
                 'slot': '10:00 AM',
                 'status': 'booked',
                 'patient_name': 'John Doe',
                 'doctor_name': 'Dr. Elizabeth Blackwell',
                 'specialty': 'Cardiology',
                 'hospital_name': 'Mercy General Hospital',
                 'hospital_city': 'New York',
                 'patient_age': 35,
                 'patient_gender': 'Male'},
                ]

# --- MEDICAL RECORDS ---
medical_records = [{'id': 'r1',
                    'patient_id': 'u1',
                    'doctor_id': 'u2',
                    'doctor_name': 'Dr. Elizabeth Blackwell',
                    'hospital_name': 'Mercy General Hospital',
                    'diagnosis': 'Hypertension (Controlled)',
                    'prescriptions': ['Amlodipine 5mg – once daily',
                                      'Low-sodium diet recommended'],
                    'reports': ['Blood Pressure Monitoring Chart'],
                    'date': '2024-04-01'},
                   ]

# ============================================================
# HELPER FUNCTIONS
# ============================================================


def find_user(email):
    return next((u for u in users if u['email'] == email), None)


def find_user_by_id(uid):
    return next((u for u in users if u['id'] == uid), None)


def find_hospital(hid):
    return next((h for h in hospitals if h['id'] == hid), None)


def get_hospital_doctors(hospital_id):
    return [u for u in users if u.get(
        'role') == 'doctor' and u.get('hospital_id') == hospital_id]


def get_patient_appointments(patient_id):
    return [a for a in appointments if a['patient_id'] == patient_id]


def get_doctor_appointments(doctor_id):
    return [a for a in appointments if a['doctor_id'] == doctor_id]


def get_hospital_appointments(hospital_id):
    return [a for a in appointments if a['hospital_id'] == hospital_id]


def get_patient_records(patient_id):
    return [r for r in medical_records if r['patient_id'] == patient_id]

# ============================================================
# AI RECOMMENDATION ENGINE
# ============================================================


SYMPTOM_SPECIALTY_MAP = {
    'cardiology': [
        'heart',
        'chest pain',
        'palpitation',
        'cardiac',
        'cardio',
        'shortness of breath'],
    'orthopedics': [
        'bone',
        'joint',
        'fracture',
        'back pain',
        'knee',
        'orthopedic',
        'spine',
        'shoulder'],
    'dermatology': [
        'skin',
        'rash',
        'acne',
        'itch',
        'eczema',
        'derma',
        'allergy',
        'hives'],
    'neurology': [
        'brain',
        'headache',
        'migraine',
        'dizzy',
        'seizure',
        'neuro',
        'memory',
        'tremor'],
    'pediatrics': [
        'child',
        'baby',
        'infant',
        'pediatric',
        'kid',
        'toddler',
        'growth'],
    'ophthalmology': [
        'eye',
        'vision',
        'sight',
        'blind',
        'cataract'],
}


def map_symptoms_to_specialty(symptoms):
    symptoms_lower = symptoms.lower()
    best_specialty = 'General Medicine'
    for specialty, keywords in SYMPTOM_SPECIALTY_MAP.items():
        if any(kw in symptoms_lower for kw in keywords):
            best_specialty = specialty.title()
            break
    return best_specialty


def get_recommendations(symptoms, location, budget):
    required_specialty = map_symptoms_to_specialty(symptoms)
    budget = float(budget)

    # Filter by city (case-insensitive), fallback to all
    matched_hospitals = [
        h for h in hospitals if location.lower() in h['city'].lower()]
    if not matched_hospitals:
        matched_hospitals = list(hospitals)

    results = []
    for h in matched_hospitals:
        score = 50  # base

        # Specialty match
        specialty_match = any(required_specialty.lower()
                              in s.lower() for s in h['specialty'])
        if specialty_match:
            score += 30

        # Rating bonus (max 50 pts)
        score += h['rating'] * 10

        # Budget bonus/penalty
        if h['avg_cost'] <= budget:
            score += 20
        else:
            over = h['avg_cost'] - budget
            score -= min(30, int(over / 50))

        # Waiting time penalty
        score -= h['waiting_time'] // 5

        # Find matching doctor
        docs = get_hospital_doctors(h['id'])
        matching_docs = [
            d for d in docs if required_specialty.lower() in d.get(
                'specialty', '').lower()]
        if matching_docs:
            score += 15
        doctor = matching_docs[0] if matching_docs else (
            docs[0] if docs else None)

        # Build reason
        reasons = []
        if specialty_match:
            reasons.append(f'Specializes in {required_specialty}')
        reasons.append(f'Rated {h["rating"]}/5')
        if h['avg_cost'] <= budget:
            reasons.append(
                f'Within your ${
                    budget:.0f} budget at ${
                    h["avg_cost"]}')
        else:
            reasons.append(
                f'Slightly above budget (${
                    h["avg_cost"]}), but offers excellent care')
        if h['waiting_time'] < 20:
            reasons.append(
                f'Short wait time of only {
                    h["waiting_time"]} minutes')

        results.append({'hospital': h,
                        'doctor': {'name': doctor['name'],
                                   'specialty': doctor.get('specialty',
                                                           '')} if doctor else None,
                        'score': max(10,
                                     round(score)),
                        'reason': ', '.join(reasons) + '.'})

    return sorted(
        results, key=lambda x: x['score'], reverse=True), required_specialty

# ============================================================
# DECORATORS
# ============================================================


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('patient_login'))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in.', 'error')
                return redirect(url_for('patient_login'))
            if session.get('role') not in roles:
                flash('Access denied.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return decorator

# ============================================================
# PUBLIC ROUTES
# ============================================================


@app.route('/')
def index():
    return render_template('index.html', hospitals=hospitals[:3])


@app.route('/search-hospitals')
def search_hospitals():
    query = request.args.get('query', '').lower()
    city = request.args.get('city', '').lower()
    spec = request.args.get('specialty', '').lower()

    results = list(hospitals)
    if query:
        results = [h for h in results if query in h['name'].lower(
        ) or query in h['city'].lower() or any(query in s.lower() for s in h['specialty'])]
    if city:
        results = [h for h in results if city in h['city'].lower()]
    if spec:
        results = [
            h for h in results if any(
                spec in s.lower() for s in h['specialty'])]

    return render_template(
        'search_hospitals.html',
        results=results,
        query=query)


@app.route('/search-doctors')
def search_doctors():
    spec = request.args.get('specialty', '').lower()
    docs = [u for u in users if u.get('role') == 'doctor']
    if spec:
        docs = [d for d in docs if spec in d.get('specialty', '').lower()]
    for d in docs:
        h = find_hospital(d.get('hospital_id', ''))
        d['hospital_name'] = h['name'] if h else 'Unknown'
    return render_template('search_doctors.html', doctors=docs, spec=spec)


@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return redirect(url_for('patient_login'))
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# ============================================================
# PATIENT AUTH
# ============================================================


@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():
    if 'user_id' in session and session.get('role') == 'patient':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = find_user(email)

        if user and user['password'] == hash_password(
                password) and user['role'] == 'patient':
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            session['email'] = user['email']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/patient-register', methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', 'Male')

        # Validation
        if not all([name, email, password, age]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')
        if find_user(email):
            flash('Email already registered. Please log in.', 'error')
            return render_template('register.html')

        new_user = {
            'id': str(uuid.uuid4())[:8], 'email': email, 'name': name,
            'password': hash_password(password), 'role': 'patient',
            'age': int(age), 'gender': gender, 'medical_history': []
        }
        users.append(new_user)

        session['user_id'] = new_user['id']
        session['name'] = new_user['name']
        session['role'] = 'patient'
        session['email'] = new_user['email']
        flash(f'Account created! Welcome to MediBridge AI, {name}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# ============================================================
# HOSPITAL / DOCTOR / ADMIN AUTH
# ============================================================


@app.route('/hospital-login', methods=['GET', 'POST'])
def hospital_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'doctor')
        user = find_user(email)

        if user and user['password'] == hash_password(
                password) and user['role'] == role:
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            session['email'] = user['email']

            if role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif role == 'hospital_admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'super_admin':
                return redirect(url_for('super_admin_dashboard'))
        else:
            flash('Invalid credentials or role mismatch.', 'error')

    return render_template('hospital.html')

# ============================================================
# PATIENT ROUTES
# ============================================================


@app.route('/dashboard')
@login_required
@role_required('patient')
def dashboard():
    patient_id = session['user_id']
    patient_appointments = sorted(
        get_patient_appointments(patient_id),
        key=lambda a: a['date'],
        reverse=True)
    patient_records = sorted(
        get_patient_records(patient_id),
        key=lambda r: r['date'],
        reverse=True)
    upcoming = [a for a in patient_appointments if a['status'] == 'booked']

    stats = {
        'total_appointments': len(patient_appointments),
        'upcoming': len(upcoming),
        'completed': sum(
            1 for a in patient_appointments if a['status'] == 'completed'),
        'records': len(patient_records)}
    return render_template('dashboard.html',
                           stats=stats,
                           appointments=patient_appointments[:3],
                           records=patient_records[:3])


@app.route('/ai-recommend', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def ai_recommend():
    recommendations = None
    matched_specialty = None
    if request.method == 'POST':
        symptoms = request.form.get('symptoms', '')
        location = request.form.get('location', '')
        budget = request.form.get('budget', '200')
        if symptoms and location:
            recommendations, matched_specialty = get_recommendations(
                symptoms, location, budget)
    return render_template(
        'ai_recommend.html',
        recommendations=recommendations,
        matched_specialty=matched_specialty)


@app.route('/appointments')
@login_required
@role_required('patient')
def patient_appointments():
    appts = sorted(
        get_patient_appointments(
            session['user_id']),
        key=lambda a: a['date'],
        reverse=True)
    return render_template('appointments.html', appointments=appts)


@app.route('/records')
@login_required
@role_required('patient')
def patient_records():
    recs = sorted(
        get_patient_records(
            session['user_id']),
        key=lambda r: r['date'],
        reverse=True)
    return render_template('records.html', records=recs)

# ============================================================
# APPOINTMENT BOOKING FLOW
# ============================================================


@app.route('/appointment')
@login_required
@role_required('patient')
def appointment():
    city = request.args.get('city', '').lower()
    spec = request.args.get('specialty', '').lower()
    hosp_id = request.args.get('hospital_id', '')

    filtered = list(hospitals)
    if city:
        filtered = [h for h in filtered if city in h['city'].lower()]
    if spec:
        filtered = [
            h for h in filtered if any(
                spec in s.lower() for s in h['specialty'])]

    # If a hospital was pre-selected (e.g. from AI recommendation)
    if hosp_id:
        selected = find_hospital(hosp_id)
        if selected:
            session['booking_hospital_id'] = hosp_id
            return redirect(url_for('appointment_select_doctor'))

    return render_template('appointment.html', hospitals=filtered, step=1)


@app.route('/appointment/select-hospital', methods=['POST'])
@login_required
@role_required('patient')
def appointment_select_hospital():
    hospital_id = request.form.get('hospital_id')
    session['booking_hospital_id'] = hospital_id
    return redirect(url_for('appointment_select_doctor'))


@app.route('/appointment/select-doctor')
@login_required
@role_required('patient')
def appointment_select_doctor():
    hospital_id = session.get('booking_hospital_id')
    if not hospital_id:
        return redirect(url_for('appointment'))
    selected_hospital = find_hospital(hospital_id)
    doctors = get_hospital_doctors(hospital_id)
    return render_template(
        'appointment.html',
        step=2,
        selected_hospital=selected_hospital,
        doctors=doctors)


@app.route('/appointment/select-doctor', methods=['POST'])
@login_required
@role_required('patient')
def appointment_select_doctor_post():
    doctor_id = request.form.get('doctor_id')
    session['booking_doctor_id'] = doctor_id
    return redirect(url_for('appointment_date'))


@app.route('/appointment/date')
@login_required
@role_required('patient')
def appointment_date():
    hospital_id = session.get('booking_hospital_id')
    doctor_id = session.get('booking_doctor_id')
    if not hospital_id or not doctor_id:
        return redirect(url_for('appointment'))
    selected_hospital = find_hospital(hospital_id)
    selected_doctor = find_user_by_id(doctor_id)
    return render_template('appointment.html', step=3,
                           selected_hospital=selected_hospital,
                           selected_doctor=selected_doctor,
                           today=str(date.today()))


@app.route('/appointment/confirm', methods=['POST'])
@login_required
@role_required('patient')
def appointment_confirm():
    hospital_id = session.get('booking_hospital_id')
    doctor_id = session.get('booking_doctor_id')
    appt_date = request.form.get('date')
    slot = request.form.get('slot')

    if not all([hospital_id, doctor_id, appt_date, slot]):
        flash('Please complete all booking details.', 'error')
        return redirect(url_for('appointment'))

    # Check slot availability
    conflict = next((a for a in appointments if a['doctor_id'] == doctor_id and a['date']
                    == appt_date and a['slot'] == slot and a['status'] == 'booked'), None)
    if conflict:
        flash(
            f'The slot {slot} on {appt_date} is already booked. Please choose a different time.',
            'error')
        return redirect(url_for('appointment_date'))

    hospital = find_hospital(hospital_id)
    doctor = find_user_by_id(doctor_id)
    patient = find_user_by_id(session['user_id'])

    new_appt = {
        'id': str(uuid.uuid4())[:8],
        'patient_id': session['user_id'],
        'doctor_id': doctor_id,
        'hospital_id': hospital_id,
        'date': appt_date,
        'slot': slot,
        'status': 'booked',
        'patient_name': patient['name'] if patient else 'Unknown',
        'doctor_name': doctor['name'] if doctor else 'Unknown',
        'specialty': doctor.get('specialty', '') if doctor else '',
        'hospital_name': hospital['name'] if hospital else 'Unknown',
        'hospital_city': hospital['city'] if hospital else '',
        'patient_age': patient.get('age', '') if patient else '',
        'patient_gender': patient.get('gender', '') if patient else '',
    }
    appointments.append(new_appt)

    # Clear booking session state
    session.pop('booking_hospital_id', None)
    session.pop('booking_doctor_id', None)

    flash(
        f'✅ Appointment confirmed at {
            hospital["name"]} with {
            doctor["name"]} on {appt_date} at {slot}!',
        'success')
    return redirect(url_for('patient_appointments'))

# ============================================================
# DOCTOR ROUTES
# ============================================================


@app.route('/doctor/dashboard')
@login_required
@role_required('doctor')
def doctor_dashboard():
    doctor_id = session['user_id']
    today_str = str(date.today())
    all_appts = get_doctor_appointments(doctor_id)
    today_appts = [a for a in all_appts if a['date'] == today_str]

    stats = {
        'today_appointments': len(today_appts),
        'pending': sum(1 for a in all_appts if a['status'] == 'booked'),
        'completed': sum(1 for a in all_appts if a['status'] == 'completed'),
        'total': len(all_appts),
    }
    return render_template('doctor_dashboard.html',
                           stats=stats,
                           today_appointments=today_appts,
                           today_date=today_str)


@app.route('/doctor/appointments')
@login_required
@role_required('doctor')
def doctor_appointments():
    appts = sorted(
        get_doctor_appointments(
            session['user_id']),
        key=lambda a: a['date'],
        reverse=True)
    return render_template('doctor_appointments.html', appointments=appts)


@app.route('/doctor/prescribe', methods=['GET', 'POST'])
@login_required
@role_required('doctor')
def doctor_prescribe():
    appointment = None
    patient_history = []

    if request.method == 'POST':
        appt_id = request.form.get('appointment_id')
        patient_id = request.form.get('patient_id')
        diagnosis = request.form.get('diagnosis', '').strip()
        prescriptions = [
            p.strip() for p in request.form.get(
                'prescriptions',
                '').splitlines() if p.strip()]
        reports = [r.strip() for r in request.form.get(
            'reports', '').splitlines() if r.strip()]

        # Mark appointment completed
        for a in appointments:
            if a['id'] == appt_id:
                a['status'] = 'completed'
                doctor_name = a.get('doctor_name', session['name'])
                hospital_name = a.get('hospital_name', '')
                break
        else:
            doctor_name = session['name']
            hospital_name = ''

        record = {
            'id': str(uuid.uuid4())[:8],
            'patient_id': patient_id,
            'doctor_id': session['user_id'],
            'doctor_name': doctor_name,
            'hospital_name': hospital_name,
            'diagnosis': diagnosis,
            'prescriptions': prescriptions,
            'reports': reports,
            'date': str(date.today())
        }
        medical_records.append(record)
        flash('✅ Prescription saved and appointment marked as completed.', 'success')
        return redirect(url_for('doctor_prescribe'))

    # GET
    appt_id = request.args.get('appointment_id')
    if appt_id:
        appointment = next(
            (a for a in appointments if a['id'] == appt_id), None)
        if appointment:
            patient_history = get_patient_records(appointment['patient_id'])

    return render_template(
        'prescribe.html',
        appointment=appointment,
        patient_history=patient_history)

# ============================================================
# HOSPITAL ADMIN ROUTES
# ============================================================


@app.route('/admin/dashboard')
@login_required
@role_required('hospital_admin')
def admin_dashboard():
    admin = find_user_by_id(session['user_id'])
    hospital_id = admin.get('hospital_id', 'h1')
    hospital = find_hospital(hospital_id)
    doctors = get_hospital_doctors(hospital_id)
    appts = get_hospital_appointments(hospital_id)
    recent = sorted(appts, key=lambda a: a['date'], reverse=True)[:5]

    completed = [a for a in appts if a['status'] == 'completed']
    stats = {
        'doctors': len(doctors),
        'appointments': len(appts),
        'completed': len(completed),
        'revenue': len(completed) * (hospital['avg_cost'] if hospital else 100)
    }
    return render_template('admin_dashboard.html',
                           hospital=hospital, doctors=doctors,
                           recent_appointments=recent, stats=stats)


@app.route('/admin/doctors', methods=['GET', 'POST'])
@login_required
@role_required('hospital_admin')
def admin_doctors():
    admin = find_user_by_id(session['user_id'])
    hospital_id = admin.get('hospital_id', 'h1')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        specialty = request.form.get('specialty', 'General Medicine')
        avail_str = request.form.get('availability', '')
        availability = [d.strip() for d in avail_str.split(',') if d.strip()]

        if find_user(email):
            flash('A user with this email already exists.', 'error')
        else:
            new_doc = {
                'id': str(
                    uuid.uuid4())[
                    :8],
                'email': email,
                'name': name,
                'password': hash_password(password),
                'role': 'doctor',
                'specialty': specialty,
                'hospital_id': hospital_id,
                'availability': availability,
                'time_slots': [
                    '09:00 AM',
                    '10:00 AM',
                    '11:00 AM',
                    '02:00 PM',
                    '03:00 PM',
                    '04:00 PM']}
            users.append(new_doc)
            flash(f'Dr. {name} has been added successfully.', 'success')
        return redirect(url_for('admin_doctors'))

    doctors = get_hospital_doctors(hospital_id)
    hospital = find_hospital(hospital_id)
    return render_template(
        'admin_doctors.html',
        doctors=doctors,
        hospital=hospital)


@app.route('/admin/doctors/remove/<doc_id>', methods=['POST'])
@login_required
@role_required('hospital_admin')
def admin_remove_doctor(doc_id):
    global users
    users = [u for u in users if u['id'] != doc_id]
    flash('Doctor removed successfully.', 'success')
    return redirect(url_for('admin_doctors'))


@app.route('/admin/appointments')
@login_required
@role_required('hospital_admin')
def admin_appointments():
    admin = find_user_by_id(session['user_id'])
    hospital_id = admin.get('hospital_id', 'h1')
    appts = sorted(get_hospital_appointments(hospital_id),
                   key=lambda a: a['date'], reverse=True)
    return render_template('admin_appointments.html', appointments=appts)


@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
@role_required('hospital_admin')
def admin_profile():
    admin = find_user_by_id(session['user_id'])
    hospital_id = admin.get('hospital_id', 'h1')
    hospital = find_hospital(hospital_id)

    if request.method == 'POST':
        hospital['name'] = request.form.get('name', hospital['name'])
        hospital['city'] = request.form.get('city', hospital['city'])
        hospital['avg_cost'] = int(
            request.form.get(
                'avg_cost',
                hospital['avg_cost']))
        hospital['waiting_time'] = int(
            request.form.get(
                'waiting_time',
                hospital['waiting_time']))
        specs = request.form.get('specialty', '')
        hospital['specialty'] = [s.strip()
                                 for s in specs.split(',') if s.strip()]
        flash('Hospital profile updated successfully.', 'success')
        return redirect(url_for('admin_profile'))

    return render_template('admin_profile.html', hospital=hospital)

# ============================================================
# SUPER ADMIN ROUTES
# ============================================================


@app.route('/superadmin/dashboard')
@login_required
@role_required('super_admin')
def super_admin_dashboard():
    doctors = [u for u in users if u['role'] == 'doctor']
    patients = [u for u in users if u['role'] == 'patient']
    stats = {
        'hospitals': len(hospitals),
        'doctors': len(doctors),
        'patients': len(patients),
        'appointments': len(appointments)
    }
    return render_template('superadmin_dashboard.html',
                           hospitals=hospitals, stats=stats)


@app.route('/superadmin/add-hospital', methods=['POST'])
@login_required
@role_required('super_admin')
def superadmin_add_hospital():
    name = request.form.get('name', '').strip()
    city = request.form.get('city', '').strip()
    spec = request.form.get('specialty', '')
    cost = request.form.get('avg_cost', '100')
    wait = request.form.get('waiting_time', '20')
    rating = request.form.get('rating', '4.0')

    new_hosp = {
        'id': str(
            uuid.uuid4())[
            :8],
        'name': name,
        'city': city,
        'specialty': [
                s.strip() for s in spec.split(',') if s.strip()],
        'avg_cost': int(cost),
        'waiting_time': int(wait),
        'rating': float(rating),
        'available_specialists': []}
    hospitals.append(new_hosp)
    flash(f'{name} has been added to the network.', 'success')
    return redirect(url_for('super_admin_dashboard'))


@app.route('/superadmin/remove-hospital/<hid>', methods=['POST'])
@login_required
@role_required('super_admin')
def superadmin_remove_hospital(hid):
    global hospitals
    hospitals = [h for h in hospitals if h['id'] != hid]
    flash('Hospital removed from the network.', 'success')
    return redirect(url_for('super_admin_dashboard'))

# ============================================================
# ERROR HANDLERS
# ============================================================


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('404.html'), 403

# ============================================================
# RUN
# ============================================================


if __name__ == '__main__':
    app.run(debug=True, port=5000)
