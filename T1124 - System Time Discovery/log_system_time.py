import datetime
import os
import firebase_admin
from firebase_admin import credentials, db

# Path to your service account key
cred_path = os.path.join(os.path.dirname(__file__), 'CREDENTIAL FILE NAME HERE')  # Ensure this filename matches the JSON key

# Initialize Firebase
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cyberlog-6eb66-default-rtdb.europe-west1.firebasedatabase.app/'  # Replace with your database URL
})

# Get the current system time
current_time = datetime.datetime.now()

# Specify the log file path
log_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'log.txt')

# Write the current time to the log file
with open(log_file_path, 'a') as log_file:
    log_file.write(f"Current System Time: {current_time}\n")

# Write the current time and event to Firebase
ref = db.reference('logs')
new_log = ref.push({
    'event': 'System time discovery',
    'timestamp': str(current_time)
})

print("System time logged successfully.")
