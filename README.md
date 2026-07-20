# 🏥 MediBridge AI

**MediBridge AI** is an intelligent, multi-role healthcare platform built with Python (Flask) that connects patients with the right doctors and hospitals using AI-assisted symptom analysis and smart recommendations.

---

## 🌟 Key Features

### 🧑‍⚕️ Multi-Role Architecture
- **Patient Portal:** Book appointments, manage medical records, and search for hospitals/doctors.
- **Doctor Dashboard:** Manage appointments, prescribe medications, and view patient history.
- **Hospital Admin:** Manage hospital staff, doctors, and overview institutional appointments.
- **Superadmin:** Oversee the entire platform, manage all hospitals, and system metrics.

### 🤖 AI-Powered Recommendations
- **Symptom Matching:** Patients can input their symptoms, and the system intelligently matches them with the correct medical specialty (e.g., Cardiology, Neurology).
- **Smart Ranking:** Hospitals are recommended and ranked based on available specialists, average cost, waiting times, and overall ratings.

### 📅 Seamless Appointments
- Find doctors by specialty, location, or hospital.
- Book, reschedule, or cancel appointments.
- Real-time slot availability.

---

## 🛠️ Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, Jinja2 Templates (Vanilla CSS for maximum flexibility and performance)
- **Data Store:** In-memory structures (Ready to be integrated with SQL/NoSQL databases)

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hema-supriya-01/medibridge.git
   cd medibridge
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

---

## 🔐 Default Test Accounts

You can use the following credentials to test different user roles:

| Role | Email | Password |
|------|-------|----------|
| **Patient** | `patient@medibridge.com` | `password` |
| **Doctor** | `doctor@medibridge.com` | `password` |
| **Admin** | `admin@medibridge.com` | `password` |
| **Superadmin** | `superadmin@medibridge.com` | `password` |

---

## 📂 Project Structure

```
medibridge/
│
├── backend/
│   ├── app.py                  # Main Flask application and routing
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── static/
│   │   ├── style.css           # Global styles and UI tokens
│   │   └── script.js           # Client-side interactivity
│   │
│   └── templates/              # Jinja2 HTML templates
│       ├── index.html
│       ├── dashboard.html
│       ├── ai_recommend.html
│       └── ...
│
└── README.md                   # Project documentation
```

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
