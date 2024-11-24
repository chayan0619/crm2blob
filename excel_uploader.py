from flask import Flask, request, send_from_directory, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    """Home route with upload instructions."""
    return '''
    <h1>Excel File Uploader</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xls,.xlsx">
        <button type="submit">Upload</button>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and provide download link."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Determine file extension
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"test001.{file_extension}"

        # Save the file with the new name
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)

        # Generate download URL
        download_url = f"http://127.0.0.1:5000/download/{new_filename}"
        return jsonify({"message": "File uploaded successfully", "download_url": download_url})
    else:
        return jsonify({"error": "Invalid file type. Only Excel files are allowed"}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Serve the renamed file for download."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
