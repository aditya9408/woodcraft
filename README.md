# 🪵 WoodCraft — Carpentry Business Website

> A full-stack Django monolithic web application built for a carpentry business based in Surat, Gujarat, India.

**🌐 Live Site:** [woodcraft.up.railway.app](https://woodcraft.up.railway.app)  
**📦 Repository:** [github.com/aditya9408/woodcraft](https://github.com/aditya9408/woodcraft)

---

## 📸 Overview

WoodCraft is a production-ready business website built for a master carpenter to showcase his work, attract clients, and manage inquiries — all through a clean Django admin panel. Built as a real-world portfolio project demonstrating end-to-end Django development, cloud deployment, and third-party integrations.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 6, Python 3.13 |
| **Database** | MySQL (Railway) |
| **Frontend** | Vanilla HTML / CSS / JS |
| **Media Storage** | Cloudinary |
| **Static Files** | WhiteNoise |
| **Email** | Brevo SMTP |
| **Deployment** | Railway |
| **Version Control** | GitHub |

---

## 🏗️ Architecture

```
                    ┌──────────────────────────┐
                    │         Browser           │
                    └────────────┬─────────────┘
                                 │ HTTPS
                    ┌────────────▼─────────────┐
                    │       Railway CDN          │
                    │  woodcraft.up.railway.app  │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │    Gunicorn WSGI Server    │
                    │        2 Workers           │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │        Django App          │
                    │                           │
                    │   ┌───────────────────┐   │
                    │   │    URL Router     │   │
                    │   └────────┬──────────┘   │
                    │            │              │
                    │   ┌────────▼──────────┐   │
                    │   │      Views        │   │
                    │   │  home / projects  │   │
                    │   │  about / contact  │   │
                    │   │  project_detail   │   │
                    │   └────────┬──────────┘   │
                    │            │              │
                    │   ┌────────▼──────────┐   │
                    │   │      Models       │   │
                    │   │  Project          │   │
                    │   │  ProjectCategory  │   │
                    │   │  ProjectImage     │   │
                    │   │  Testimonial      │   │
                    │   │  ContactMessage   │   │
                    │   └────────┬──────────┘   │
                    └────────────┼─────────────┘
                                 │
          ┌──────────────────────┼─────────────────────┐
          │                      │                      │
┌─────────▼────────┐  ┌─────────▼────────┐  ┌────────▼─────────┐
│  Railway MySQL    │  │   Cloudinary     │  │   Brevo SMTP     │
│  (Database)       │  │   (Media Files)  │  │   (Email)        │
│  Projects         │  │   Project Photos │  │   Contact Form   │
│  Contacts etc.    │  │   Gallery Images │  │   Notifications  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## ✨ Features

### Public Pages
- **Home** — Hero, services grid, featured projects, about snippet, testimonials, contact form
- **Projects** — Full project listing with live category filter
- **Project Detail** — Full description, image gallery, related projects
- **About** — Company story, stats, workshop location, client testimonials
- **Contact** — Form with First Name, Last Name, Phone, Subject, Description

### Admin Panel (`/admin/`)
- Add / edit projects with cover image and gallery images
- Manage project categories for filtering
- Toggle featured projects displayed on the home page
- View contact messages with status (New / Read / Replied / Archived)
- Add / edit client testimonials with star ratings

### Technical Highlights
- ✅ Auto-slug generation from title with duplicate handling
- ✅ Image auto-compression to JPEG 75% and max 1200px on upload
- ✅ Email notification to admin on every contact form submission
- ✅ Cloudinary media storage — images persist across every redeploy
- ✅ Fully responsive — mobile, tablet, desktop
- ✅ Environment-based configuration — no secrets in code

---

## 📁 Project Structure

```
woodcraft/
├── woodcraft/                  # Django project config
│   ├── settings.py             # All settings, fully env-based
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py
│
├── core/                       # Main application
│   ├── models.py               # Models with auto-slug + image compression
│   ├── views.py                # Page views + email notification helper
│   ├── urls.py                 # App URL patterns
│   ├── forms.py                # ContactForm (ModelForm)
│   ├── admin.py                # Admin configuration with fieldsets
│   │
│   ├── templates/core/
│   │   ├── base.html           # Base layout — navbar + footer
│   │   ├── home.html           # Home page
│   │   ├── projects.html       # Projects listing with filter
│   │   ├── project_detail.html # Individual project page
│   │   ├── about.html          # About page
│   │   └── contact.html        # Contact page
│   │
│   └── static/core/
│       ├── css/style.css       # All styles — warm wood colour palette
│       └── js/main.js          # Mobile nav toggle + flash messages
│
├── requirements.txt
├── Procfile                    # Railway start command
├── railway.json                # Railway build config
├── .env.example                # Environment variable template
└── manage.py
```

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/aditya9408/woodcraft.git
cd woodcraft

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in your values

# 5. Run migrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in your values:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `MYSQLDATABASE` | MySQL database name |
| `MYSQLHOST` | MySQL host address |
| `MYSQLUSER` | MySQL username |
| `MYSQLPASSWORD` | MySQL password |
| `MYSQLPORT` | MySQL port (default 3306) |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `EMAIL_HOST` | SMTP host (Brevo: `smtp-relay.brevo.com`) |
| `EMAIL_HOST_USER` | SMTP login email |
| `EMAIL_HOST_PASSWORD` | SMTP password / API key |
| `CONTACT_RECIPIENT_EMAIL` | Email address to receive contact messages |

---

## 🚀 Deployment

Deployed on **Railway** with automatic deploys on every GitHub push.

| Service | Provider |
|---|---|
| Web App | Railway (Gunicorn) |
| Database | Railway MySQL |
| Media Files | Cloudinary |
| Static Files | WhiteNoise middleware |
| Email | Brevo SMTP |

### Deploy your own
1. Fork this repo
2. Create a new project on [railway.app](https://railway.app)
3. Connect your GitHub repo
4. Add a MySQL service
5. Set all environment variables in Railway dashboard
6. Deploy — Railway handles the rest

---

## 🗄️ Data Models

```
ProjectCategory          Project
─────────────────        ─────────────────────────────
id                       id
name                     title
slug (auto)              slug (auto-generated)
                         category (FK → ProjectCategory)
                         short_description
                         description
                         cover_image (→ Cloudinary)
                         is_featured
                         order
                         created_at

ProjectImage             Testimonial
─────────────────        ─────────────────────────────
id                       id
project (FK)             author_name
image (→ Cloudinary)     author_initials
caption                  quote
order                    rating
                         is_active
                         order

ContactMessage
─────────────────────────────
id
first_name / last_name
phone_number
subject / description
status (New/Read/Replied/Archived)
admin_notes
created_at
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built by **Aditya Vishwakarma** · [GitHub](https://github.com/aditya9408)*