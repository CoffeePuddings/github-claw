import os
import subprocess
import uuid
from datetime import datetime

from PIL import Image

from config import UPLOAD_FOLDER, OUTPUT_FOLDER
from database import get_db


def process_image(task_id, filepath, target_format, quality):
    """Compress or convert an image file."""
    db = get_db()
    try:
        img = Image.open(filepath)

        # Handle RGBA for formats that don't support it
        if target_format.lower() in ('jpg', 'jpeg') and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        output_name = f"{uuid.uuid4().hex}.{target_format}"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        save_kwargs = {}
        if target_format.lower() in ('jpg', 'jpeg'):
            save_kwargs['quality'] = quality or 75
            save_kwargs['optimize'] = True
        elif target_format.lower() == 'png':
            save_kwargs['optimize'] = True
        elif target_format.lower() == 'webp':
            save_kwargs['quality'] = quality or 80

        img.save(output_path, **save_kwargs)

        db.execute(
            'UPDATE tasks SET status=?, output_path=?, completed_at=? WHERE id=?',
            ('completed', output_path, datetime.now(), task_id)
        )
        db.commit()
        return output_path
    except Exception as e:
        db.execute(
            'UPDATE tasks SET status=?, error_message=? WHERE id=?',
            ('failed', str(e), task_id)
        )
        db.commit()
        raise
    finally:
        db.close()


def process_audio(task_id, filepath, target_format, quality):
    """Compress or convert an audio file using FFmpeg."""
    db = get_db()
    try:
        output_name = f"{uuid.uuid4().hex}.{target_format}"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        cmd = ['ffmpeg', '-y', '-i', filepath]

        if target_format.lower() == 'mp3':
            bitrate = f"{quality or 128}k"
            cmd.extend(['-b:a', bitrate])
        elif target_format.lower() == 'aac':
            bitrate = f"{quality or 128}k"
            cmd.extend(['-b:a', bitrate])
        elif target_format.lower() == 'ogg':
            q = min(10, max(0, (quality or 5)))
            cmd.extend(['-q:a', str(q)])
        elif target_format.lower() == 'wav':
            pass  # No compression for wav
        elif target_format.lower() == 'flac':
            cmd.extend(['-compression_level', '8'])

        cmd.append(output_path)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr[:500]}")

        db.execute(
            'UPDATE tasks SET status=?, output_path=?, completed_at=? WHERE id=?',
            ('completed', output_path, datetime.now(), task_id)
        )
        db.commit()
        return output_path
    except Exception as e:
        db.execute(
            'UPDATE tasks SET status=?, error_message=? WHERE id=?',
            ('failed', str(e), task_id)
        )
        db.commit()
        raise
    finally:
        db.close()


def process_video(task_id, filepath, target_format, quality):
    """Compress or convert a video file using FFmpeg."""
    db = get_db()
    try:
        output_name = f"{uuid.uuid4().hex}.{target_format}"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        cmd = ['ffmpeg', '-y', '-i', filepath]

        crf = quality or 23
        if target_format.lower() in ('mp4', 'mkv'):
            cmd.extend(['-c:v', 'libx264', '-crf', str(crf), '-preset', 'medium'])
            cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
        elif target_format.lower() == 'webm':
            cmd.extend(['-c:v', 'libvpx-vp9', '-crf', str(crf), '-b:v', '0'])
            cmd.extend(['-c:a', 'libopus', '-b:a', '128k'])
        elif target_format.lower() == 'avi':
            cmd.extend(['-c:v', 'mpeg4', '-q:v', str(max(1, min(31, crf)))])
            cmd.extend(['-c:a', 'mp3', '-b:a', '128k'])
        elif target_format.lower() == 'mov':
            cmd.extend(['-c:v', 'libx264', '-crf', str(crf)])
            cmd.extend(['-c:a', 'aac', '-b:a', '128k'])

        cmd.append(output_path)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr[:500]}")

        db.execute(
            'UPDATE tasks SET status=?, output_path=?, completed_at=? WHERE id=?',
            ('completed', output_path, datetime.now(), task_id)
        )
        db.commit()
        return output_path
    except Exception as e:
        db.execute(
            'UPDATE tasks SET status=?, error_message=? WHERE id=?',
            ('failed', str(e), task_id)
        )
        db.commit()
        raise
    finally:
        db.close()
