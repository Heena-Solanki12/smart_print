import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
# This allows your React app to send requests without CORS errors
CORS(app)

# Directory where the Pi will save uploaded files
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/status', methods=['GET'])
def check_status():
    # Mock printer status. You can update this later to read real printer status
    return jsonify({
        "online": True, 
        "ready": True, 
        "status": "Waiting for jobs"
    })

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
            # Prefix the filename with the Job ID to keep things organized
            save_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")
            file.save(save_path)
            saved_files.append(filename)
            
    # ---> Here is where you would trigger the actual physical printer <---
            
    return jsonify({
        "success": True, 
        "jobId": job_id, 
        "filesReceived": saved_files
    }), 200

if __name__ == '__main__':
    # host='0.0.0.0' allows it to be accessed from your local network (10.110.40.42)
    app.run(host='0.0.0.0', port=5000)
