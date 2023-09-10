# Django Chat Application

This is a Django-based chat application that allows users to create accounts, log in, view online users, start chats with online users, and send messages in real-time.

## Features

- User registration and authentication
- Viewing online users
- Initiating chats with online users
- Real-time messaging using WebSockets
- Friend recommendations based on interests

## Setup

1. Clone the repository.

```bash
git clone https://github.com/ibr03/django-chat-app.git
```

2. Create a virtual environment and install dependencies.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Apply migrations and create a super user
```
python manage.py migrate
python manage.py createsuperuser
```

4. Run development server
```
python manage.py runserver
```

## Usage
1. Visit http://localhost:8000/ to access the chat application.
2. Use the provided API endpoints for registration, login, and chat functionality (details in API documentation).
3. WebSocket connection is available at ws://localhost:8000/ws/chat/.

