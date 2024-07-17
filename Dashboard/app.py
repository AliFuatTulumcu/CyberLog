from flask import Flask, render_template, redirect, url_for, request, session
from firebase_admin import credentials, initialize_app, db
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'CREDENTIAL FILE NAME HERE'))
initialize_app(cred, {
    'databaseURL': 'https://cyberlog-6eb66-default-rtdb.europe-west1.firebasedatabase.app'
})

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    ref = db.reference('logs')
    logs = ref.get()

    if logs:
        log_entries = [{"event": log.get("event", "No event"), "timestamp": log.get("timestamp", "No timestamp")} for log in logs.values()]
    else:
        log_entries = []

    return render_template('dashboard.html', logs=log_entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
