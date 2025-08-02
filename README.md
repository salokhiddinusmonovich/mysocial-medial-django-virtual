# Virtual Social Network with Pinterest Parser and Real-time Chat

A full-featured social networking platform built with Django and Docker. It includes real-time chat via WebSockets, content parsing from Pinterest, and background task processing for email notifications. The project is deployed using Nginx and Docker Compose.

## 🔧 Tech Stack

- **Backend:** Django, Django Channels, Celery, Redis
- **Frontend:** HTML, Tailwind CSS, HTMX / Javascrip
- **Database:** PostgreSQL
- **Async Tasks:** Celery + Redis
- **Parsing:** Beautiful Soup (Pinterest content)
- **Deployment:** Docker, Docker Compose, Nginx, Gunicorn, Daphne 
- **Monitoring:** Flower (Celery dashboard)

## 💡 Features

- ✅ User registration and authentication
- ✅ Real-time chat using Django Channels and WebSockets
- ✅ Pinterest parser with Beautiful Soup (images, titles, etc.)
- ✅ Email notifications (e.g., new users) using Celery
- ✅ PostgreSQL for storing user data, chat history, and parsed content
- ✅ Task monitoring with Flower
- ✅ Production-ready deployment with Docker + Nginx

## 🌐 Live Demo

http://37.221.193.231/

> Note: Hosted on a personal VPS. Uptime not guaranteed.

## 🛠 Setup & Run (Docker)

```bash
git clone https:https://github.com/salokhiddinusmonovich/mysocial-medial-django-virtual.git
cd mysocial-medial-django-virtual

# Build and run all services
sudo docker compose -f docker-compose-yaml.prod up --build 
