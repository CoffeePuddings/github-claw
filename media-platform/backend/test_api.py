"""
Automated test script for the Media Processing Platform backend.
Tests image, audio, and video processing flows.
"""
import os
import sys
import json
import tempfile
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import init_db

# Create test client
app.config['TESTING'] = True
client = app.test_client()


def create_test_image(path, width=100, height=100):
    """Create a simple test image using Pillow."""
    from PIL import Image
    img = Image.new('RGB', (width, height), color='red')
    img.save(path)


def create_test_audio(path, duration=2):
    """Create a simple test audio file using FFmpeg."""
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i',
        f'sine=frequency=440:duration={duration}',
        '-q:a', '9', path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def create_test_video(path, duration=2):
    """Create a simple test video file using FFmpeg."""
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i',
        f'testsrc=duration={duration}:size=320x240:rate=24',
        '-f', 'lavfi', '-i', f'sine=frequency=440:duration={duration}',
        '-c:v', 'libx264', '-c:a', 'aac', '-shortest', path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def test_health():
    """Test health endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    print("✅ Health check passed")


def test_image_processing():
    """Test image upload and conversion."""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        create_test_image(f.name)
        temp_path = f.name

    try:
        # Upload
        with open(temp_path, 'rb') as f:
            response = client.post('/api/upload', data={'file': (f, 'test.png')})
        assert response.status_code == 200
        upload_data = json.loads(response.data)
        assert upload_data['media_type'] == 'image'
        print(f"  ✅ Image upload: {upload_data['filename']} ({upload_data['file_size']} bytes)")

        # Process: PNG -> JPG
        response = client.post('/api/process', json={
            'stored_name': upload_data['stored_name'],
            'target_format': 'jpg',
            'quality': 75
        })
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['output_file'].endswith('.jpg')
        print(f"  ✅ PNG→JPG conversion: {result['input_size']}B → {result['output_size']}B ({result['compression_ratio']}%)")

        # Process: PNG -> WebP
        with open(temp_path, 'rb') as f:
            response = client.post('/api/upload', data={'file': (f, 'test.png')})
        upload_data = json.loads(response.data)

        response = client.post('/api/process', json={
            'stored_name': upload_data['stored_name'],
            'target_format': 'webp',
            'quality': 80
        })
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['output_file'].endswith('.webp')
        print(f"  ✅ PNG→WebP conversion: {result['input_size']}B → {result['output_size']}B ({result['compression_ratio']}%)")

        print("✅ Image processing tests passed")
    finally:
        os.unlink(temp_path)


def test_audio_processing():
    """Test audio upload and conversion."""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name

    if not create_test_audio(temp_path):
        print("⚠️  Skipping audio tests (FFmpeg not available or failed)")
        return

    try:
        # Upload
        with open(temp_path, 'rb') as f:
            response = client.post('/api/upload', data={'file': (f, 'test.wav')})
        assert response.status_code == 200
        upload_data = json.loads(response.data)
        assert upload_data['media_type'] == 'audio'
        print(f"  ✅ Audio upload: {upload_data['filename']} ({upload_data['file_size']} bytes)")

        # Process: WAV -> MP3
        response = client.post('/api/process', json={
            'stored_name': upload_data['stored_name'],
            'target_format': 'mp3',
            'quality': 128
        })
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['output_file'].endswith('.mp3')
        print(f"  ✅ WAV→MP3 conversion: {result['input_size']}B → {result['output_size']}B ({result['compression_ratio']}%)")

        # Process: WAV -> OGG
        with open(temp_path, 'rb') as f:
            response = client.post('/api/upload', data={'file': (f, 'test.wav')})
        upload_data = json.loads(response.data)

        response = client.post('/api/process', json={
            'stored_name': upload_data['stored_name'],
            'target_format': 'ogg',
            'quality': 5
        })
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['output_file'].endswith('.ogg')
        print(f"  ✅ WAV→OGG conversion: {result['input_size']}B → {result['output_size']}B ({result['compression_ratio']}%)")

        print("✅ Audio processing tests passed")
    finally:
        os.unlink(temp_path)


def test_video_processing():
    """Test video upload and conversion."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        temp_path = f.name

    if not create_test_video(temp_path):
        print("⚠️  Skipping video tests (FFmpeg not available or failed)")
        return

    try:
        # Upload
        with open(temp_path, 'rb') as f:
            response = client.post('/api/upload', data={'file': (f, 'test.mp4')})
        assert response.status_code == 200
        upload_data = json.loads(response.data)
        assert upload_data['media_type'] == 'video'
        print(f"  ✅ Video upload: {upload_data['filename']} ({upload_data['file_size']} bytes)")

        # Process: MP4 -> MKV
        response = client.post('/api/process', json={
            'stored_name': upload_data['stored_name'],
            'target_format': 'mkv',
            'quality': 28
        })
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['output_file'].endswith('.mkv')
        print(f"  ✅ MP4→MKV conversion: {result['input_size']}B → {result['output_size']}B ({result['compression_ratio']}%)")

        print("✅ Video processing tests passed")
    finally:
        os.unlink(temp_path)


def test_tasks_list():
    """Test tasks listing."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    tasks = json.loads(response.data)
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    print(f"✅ Tasks list: {len(tasks)} tasks found")


def test_download():
    """Test file download."""
    response = client.get('/api/download/nonexistent.jpg')
    assert response.status_code == 404
    print("✅ Download 404 test passed")


if __name__ == '__main__':
    print("=" * 50)
    print("🧪 Media Processing Platform - Backend Tests")
    print("=" * 50)

    init_db()

    test_health()
    print()
    print("--- Image Processing ---")
    test_image_processing()
    print()
    print("--- Audio Processing ---")
    test_audio_processing()
    print()
    print("--- Video Processing ---")
    test_video_processing()
    print()
    test_tasks_list()
    test_download()

    print()
    print("=" * 50)
    print("🎉 All tests passed!")
    print("=" * 50)
