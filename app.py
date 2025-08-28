from flask import Flask, request, render_template, flash, send_from_directory, redirect, url_for
import os
from filters import apply_filter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "2000sfiltersecret"

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp','gif'}

# 更新 FILTERS 列表，新增爆款滤镜
FILTERS = ['ccd', 'vintage', 'film', 'kodachrome', 'fuji_superia', 'agfa', 'retro_green', 'sepia', 'dark_brown', 'lomo', 'dreamy', 'vhs', 'bw', 'vaporwave', 'glitch', 'y2k']

# 全局变量保留上次上传的图片和滤镜
LAST_ORIGINAL = None
LAST_PROCESSED = None
LAST_FILTER = 'ccd'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    global LAST_ORIGINAL, LAST_PROCESSED, LAST_FILTER

    if request.method == 'POST':
        filter_name = request.form.get('filter', LAST_FILTER)
        
        # 检查是否有新的文件上传
        file = request.files.get('image')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            LAST_ORIGINAL = filename
            LAST_PROCESSED = None
            flash("Image uploaded successfully!") # 图片上传成功后立即清除提示

        # 如果没有新文件上传且没有历史图片，则提示用户
        elif not LAST_ORIGINAL:
            flash("Please upload an image first!")
            return render_template('index.html', original=LAST_ORIGINAL, processed=LAST_PROCESSED, filters=FILTERS, selected_filter=LAST_FILTER)
        
        # 应用滤镜
        processed_path = apply_filter(os.path.join(UPLOAD_FOLDER, LAST_ORIGINAL), filter_name)
        LAST_PROCESSED = os.path.basename(processed_path)
        LAST_FILTER = filter_name

    return render_template('index.html', original=LAST_ORIGINAL, processed=LAST_PROCESSED, filters=FILTERS, selected_filter=LAST_FILTER)

@app.route('/download/<filename>')
def download(filename):
    """提供处理后的图片供用户下载"""
    # 确保文件存在且在处理后的文件夹中
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)