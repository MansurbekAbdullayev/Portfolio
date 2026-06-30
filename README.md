# Mansurbek Abdullayev Portfolio Website

A complete, production-quality personal developer portfolio website featuring a secure administrator dashboard panel. 

## Technology Stack
- **Backend Framework**: Python Flask
- **Database System**: SQLite
- **Authentication**: Flask-Login
- **Password Encryption**: Werkzeug password hashing
- **Styling Core**: Tailwind CSS (via CDN) & Custom Vanilla CSS
- **Interactivity**: Vanilla JavaScript & Jinja2 Templates
- **Media Uploads**: Safe file upload filters for images and CV documents

---

## Workspace Structure
```text
portfolio/
│ app.py
│ database.db
│ requirements.txt
│ README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── admin/
│   │   ├── base_admin.html
│   │   ├── dashboard.html
│   │   ├── projects.html
│   │   ├── project_form.html
│   │   ├── skills.html
│   │   ├── services.html
│   │   ├── messages.html
│   │   ├── settings.html
│   │   └── experience.html
│
└── static/
    ├── css/
    │   └── main.css
    ├── js/
    │   └── main.js
    └── uploads/
```

---

## Setup & Running Locally

Follow these quick commands to spin up the portfolio locally:

### 1. Install Dependencies
Run the command below to download and install Flask, Flask-Login, and Werkzeug:
```bash
pip install -r requirements.txt
```

### 2. Run the Application
Start the Flask application using standard python execution:
```bash
python app.py
```

### 3. Open in Browser
Visit `http://127.0.0.1:5000` inside your browser to view the portfolio.

---

## Admin Portal Authentication

The system automatically initializes an administrator credentials row when booting for the first time.

- **Login URL**: `/login` (or click "Admin Panel" in the header)
- **Initial Username**: `admin`
- **Initial Password**: `mansurbekblog2010`

> [!WARNING]
> Please change the administrator credentials on the **Settings** page immediately after logging in for security.

---

## Key Features

### Public Website
- **Sticky Navbar**: Header locks on scroll with section anchors tracking.
- **Hero & About**: Code mockup visual card, numeric stat indicators, and professional resume descriptors.
- **Dynamic Skills & Services**: Sorted dynamically from database query.
- **Projects Grid**: Category filter tabs, custom card zoom tags, and quick-look modal overlay.
- **Timeline Events**: Standardised experience timeline for work and academic history.
- **Contact Form**: SQLite validation logging, alert notifications, and map placeholder coordinates.

### Admin Dashboard (Authenticated)
- **Dashboard Summary**: Real-time stats count block and activity checklists.
- **Projects CRUD**: Multi-field form featuring inline image replacements.
- **Skills CRUD**: Percentage indicator sliders and category toggles.
- **Services CRUD**: Card description logs and icon options.
- **Timeline CRUD**: Work/Education card updates.
- **Contact Inbox**: Mark as read filters and deletion utilities.
- **Global Settings**: Update hero texts, social link extensions, profile pictures, CV documents, and admin passwords.
