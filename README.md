# Phishing Awareness Demo (Flask)

Educational demo that shows how phishing pages can look like and why users should verify URLs.
**This project does NOT collect real credentials and does NOT log keystrokes.**

## Features
- Simple login-like UI for awareness training
- Demonstration flow: submit -> educational warning
- Local-only Flask app

## Tech Stack
- Python
- Flask

## Run locally (Windows)
### 1) Create & activate venv
python -m venv venv
.\venv\Scripts\activate

2) Install dependencies
pip install -r requirements.txt

3) Run the app
python app.py

Open: http://127.0.0.1:5001/
