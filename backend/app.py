# Save this on your Pi as app.py
# Install requirements: pip install flask flask-cors
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Allow your React app to talk to this Pi server
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/status', methods=['GET'])
def check_status():
    # In the real app, this would check the physical printer state (e.g., via CUPS)
    return jsonify({"online": True, "ready": True, "status": "Waiting for jobs"})

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'files' not in request.files:
        return jsonify({"error": "No files attached"}), 400
        
    job_id = request.form.get('jobId', 'unknown_job')
    files = request.files.getlist('files')
    
    saved_files = []
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            # You might want to save them in folders grouped by jobId
            save_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")
            file.save(save_path)
            saved_files.append(filename)
            
    # Here you would trigger the actual printing process...
            
    return jsonify({"success": True, "jobId": job_id, "filesReceived": saved_files}), 200

if __name__ == '__main__':
    # Listen on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
