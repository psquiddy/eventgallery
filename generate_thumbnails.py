import os
from PIL import Image
from moviepy.editor import VideoFileClip
import io

# Paths
UPLOAD_FOLDER = 'static/uploads'
THUMBNAIL_FOLDER = 'static/thumbnails'

# Ensure the thumbnail folder exists
if not os.path.exists(THUMBNAIL_FOLDER):
    os.makedirs(THUMBNAIL_FOLDER)

def create_image_thumbnail(image_path):
    with Image.open(image_path) as img:
        # Rotate image if needed
        if img._exif.get(274) == 6:  # Check orientation tag for 90-degree rotation
            img = img.rotate(-90, expand=True)
        elif img._exif.get(274) == 8:  # Check orientation tag for -90-degree rotation
            img = img.rotate(90, expand=True)
        
        img.thumbnail((200, 200))
        thumbnail_path = os.path.join(THUMBNAIL_FOLDER, os.path.basename(image_path))
        img.save(thumbnail_path)

def create_video_thumbnail(video_path):
    with VideoFileClip(video_path) as video:
        # Extract a frame
        frame = video.get_frame(0)
        image = Image.fromarray(frame)
        
        # Rotate image if needed
        image = image.rotate(-90, expand=True)  # Adjust as necessary based on your needs
        
        image.thumbnail((200, 200))
        thumbnail_path = os.path.join(THUMBNAIL_FOLDER, os.path.basename(video_path) + '.jpg')
        image.save(thumbnail_path, 'JPEG')

def process_files():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            create_image_thumbnail(file_path)
        elif filename.lower().endswith(('mp4', 'mov')):
            create_video_thumbnail(file_path)

if __name__ == '__main__':
    process_files()
