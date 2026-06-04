import os
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER, OUTPUT_FOLDER, MAX_CONTENT_LENGTH
from database import init_db, get_db
from processors import process_image, process_audio, process_video

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
CORS(app)

IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma'}
VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'webm', 'flv', 'wmv'}


def get_media_type(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext in IMAGE_EXTENSIONS:
        return 'image'
    elif ext in AUDIO_EXTENSIONS:
        return 'audio'
    elif ext in VIDEO_EXTENSIONS:
        return 'video'
    return None


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Media Processing Platform is running'})


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    media_type = get_media_type(file.filename)
    if not media_type:
        return jsonify({'error': 'Unsupported file type'}), 400

    # Save uploaded file
    original_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{original_name}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    file_size = os.path.getsize(filepath)

    return jsonify({
        'message': 'File uploaded successfully',
        'filename': original_name,
        'stored_name': unique_name,
        'media_type': media_type,
        'file_size': file_size
    })


@app.route('/api/process', methods=['POST'])
def process_file():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    stored_name = data.get('stored_name')
    target_format = data.get('target_format')
    quality = data.get('quality')
    operation = data.get('operation', 'convert')

    if not stored_name or not target_format:
        return jsonify({'error': 'stored_name and target_format are required'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, stored_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    # Determine media type
    media_type = get_media_type(stored_name)
    if not media_type:
        return jsonify({'error': 'Cannot determine media type'}), 400

    # Create task record
    db = get_db()
    cursor = db.execute(
        'INSERT INTO tasks (filename, original_path, media_type, operation, target_format, quality, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (stored_name, filepath, media_type, operation, target_format, quality, 'processing')
    )
    task_id = cursor.lastrowid
    db.commit()
    db.close()

    # Process the file
    try:
        if media_type == 'image':
            output_path = process_image(task_id, filepath, target_format, quality)
        elif media_type == 'audio':
            output_path = process_audio(task_id, filepath, target_format, quality)
        elif media_type == 'video':
            output_path = process_video(task_id, filepath, target_format, quality)
        else:
            return jsonify({'error': 'Unsupported media type'}), 400

        output_size = os.path.getsize(output_path)
        input_size = os.path.getsize(filepath)

        return jsonify({
            'message': 'Processing completed',
            'task_id': task_id,
            'output_file': os.path.basename(output_path),
            'input_size': input_size,
            'output_size': output_size,
            'compression_ratio': round(output_size / input_size * 100, 2) if input_size > 0 else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(OUTPUT_FOLDER, secure_filename(filename))
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath, as_attachment=True)


@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks ORDER BY created_at DESC LIMIT 50').fetchall()
    db.close()
    return jsonify([dict(t) for t in tasks])


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    db.close()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(dict(task))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
