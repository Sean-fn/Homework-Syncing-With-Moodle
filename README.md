# Homework Syncing With Moodle
This is a web application that can sync homework from Moodle to **Google Calendar** and **Google Task**. Inculding details and updates of submission status.

GR8 tool for students to manage their homework.

## Still under development

### Platform Support

| Platform | Support |
| - | - |
| Google Calendar | Yes |
| Google Task | No |
| Web Dashboard | No |

### School Support

| School | Support |
| - | - |
| CUTe | Yes |

Currently only support CUTe Moodle, I will add more school support in the future.

## Prerequisite
- Python 3.9 or above
- Moodle Account
- Google API Credentials, if you don't have one, please follow the steps below
    1. Go to [Google Cloud Platform](https://console.cloud.google.com/projectcreate) and create a new project.
    2. In the [Google API Console](https://console.cloud.google.com/apis/dashboard) for your project, enable the "Google Calendar API" and "Google Tasks API".
    3. In the [Google API Console](https://console.cloud.google.com/apis/credentials) , create OAuth client credentials with the "Desktop client" type.
    4. Copy the credentials to `GOOGLE_CREDENTIALS=` in your .env file


## How to use
1. Clone this repo
2. Install all the dependencies
3. Create a .env file in the root directory
4. Fill in the .env file with the following information
```
# .env
FLASK_SECRET_KEY='qUstuk-3wyfta-xyswuf'     # Generate a random string
FLASK_DEBUG='True'
DATABASE_URL='sqlite:///app/db/user_info.db'

GOOGLE_CREDENTIALS='Your_Google_API_Credentials:json'
```
5. Run the app
```
flask run
```
or
```
docker-compose up -f docker/docker-compose.yml
```

---
## Directory Structure
```
my-app/
├─ wigs.py
├─ .env_example
├─ LICENSE
├─ Procfile
├─ app.py
├─ .gitignore
├─ requirement.txt
├─ README.md
├─ frontend/
│  ├─ static/
│  │  ├─ js/
│  │  │  ├─ bold-and-dark
│  │  ├─ web/
│  │  │  ├─ js/
│  │  │  │  ├─ web.min.js
│  │  │  ├─ css/
│  │  │  │  ├─ web.min.css
│  ├─ templates/
│  │  ├─ delete.html
│  │  ├─ signup.html
├─ flask_api/
│  ├─ database/
│  │  ├─ models.py
│  ├─ common/
│  │  ├─ utils.py
│  ├─ __init__.py
│  ├─ config.py
├─ merge_data/
│  ├─ google_calendar/
│  │  ├─ g_calendar.py
│  │  ├─ g_task.py
│  ├─ common/
│  │  ├─ utils.py
│  ├─ Moodle_scraper/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ scraper.py
│  │  ├─ moodle.py
│  ├─ __init__.py
├─ main/
│  ├─ dbUtils.py
│  ├─ login_utils.py
│  ├─ routes.py
```
