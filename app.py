from flask import Flask, request, render_template, send_from_directory, after_this_request
import os
import subprocess
import threading
import time


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'mp3'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(CONVERTED_FOLDER):
    os.makedirs(CONVERTED_FOLDER)

def allowed_file(filename, file_type):
    if file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    elif file_type in ['video']:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS
    else:
        return False

def delayed_file_deletion(filepath, delay):
    """Delete a file after a delay in seconds."""
    time.sleep(delay)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            app.logger.info(f"Deleted file: {filepath}")
    except Exception as e:
        app.logger.error(f"Error deleting file: {filepath}, Error: {e}")


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Determine file type
    file_type = ''
    if allowed_file(file.filename, 'image'):
        file_type = 'image'
    elif allowed_file(file.filename, 'video'):
        file_type = 'video'
    else:
        return 'File type not allowed'

    # Save the file
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Get selected format
    selected_format = request.form.get('format')

    # Convert the file using FFmpeg or handle image conversion
    if file_type == 'image':
        if selected_format in ALLOWED_IMAGE_EXTENSIONS:
            # Convert the image using FFmpeg
            converted_filename = f"{filename.rsplit('.', 1)[0]}.{selected_format}"
            converted_filepath = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
            subprocess.call(['ffmpeg', '-y', '-i', filepath, converted_filepath])
        else:
            return 'Invalid image format selected'
    elif file_type == 'video':
        if selected_format in ALLOWED_VIDEO_EXTENSIONS:
            # Convert the video using FFmpeg
            converted_filename = f"{filename.rsplit('.', 1)[0]}.{selected_format}"
            converted_filepath = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
            subprocess.call(['ffmpeg', '-y', '-i', filepath, converted_filepath])
        else:
            return 'Invalid video format selected'
    else:
        return 'File type not supported'

        # Delete the uploaded file after conversion and before sending the converted file
    @after_this_request
    def remove_uploaded_file(response):
        try:
            os.remove(filepath)
            app.logger.info(f"Deleted uploaded file: {filepath}")
        except Exception as error:
            app.logger.error(f"Error removing uploaded file: {filepath}, Error: {error}")
        return response

    # Schedule the converted file for deletion after 1 minute
    threading.Thread(target=delayed_file_deletion, args=(converted_filepath, 60)).start()

    return send_from_directory(app.config['CONVERTED_FOLDER'], converted_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5006, debug=True)
