from flask import Flask, render_template
from routes import file_organizer_routes
from scheduler import start_scheduler
import webbrowser
import threading

app = Flask(__name__, static_folder="js")
start_scheduler()
app.register_blueprint(file_organizer_routes)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start() # Opens browser after 1.5 sec
    app.run(debug=False, use_reloader=False)
    