from flask import Flask, render_template
from routes import file_organizer_routes
from scheduler import start_scheduler

app = Flask(__name__, static_folder="js")
start_scheduler()
app.register_blueprint(file_organizer_routes)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)