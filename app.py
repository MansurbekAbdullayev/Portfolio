import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'mansurbek_secret_portfolio_key_2026'

# Configure Uploads
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_CV_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database file
DATABASE = os.path.join(app.root_path, 'database.db')

# Helper functions for SQLite Database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def db_query(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def db_execute(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    row = db_query('SELECT * FROM admins WHERE id = ?', (user_id,), one=True)
    if row:
        return User(row['id'], row['username'])
    return None

# Allowed files validators
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_cv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_CV_EXTENSIONS

@app.before_request
def before_request():
    if 'lang' not in session:
        session['lang'] = 'uz'
    if request.args.get('lang') in ['en', 'uz', 'ru']:
        session['lang'] = request.args.get('lang')
    g.lang = session['lang']

TRANSLATIONS = {
    'en': {
        'home': 'Home', 'about': 'About', 'skills': 'Skills', 'services': 'Services',
        'projects': 'Projects', 'experience': 'Experience', 'contact': 'Contact',
        'admin_panel': 'Admin Portal', 'download_cv': 'Download CV', 'contact_me': 'Contact Me',
        'view_projects': 'View Projects', 'about_me': 'About Me', 'biography': 'Biography',
        'role': 'Role', 'location': 'Location', 'email': 'Email', 'telegram': 'Telegram',
        'projects_completed': 'Projects Completed', 'tech_learned': 'Tech Learned',
        'years_learning': 'Years of Learning', 'happy_clients': 'Happy Clients',
        'my_skills': 'My Skills', 'expertise': 'Expertise', 'offerings': 'Offerings',
        'my_services': 'My Services', 'portfolio': 'Portfolio', 'recent_projects': 'Recent Projects',
        'timeline': 'Timeline', 'exp_edu': 'Experience & Education', 'work_exp': 'Work Experience',
        'edu_cert': 'Education & Certification', 'get_in_touch': 'Get in Touch',
        'lets_talk': 'Let\'s talk', 'contact_desc': 'Have a project, a question, or a business proposition? Feel free to reach out. I will get back to you within 24 hours.',
        'email_address': 'Email Address', 'phone_number': 'Phone Number', 'workplace': 'Workplace',
        'available_remote': 'Available for Global Remote Work', 'send_message': 'Send Message',
        'name': 'Name', 'subject': 'Subject', 'message': 'Message', 'quick_links': 'Quick Links',
        'social_media': 'Social Media', 'all': 'All', 'featured': 'Featured',
        'quick_view': 'Quick View', 'project_details': 'Project Details', 'tech_used': 'Technologies Used',
        'view_github': 'View GitHub', 'closed_source': 'Closed Source', 'live_demo': 'Live Demo',
        'dashboard': 'Dashboard', 'messages': 'Messages', 'settings': 'Settings', 'view_site': 'View Site', 'sign_out': 'Sign Out'
    },
    'uz': {
        'home': 'Bosh sahifa', 'about': 'Haqimda', 'skills': 'Ko\'nikmalar', 'services': 'Xizmatlar',
        'projects': 'Loyihalar', 'experience': 'Tajriba', 'contact': 'Aloqa',
        'admin_panel': 'Admin Panel', 'download_cv': 'CV Yuklash', 'contact_me': 'Bog\'lanish',
        'view_projects': 'Loyihalarni Ko\'rish', 'about_me': 'Men Haqimda', 'biography': 'Biografiya',
        'role': 'Kasb', 'location': 'Manzil', 'email': 'Elektron pochta', 'telegram': 'Telegram',
        'projects_completed': 'Bajarilgan Loyihalar', 'tech_learned': 'O\'rganilgan Texnologiyalar',
        'years_learning': 'Yillik Tajriba', 'happy_clients': 'Mamnun Mijozlar',
        'my_skills': 'Mening Ko\'nikmalarim', 'expertise': 'Tajriba', 'offerings': 'Takliflar',
        'my_services': 'Mening Xizmatlarim', 'portfolio': 'Portfel', 'recent_projects': 'So\'nggi Loyihalar',
        'timeline': 'Vaqt shkalasi', 'exp_edu': 'Tajriba va Ta\'lim', 'work_exp': 'Ish Tajribasi',
        'edu_cert': 'Ta\'lim va Sertifikatlar', 'get_in_touch': 'Aloqaga Chiqing',
        'lets_talk': 'Keling, gaplashamiz', 'contact_desc': 'Loyihangiz, savolingiz yoki biznes taklifingiz bormi? Bemalol bog\'laning. Sizga tez orada javob beraman.',
        'email_address': 'Email Manzili', 'phone_number': 'Telefon Raqami', 'workplace': 'Ish Joyi',
        'available_remote': 'Masofadan ishlashga tayyorman', 'send_message': 'Xabar Jo\'natish',
        'name': 'Ism', 'subject': 'Mavzu', 'message': 'Xabar', 'quick_links': 'Tezkor Havolalar',
        'social_media': 'Ijtimoiy Tarmoqlar', 'all': 'Barchasi', 'featured': 'Tavsiya etilgan',
        'quick_view': 'Tezkor Ko\'rish', 'project_details': 'Loyiha Tafsilotlari', 'tech_used': 'Foydalanilgan Texnologiyalar',
        'view_github': 'GitHub-da Ko\'rish', 'closed_source': 'Yopiq Kodli', 'live_demo': 'Jonli Namoyish',
        'dashboard': 'Boshqaruv Paneli', 'messages': 'Xabarlar', 'settings': 'Sozlamalar', 'view_site': 'Saytni Ko\'rish', 'sign_out': 'Chiqish'
    },
    'ru': {
        'home': 'Главная', 'about': 'Обо мне', 'skills': 'Навыки', 'services': 'Услуги',
        'projects': 'Проекты', 'experience': 'Опыт', 'contact': 'Контакты',
        'admin_panel': 'Панель Админа', 'download_cv': 'Скачать резюме', 'contact_me': 'Связаться со мной',
        'view_projects': 'Смотреть Проекты', 'about_me': 'Обо мне', 'biography': 'Биография',
        'role': 'Должность', 'location': 'Место нахождения', 'email': 'Электронная почта', 'telegram': 'Телеграм',
        'projects_completed': 'Завершенные Проекты', 'tech_learned': 'Изученные Технологии',
        'years_learning': 'Годы Обучения', 'happy_clients': 'Довольные Клиенты',
        'my_skills': 'Мои Навыки', 'expertise': 'Экспертиза', 'offerings': 'Предложения',
        'my_services': 'Мои Услуги', 'portfolio': 'Портфолио', 'recent_projects': 'Недавние Проекты',
        'timeline': 'Хронология', 'exp_edu': 'Опыт и Образование', 'work_exp': 'Опыт Работы',
        'edu_cert': 'Образование и Сертификаты', 'get_in_touch': 'Связаться',
        'lets_talk': 'Давайте поговорим', 'contact_desc': 'Есть проект, вопрос или деловое предложение? Не стесняйтесь обращаться. Я отвечу вам в ближайшее время.',
        'email_address': 'Адрес электронной почты', 'phone_number': 'Номер Телефона', 'workplace': 'Место работы',
        'available_remote': 'Доступен для удаленной работы', 'send_message': 'Отправить Сообщение',
        'name': 'Имя', 'subject': 'Тема', 'message': 'Сообщение', 'quick_links': 'Быстрые ссылки',
        'social_media': 'Социальные сети', 'all': 'Все', 'featured': 'Рекомендуемые',
        'quick_view': 'Быстрый Просмотр', 'project_details': 'Детали Проекта', 'tech_used': 'Используемые Технологии',
        'view_github': 'Смотреть на GitHub', 'closed_source': 'Закрытый Исходный Код', 'live_demo': 'Демо',
        'dashboard': 'Панель управления', 'messages': 'Сообщения', 'settings': 'Настройки', 'view_site': 'Посмотреть Сайт', 'sign_out': 'Выйти'
    }
}

# Context processor to make site settings available globally in all templates
@app.context_processor
def inject_settings():
    try:
        rows = db_query('SELECT * FROM settings')
        settings_dict = {row['key']: row['value'] for row in rows}
    except Exception:
        settings_dict = {}
        
    def get_text(key):
        return TRANSLATIONS.get(getattr(g, 'lang', 'uz'), TRANSLATIONS['uz']).get(key, key)
        
    def get_db_field(obj, base_key):
        lang = getattr(g, 'lang', 'uz')
        if lang == 'en':
            return obj[base_key]
        lang_key = f"{base_key}_{lang}"
        if lang_key in obj.keys() and obj[lang_key]:
             return obj[lang_key]
        return obj[base_key]
        
    return dict(settings=settings_dict, t=get_text, tf=get_db_field, current_lang=getattr(g, 'lang', 'uz'))

def check_and_add_column(db, table, column, type_="TEXT"):
    try:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type_}")
        db.commit()
    except sqlite3.OperationalError:
        pass

# Initialize Database Schema & Default Records
def init_db():
    with app.app_context():
        db = get_db()
        
        # Create Tables
        db.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                percentage INTEGER NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_url TEXT NOT NULL,
                tech_stack TEXT NOT NULL,
                github_url TEXT,
                demo_url TEXT,
                category TEXT NOT NULL,
                is_featured INTEGER DEFAULT 0
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company_or_institution TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        
        # Migrations for Multilingual support
        check_and_add_column(db, 'skills', 'name_uz')
        check_and_add_column(db, 'skills', 'name_ru')
        check_and_add_column(db, 'skills', 'category_uz')
        check_and_add_column(db, 'skills', 'category_ru')
        
        check_and_add_column(db, 'services', 'title_uz')
        check_and_add_column(db, 'services', 'title_ru')
        check_and_add_column(db, 'services', 'description_uz')
        check_and_add_column(db, 'services', 'description_ru')
        
        check_and_add_column(db, 'projects', 'title_uz')
        check_and_add_column(db, 'projects', 'title_ru')
        check_and_add_column(db, 'projects', 'description_uz')
        check_and_add_column(db, 'projects', 'description_ru')
        check_and_add_column(db, 'projects', 'category_uz')
        check_and_add_column(db, 'projects', 'category_ru')
        
        check_and_add_column(db, 'experiences', 'title_uz')
        check_and_add_column(db, 'experiences', 'title_ru')
        check_and_add_column(db, 'experiences', 'company_or_institution_uz')
        check_and_add_column(db, 'experiences', 'company_or_institution_ru')
        check_and_add_column(db, 'experiences', 'description_uz')
        check_and_add_column(db, 'experiences', 'description_ru')
        
        # Check and insert initial Admin Account
        admin_exists = db.execute('SELECT * FROM admins WHERE username = ?', ('admin',)).fetchone()
        if not admin_exists:
            hashed_pwd = generate_password_hash('mansurbekblog2010')
            db.execute('INSERT INTO admins (username, password) VALUES (?, ?)', ('admin', hashed_pwd))
            db.commit()
            print("Initial admin account created: admin / mansurbekblog2010")

        # Check and insert default Settings
        settings_count = db.execute('SELECT count(*) FROM settings').fetchone()[0]
        if settings_count == 0:
            default_settings = {
                'hero_title': 'Mansurbek Abdullayev',
                'hero_title_uz': 'Mansurbek Abdullayev',
                'hero_title_ru': 'Мансурбек Абдуллаев',
                'hero_subtitle': 'Full Stack Developer',
                'hero_subtitle_uz': 'Full Stack Dasturchi',
                'hero_subtitle_ru': 'Full Stack Разработчик',
                'hero_description': 'I design and build premium, clean, and production-quality software applications that solve real-world problems. Specialized in Python, SQL, modern web systems, and custom automation tools.',
                'hero_description_uz': 'Men real muammolarni hal qiluvchi premium, toza va ishlab chiqarish sifatidagi dasturiy ilovalarni loyihalashtiraman va quraman.',
                'hero_description_ru': 'Я проектирую и создаю премиальные, чистые и качественные программные приложения, которые решают реальные проблемы.',
                'about_bio': 'I am a highly motivated Full Stack Python Developer with a passion for crafting elegant, performant, and premium user experiences. I specialize in building robust backend microservices, structuring reliable databases, and developing clean front-end interfaces.',
                'about_bio_uz': 'Men nafis, samarali va yuqori darajadagi foydalanuvchi tajribasini yaratishga ishtiyoqi bor yuqori motivatsiyali Full Stack Python dasturchisiman.',
                'about_bio_ru': 'Я высокомотивированный Full Stack Python разработчик, страстно увлеченный созданием элегантного, производительного и премиального пользовательского опыта.',
                'email': 'mansurbek.dev@example.com',
                'phone': '+998 90 123 45 67',
                'telegram': 'mansurbek_dev',
                'instagram': 'mansurbek_dev',
                'github': 'mansurbek-dev',
                'linkedin': 'mansurbek-dev',
                'location': 'Tashkent, Uzbekistan',
                'location_uz': 'Toshkent, O\'zbekiston',
                'location_ru': 'Ташкент, Узбекистан',
                'workplace': 'DevStudio',
                'workplace_map_url': 'https://maps.google.com/?q=Tashkent',
                'cv_url': '',
                'profile_image': '',
                'stats_projects': '12+',
                'stats_tech': '15+',
                'stats_years': '4+',
                'stats_clients': '10+'
            }
            for k, v in default_settings.items():
                db.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
            db.commit()
            print("Default site settings populated.")
        else:
            # Ensure new keys exist if updating
            new_keys = {'workplace': 'DevStudio', 'workplace_map_url': 'https://maps.google.com/?q=Tashkent'}
            for k, v in new_keys.items():
                db.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
            db.commit()

        # Check and insert default Skills
        skills_count = db.execute('SELECT count(*) FROM skills').fetchone()[0]
        if skills_count == 0:
            default_skills = [
                ('HTML', 95, 'Frontend'),
                ('CSS', 90, 'Frontend'),
                ('Tailwind CSS', 95, 'Frontend'),
                ('JavaScript', 85, 'Frontend'),
                ('Python', 95, 'Backend'),
                ('PHP', 80, 'Backend'),
                ('Laravel', 75, 'Backend'),
                ('Golang', 70, 'Backend'),
                ('C++', 65, 'Backend'),
                ('SQL', 90, 'Database'),
                ('MySQL', 90, 'Database'),
                ('Git and GitHub', 85, 'Other')
            ]
            for name, pct, cat in default_skills:
                db.execute('INSERT INTO skills (name, percentage, category) VALUES (?, ?, ?)', (name, pct, cat))
            db.commit()
            print("Default skills populated.")

        # Check and insert default Services
        services_count = db.execute('SELECT count(*) FROM services').fetchone()[0]
        if services_count == 0:
            default_services = [
                ('Frontend Website Development', 'Building pixel-perfect, interactive, and responsive user interfaces with smooth scrolling and elegant transitions.', 'code'),
                ('Backend Development', 'Developing scalable APIs, high-performance microservices, and secure servers in Python, Go, and PHP.', 'server'),
                ('Telegram Bot Development', 'Creating intelligent, fast, and feature-rich automated bots for customer service, CRM, and task automation.', 'send'),
                ('CRM System Development', 'Designing comprehensive custom business systems with databases, dashboards, and role management.', 'cpu'),
                ('Responsive Web Design', 'Crafting user-centric mobile and desktop layouts with a focus on modern typography and black-and-white minimalist themes.', 'monitor'),
                ('Database Design', 'Architecting robust, query-optimized SQL databases with SQLite, PostgreSQL, or MySQL.', 'database'),
                ('API Development', 'Creating clean, documented RESTful API endpoints for seamless integrations with front-ends and mobile apps.', 'link')
            ]
            for title, desc, icon in default_services:
                db.execute('INSERT INTO services (title, description, icon) VALUES (?, ?, ?)', (title, desc, icon))
            db.commit()
            print("Default services populated.")

        # Check and insert default Experiences if empty
        exp_count = db.execute('SELECT count(*) FROM experiences').fetchone()[0]
        if exp_count == 0:
            default_exp = [
                ('Senior Full Stack Developer', 'Freelance / DevStudio', '2023', 'Present', 'Building bespoke web systems, CRM dashboards, and API integrations for client projects.', 'work'),
                ('Python Backend Engineer', 'Tech Incubator', '2022', '2023', 'Engineered custom automation pipelines and Telegram bot infrastructure.', 'work'),
                ('Full Stack Web Development Certification', 'IT Academy Tashkent', '2021', '2022', 'Intensive training on Python, Flask, Django, SQL databases, and JavaScript frameworks.', 'education'),
                ('Software Engineering Degree', 'State Technical University', '2019', '2023', 'Completed Bachelor of Science in Software Engineering, focusing on databases and object-oriented design.', 'education')
            ]
            for title, company, sdate, edate, desc, type_ in default_exp:
                db.execute('INSERT INTO experiences (title, company_or_institution, start_date, end_date, description, type) VALUES (?, ?, ?, ?, ?, ?)', (title, company, sdate, edate, desc, type_))
            db.commit()
            print("Default experiences populated.")

# ================= PUBLIC ROUTES =================

@app.route('/')
def index():
    # Load all settings, skills, services, projects, experiences
    skills = db_query('SELECT * FROM skills')
    services = db_query('SELECT * FROM services')
    
    # Sort projects, featured ones first, followed by others
    projects = db_query('SELECT * FROM projects ORDER BY is_featured DESC, id DESC')
    
    experiences = db_query('SELECT * FROM experiences ORDER BY end_date DESC, start_date DESC')
    
    # Organize skills by category
    categorized_skills = {}
    for skill in skills:
        cat = skill['category']
        if cat not in categorized_skills:
            categorized_skills[cat] = []
        categorized_skills[cat].append(skill)
        
    return render_template('index.html', 
                           skills=categorized_skills, 
                           services=services, 
                           projects=projects, 
                           experiences=experiences)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not email or not subject or not message:
        flash('All fields are required.', 'danger')
        return redirect(url_for('index', _anchor='contact'))
        
    try:
        db_execute(
            'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
            (name, email, subject, message)
        )
        flash('Thank you! Your message has been sent successfully.', 'success')
    except Exception as e:
        flash('An error occurred. Please try again.', 'danger')
        print(f"Error saving message: {e}")
        
    return redirect(url_for('index', _anchor='contact'))

# ================= AUTH ROUTES =================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        row = db_query('SELECT * FROM admins WHERE username = ?', (username,), one=True)
        if row and check_password_hash(row['password'], password):
            user = User(row['id'], row['username'])
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

# ================= ADMIN ROUTES =================

@app.route('/admin')
@login_required
def admin():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Gather counts
    project_count = db_query('SELECT count(*) FROM projects', one=True)[0]
    skill_count = db_query('SELECT count(*) FROM skills', one=True)[0]
    service_count = db_query('SELECT count(*) FROM services', one=True)[0]
    unread_messages = db_query('SELECT count(*) FROM messages WHERE is_read = 0', one=True)[0]
    
    # Get recent activities: latest unread messages and projects
    recent_messages = db_query('SELECT * FROM messages ORDER BY id DESC LIMIT 5')
    recent_projects = db_query('SELECT * FROM projects ORDER BY id DESC LIMIT 3')
    
    return render_template('admin/dashboard.html',
                           project_count=project_count,
                           skill_count=skill_count,
                           service_count=service_count,
                           unread_messages=unread_messages,
                           recent_messages=recent_messages,
                           recent_projects=recent_projects)

# Projects CRUD
@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = db_query('SELECT * FROM projects ORDER BY id DESC')
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def project_add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        title_uz = request.form.get('title_uz', '').strip()
        title_ru = request.form.get('title_ru', '').strip()
        description = request.form.get('description', '').strip()
        description_uz = request.form.get('description_uz', '').strip()
        description_ru = request.form.get('description_ru', '').strip()
        tech_stack = request.form.get('tech_stack', '').strip()
        github_url = request.form.get('github_url', '').strip()
        demo_url = request.form.get('demo_url', '').strip()
        category = request.form.get('category', '').strip()
        category_uz = request.form.get('category_uz', '').strip()
        category_ru = request.form.get('category_ru', '').strip()
        is_featured = 1 if request.form.get('is_featured') else 0
        
        image_file = request.files.get('image_file')
        image_url = ''
        
        if image_file and allowed_image(image_file.filename):
            filename = secure_filename(image_file.filename)
            import time
            filename = f"{int(time.time())}_{filename}"
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f'uploads/{filename}'
        else:
            flash('Please upload a valid image file (png, jpg, jpeg, gif, webp).', 'danger')
            return render_template('admin/project_form.html', project=None, title="Add Project")

        db_execute(
            '''INSERT INTO projects (title, title_uz, title_ru, description, description_uz, description_ru, image_url, tech_stack, github_url, demo_url, category, category_uz, category_ru, is_featured) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (title, title_uz, title_ru, description, description_uz, description_ru, image_url, tech_stack, github_url, demo_url, category, category_uz, category_ru, is_featured)
        )
        flash('Project added successfully.', 'success')
        return redirect(url_for('admin_projects'))
        
    return render_template('admin/project_form.html', project=None, title="Add Project")

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    project = db_query('SELECT * FROM projects WHERE id = ?', (id,), one=True)
    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('admin_projects'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        title_uz = request.form.get('title_uz', '').strip()
        title_ru = request.form.get('title_ru', '').strip()
        description = request.form.get('description', '').strip()
        description_uz = request.form.get('description_uz', '').strip()
        description_ru = request.form.get('description_ru', '').strip()
        tech_stack = request.form.get('tech_stack', '').strip()
        github_url = request.form.get('github_url', '').strip()
        demo_url = request.form.get('demo_url', '').strip()
        category = request.form.get('category', '').strip()
        category_uz = request.form.get('category_uz', '').strip()
        category_ru = request.form.get('category_ru', '').strip()
        is_featured = 1 if request.form.get('is_featured') else 0
        
        image_file = request.files.get('image_file')
        image_url = project['image_url']
        
        if image_file and image_file.filename != '':
            if allowed_image(image_file.filename):
                filename = secure_filename(image_file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f'uploads/{filename}'
            else:
                flash('Please upload a valid image file (png, jpg, jpeg, gif, webp).', 'danger')
                return render_template('admin/project_form.html', project=project, title="Edit Project")
                
        db_execute(
            '''UPDATE projects SET title = ?, title_uz = ?, title_ru = ?, description = ?, description_uz = ?, description_ru = ?, image_url = ?, tech_stack = ?, github_url = ?, demo_url = ?, category = ?, category_uz = ?, category_ru = ?, is_featured = ?
               WHERE id = ?''',
            (title, title_uz, title_ru, description, description_uz, description_ru, image_url, tech_stack, github_url, demo_url, category, category_uz, category_ru, is_featured, id)
        )
        flash('Project updated successfully.', 'success')
        return redirect(url_for('admin_projects'))
        
    return render_template('admin/project_form.html', project=project, title="Edit Project")

@app.route('/admin/projects/delete/<int:id>', methods=['POST'])
@login_required
def project_delete(id):
    project = db_query('SELECT * FROM projects WHERE id = ?', (id,), one=True)
    if project:
        # Optionally delete actual image file from folder
        try:
            image_path = os.path.join(app.root_path, 'static', project['image_url'])
            if os.path.exists(image_path) and project['image_url']:
                os.remove(image_path)
        except Exception as e:
            print(f"Failed to delete project image file: {e}")
            
        db_execute('DELETE FROM projects WHERE id = ?', (id,))
        flash('Project deleted successfully.', 'success')
    else:
        flash('Project not found.', 'danger')
    return redirect(url_for('admin_projects'))

# Skills CRUD
@app.route('/admin/skills', methods=['GET'])
@login_required
def admin_skills():
    skills = db_query('SELECT * FROM skills ORDER BY category, percentage DESC')
    return render_template('admin/skills.html', skills=skills, current_skill=None)

@app.route('/admin/skills/add', methods=['POST'])
@login_required
def skill_add():
    name = request.form.get('name', '').strip()
    name_uz = request.form.get('name_uz', '').strip()
    name_ru = request.form.get('name_ru', '').strip()
    percentage = int(request.form.get('percentage', 0))
    category = request.form.get('category', '').strip()
    category_uz = request.form.get('category_uz', '').strip()
    category_ru = request.form.get('category_ru', '').strip()
    
    if name and percentage and category:
        db_execute('INSERT INTO skills (name, name_uz, name_ru, percentage, category, category_uz, category_ru) VALUES (?, ?, ?, ?, ?, ?, ?)', (name, name_uz, name_ru, percentage, category, category_uz, category_ru))
        flash('Skill added successfully.', 'success')
    else:
        flash('Please fill in all fields correctly.', 'danger')
    return redirect(url_for('admin_skills'))

@app.route('/admin/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def skill_edit(id):
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        name_uz = request.form.get('name_uz', '').strip()
        name_ru = request.form.get('name_ru', '').strip()
        percentage = int(request.form.get('percentage', 0))
        category = request.form.get('category', '').strip()
        category_uz = request.form.get('category_uz', '').strip()
        category_ru = request.form.get('category_ru', '').strip()
        if name and percentage and category:
            db_execute('UPDATE skills SET name = ?, name_uz = ?, name_ru = ?, percentage = ?, category = ?, category_uz = ?, category_ru = ? WHERE id = ?', (name, name_uz, name_ru, percentage, category, category_uz, category_ru, id))
            flash('Skill updated successfully.', 'success')
            return redirect(url_for('admin_skills'))
        else:
            flash('Invalid inputs.', 'danger')
            
    # If GET, edit inline
    skills = db_query('SELECT * FROM skills ORDER BY category, percentage DESC')
    current_skill = db_query('SELECT * FROM skills WHERE id = ?', (id,), one=True)
    return render_template('admin/skills.html', skills=skills, current_skill=current_skill)

@app.route('/admin/skills/delete/<int:id>', methods=['POST'])
@login_required
def skill_delete(id):
    db_execute('DELETE FROM skills WHERE id = ?', (id,))
    flash('Skill deleted successfully.', 'success')
    return redirect(url_for('admin_skills'))

# Services CRUD
@app.route('/admin/services', methods=['GET'])
@login_required
def admin_services():
    services = db_query('SELECT * FROM services ORDER BY id DESC')
    return render_template('admin/services.html', services=services, current_service=None)

@app.route('/admin/services/add', methods=['POST'])
@login_required
def service_add():
    title = request.form.get('title', '').strip()
    title_uz = request.form.get('title_uz', '').strip()
    title_ru = request.form.get('title_ru', '').strip()
    description = request.form.get('description', '').strip()
    description_uz = request.form.get('description_uz', '').strip()
    description_ru = request.form.get('description_ru', '').strip()
    icon = request.form.get('icon', '').strip()
    
    if title and description and icon:
        db_execute('INSERT INTO services (title, title_uz, title_ru, description, description_uz, description_ru, icon) VALUES (?, ?, ?, ?, ?, ?, ?)', (title, title_uz, title_ru, description, description_uz, description_ru, icon))
        flash('Service added successfully.', 'success')
    else:
        flash('Please fill all fields.', 'danger')
    return redirect(url_for('admin_services'))

@app.route('/admin/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def service_edit(id):
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        title_uz = request.form.get('title_uz', '').strip()
        title_ru = request.form.get('title_ru', '').strip()
        description = request.form.get('description', '').strip()
        description_uz = request.form.get('description_uz', '').strip()
        description_ru = request.form.get('description_ru', '').strip()
        icon = request.form.get('icon', '').strip()
        if title and description and icon:
            db_execute('UPDATE services SET title = ?, title_uz = ?, title_ru = ?, description = ?, description_uz = ?, description_ru = ?, icon = ? WHERE id = ?', (title, title_uz, title_ru, description, description_uz, description_ru, icon, id))
            flash('Service updated successfully.', 'success')
            return redirect(url_for('admin_services'))
        else:
            flash('Invalid inputs.', 'danger')
            
    services = db_query('SELECT * FROM services ORDER BY id DESC')
    current_service = db_query('SELECT * FROM services WHERE id = ?', (id,), one=True)
    return render_template('admin/services.html', services=services, current_service=current_service)

@app.route('/admin/services/delete/<int:id>', methods=['POST'])
@login_required
def service_delete(id):
    db_execute('DELETE FROM services WHERE id = ?', (id,))
    flash('Service deleted successfully.', 'success')
    return redirect(url_for('admin_services'))

# Experience CRUD
@app.route('/admin/experience', methods=['GET'])
@login_required
def admin_experience():
    experiences = db_query('SELECT * FROM experiences ORDER BY end_date DESC, start_date DESC')
    return render_template('admin/experience.html', experiences=experiences, current_exp=None)

@app.route('/admin/experience/add', methods=['POST'])
@login_required
def experience_add():
    title = request.form.get('title', '').strip()
    title_uz = request.form.get('title_uz', '').strip()
    title_ru = request.form.get('title_ru', '').strip()
    company = request.form.get('company_or_institution', '').strip()
    company_uz = request.form.get('company_or_institution_uz', '').strip()
    company_ru = request.form.get('company_or_institution_ru', '').strip()
    start_date = request.form.get('start_date', '').strip()
    end_date = request.form.get('end_date', '').strip()
    description = request.form.get('description', '').strip()
    description_uz = request.form.get('description_uz', '').strip()
    description_ru = request.form.get('description_ru', '').strip()
    exp_type = request.form.get('type', '').strip()
    
    if title and company and start_date and end_date and description and exp_type:
        db_execute(
            '''INSERT INTO experiences (title, title_uz, title_ru, company_or_institution, company_or_institution_uz, company_or_institution_ru, start_date, end_date, description, description_uz, description_ru, type) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (title, title_uz, title_ru, company, company_uz, company_ru, start_date, end_date, description, description_uz, description_ru, exp_type)
        )
        flash('Timeline item added successfully.', 'success')
    else:
        flash('Please fill in all fields.', 'danger')
    return redirect(url_for('admin_experience'))

@app.route('/admin/experience/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def experience_edit(id):
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        title_uz = request.form.get('title_uz', '').strip()
        title_ru = request.form.get('title_ru', '').strip()
        company = request.form.get('company_or_institution', '').strip()
        company_uz = request.form.get('company_or_institution_uz', '').strip()
        company_ru = request.form.get('company_or_institution_ru', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        description = request.form.get('description', '').strip()
        description_uz = request.form.get('description_uz', '').strip()
        description_ru = request.form.get('description_ru', '').strip()
        exp_type = request.form.get('type', '').strip()
        
        if title and company and start_date and end_date and description and exp_type:
            db_execute(
                '''UPDATE experiences SET title = ?, title_uz = ?, title_ru = ?, company_or_institution = ?, company_or_institution_uz = ?, company_or_institution_ru = ?, start_date = ?, end_date = ?, description = ?, description_uz = ?, description_ru = ?, type = ?
                   WHERE id = ?''',
                (title, title_uz, title_ru, company, company_uz, company_ru, start_date, end_date, description, description_uz, description_ru, exp_type, id)
            )
            flash('Timeline item updated successfully.', 'success')
            return redirect(url_for('admin_experience'))
        else:
            flash('Invalid inputs.', 'danger')
            
    experiences = db_query('SELECT * FROM experiences ORDER BY end_date DESC, start_date DESC')
    current_exp = db_query('SELECT * FROM experiences WHERE id = ?', (id,), one=True)
    return render_template('admin/experience.html', experiences=experiences, current_exp=current_exp)

@app.route('/admin/experience/delete/<int:id>', methods=['POST'])
@login_required
def experience_delete(id):
    db_execute('DELETE FROM experiences WHERE id = ?', (id,))
    flash('Timeline item deleted successfully.', 'success')
    return redirect(url_for('admin_experience'))

# Messages
@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = db_query('SELECT * FROM messages ORDER BY id DESC')
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/read/<int:id>', methods=['POST'])
@login_required
def message_read(id):
    msg = db_query(
        'SELECT is_read FROM messages WHERE id = ?',
        (id,),
        one=True
    )

    if msg:
        new_status = 1 if msg['is_read'] == 0 else 0
        db_execute(
            'UPDATE messages SET is_read = ? WHERE id = ?',
            (new_status, id)
        )
        flash('Message status updated.', 'success')

    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/delete/<int:id>', methods=['POST'])
@login_required
def message_delete(id):
    db_execute('DELETE FROM messages WHERE id = ?', (id,))
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin_messages'))

# Site Settings
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        # Text fields
        keys = [
            'hero_title', 'hero_title_uz', 'hero_title_ru',
            'hero_subtitle', 'hero_subtitle_uz', 'hero_subtitle_ru',
            'hero_description', 'hero_description_uz', 'hero_description_ru',
            'about_bio', 'about_bio_uz', 'about_bio_ru',
            'email', 'phone', 'telegram', 'instagram', 'github', 'linkedin', 
            'location', 'location_uz', 'location_ru',
            'workplace', 'workplace_map_url',
            'stats_projects', 'stats_tech', 'stats_years', 'stats_clients'
        ]
        for key in keys:
            val = request.form.get(key, '').strip()
            # use INSERT OR REPLACE strategy or explicit UPDATE
            db_execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, val))
            
        # CV file upload
        cv_file = request.files.get('cv_file')
        if cv_file and cv_file.filename != '':
            if allowed_cv(cv_file.filename):
                filename = secure_filename(cv_file.filename)
                import time
                filename = f"cv_{int(time.time())}_{filename}"
                cv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db_execute('UPDATE settings SET value = ? WHERE key = ?', (f'uploads/{filename}', 'cv_url'))
            else:
                flash('Please upload a valid CV document (pdf, doc, docx).', 'danger')
                
        # Profile image file upload
        profile_file = request.files.get('profile_image')
        if profile_file and profile_file.filename != '':
            if allowed_image(profile_file.filename):
                filename = secure_filename(profile_file.filename)
                import time
                filename = f"profile_{int(time.time())}_{filename}"
                profile_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db_execute('UPDATE settings SET value = ? WHERE key = ?', (f'uploads/{filename}', 'profile_image'))
            else:
                flash('Please upload a valid profile image (png, jpg, jpeg, gif, webp).', 'danger')

        # Password update section
        current_pwd = request.form.get('current_password', '')
        new_pwd = request.form.get('new_password', '')
        confirm_pwd = request.form.get('confirm_password', '')
        
        if new_pwd != '':
            # Verify current password
            row = db_query('SELECT password FROM admins WHERE username = ?', (current_user.username,), one=True)
            if row and check_password_hash(row['password'], current_pwd):
                if new_pwd == confirm_pwd:
                    hashed_new = generate_password_hash(new_pwd)
                    db_execute('UPDATE admins SET password = ? WHERE id = ?', (hashed_new, current_user.id))
                    flash('Admin settings and password updated successfully.', 'success')
                else:
                    flash('New passwords do not match. Other settings saved.', 'warning')
            else:
                flash('Incorrect current password. Other settings saved.', 'warning')
        else:
            flash('Settings updated successfully.', 'success')
            
        return redirect(url_for('admin_settings'))
        
    return render_template('admin/settings.html')

# Custom 404 Error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_page=True), 404

if __name__ == '__main__':
    # Initialize the tables and initial admin account
    init_db()
    
    # Run server
    app.run(debug=True, host='0.0.0.0', port=5000)
