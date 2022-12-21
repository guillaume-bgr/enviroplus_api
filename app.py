# save this as app.py
from flask import Flask, request
from markupsafe import escape
from main_process import main_process

app = Flask(__name__)

@app.route('/')
def get_temp_sample():
    main_process()

if __name__ == '__main__':
    app.run(port=5002)