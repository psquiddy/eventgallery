import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from moviepy.editor import VideoFileClip

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
THUMBNAIL_FOLDER = 'static/thumbnails'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['THUMBNAIL_FOLDER'], exist_ok=True)

def allowed_file(filename):
    # Check if file extension is allowed (case-insensitive)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_VIDEO_EXTENSIONS)

def create_image_thumbnail(image_path, thumbnail_path):
    """Creates a thumbnail for an image."""
    try:
        with Image.open(image_path) as img:
            img.thumbnail((200, 200))
            img.save(thumbnail_path)
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")

def create_video_thumbnail(video_path, thumbnail_path):
    """Creates a thumbnail for a video."""
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(0)  # Get the first frame
        img = Image.fromarray(frame)
        img.thumbnail((200, 200))
        img.save(thumbnail_path)
        clip.reader.close()
        clip.close()
    except Exception as e:
        print(f"Error creating thumbnail for {video_path}: {e}")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files and 'video' not in request.files:
            return redirect(request.url)
        
        # Handle image upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Create a thumbnail for images
                if filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
                    thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
                    create_image_thumbnail(file_path, thumbnail_path)
        
        # Handle video upload
        if 'video' in request.files:
            video = request.files['video']
            if video and allowed_file(video.filename):
                filename = secure_filename(video.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video.save(video_path)

                # Create a thumbnail for videos
                if filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS:
                    thumbnail_name = filename.rsplit('.', 1)[0] + '.png'
                    thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_name)
                    create_video_thumbnail(video_path, thumbnail_path)
        
        return redirect(url_for('upload_file'))
    
    # List images and videos
    images = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    videos = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.lower().endswith(('mp4', 'mov'))]
    
    return render_template('index.html', images=images, videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
