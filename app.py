from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
import os

# Initialize Flask app
app = Flask(__name__)

# Azure Blob Storage Configuration
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=visiondetect;AccountKey=7kfPp3Yh7zo6w1ZSkl2NEBqGDoigjeDimk2S4FxXW/WTBuB79CMvqZcIwBq+lHewc/uWS8CAuxnU+AStS5qdcA==;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "test001"

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_azure(file, blob_name):
    """Upload file to Azure Blob Storage."""
    try:
        # Initialize Blob Service Client
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)
        
        # Upload file
        blob_client.upload_blob(file, overwrite=True)
        return blob_client.url
    except Exception as e:
        return str(e)

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
    """Handle file upload and store in Azure Blob Storage."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Determine file extension and create a new name
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"test001.{file_extension}"

        # Upload to Azure Blob Storage
        azure_url = upload_to_azure(file, new_filename)
        if azure_url.startswith("http"):
            return jsonify({"message": "File uploaded successfully", "download_url": azure_url})
        else:
            return jsonify({"error": "Failed to upload to Azure Blob Storage", "details": azure_url}), 500
    else:
        return jsonify({"error": "Invalid file type. Only Excel files are allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
