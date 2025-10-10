from flask import Flask, request, render_template, flash, jsonify, redirect, url_for
import os
import io
import base64
from filters import apply_filter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "2000sfiltersecret"

# 不再需要保存文件夹，所有处理都在内存中进行

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp','gif','tiff','tif','webp','avif','heif'}

# 更新 FILTERS 列表，新增9个爆款Y2K风格滤镜
FILTERS = ['ccd', 'vintage', 'kodachrome', 'fuji_superia', 'agfa', 'retro_green', 'dark_brown', 'lomo', 'dreamy', 'vhs', 'vaporwave', 'glitch', 'y2k', 'cyberpunk', 'neon_pop', 'digital_cam', 'cyber_pink', 'retro_blue', 'millennium_gold', 'matrix_green', 'disco_fever', 'tech_silver', 'y2k_purple', 'misty_gray', 'cloudy_dream', 'foggy_memory', 'silver_mist', 'dusty_film', 'hazy_night', 'soft_focus', 'vintage_blur', 'neon_glow', 'cyber_retro', 'synthwave', 'sepia_dust', 'polaroid_fade', 'chrome_shine', 'bubble_pop', 'glitch_art', 'holographic']

# 滤镜分类
FILTER_CATEGORIES = {
    'basic': ['ccd', 'vintage', 'lomo', 'dreamy', 'neon_glow', 'cyber_retro', 'synthwave'],
    'vintage': ['kodachrome', 'fuji_superia', 'agfa', 'retro_green', 'dark_brown', 'vhs', 'sepia_dust', 'polaroid_fade'],
    'y2k': ['y2k', 'cyberpunk', 'neon_pop', 'cyber_pink', 'y2k_purple', 'millennium_gold', 'chrome_shine', 'bubble_pop'],
    'effects': ['vaporwave', 'glitch', 'matrix_green', 'disco_fever', 'tech_silver', 'glitch_art', 'holographic'],
    'advanced': ['digital_cam', 'retro_blue', 'misty_gray', 'cloudy_dream', 'foggy_memory', 'silver_mist', 'dusty_film', 'hazy_night', 'soft_focus', 'vintage_blur']
}

# 全局变量保留上次的滤镜选择
LAST_FILTER = 'ccd'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    global LAST_FILTER

    if request.method == 'POST':
        filter_name = request.form.get('filter', LAST_FILTER)
        
        # 检查是否有文件上传
        file = request.files.get('image')
        
        if file and allowed_file(file.filename):
            try:
                # 读取文件数据到内存
                file_data = file.read()
                
                # 检查文件大小
                if len(file_data) == 0:
                    return jsonify({
                        'success': False,
                        'error': 'Uploaded file is empty, please select a valid image file'
                    })
                
                # 直接在内存中应用滤镜
                processed_data = apply_filter(file_data, filter_name)
                LAST_FILTER = filter_name
                
                # 将处理后的图片转换为base64编码
                processed_base64 = base64.b64encode(processed_data).decode('utf-8')
                
                # 返回JSON响应，包含base64图片数据
                return jsonify({
                    'success': True,
                    'filtered_image': f'data:image/jpeg;base64,{processed_base64}',
                    'filter_name': filter_name
                })
                
            except ValueError as e:
                # 用户输入错误（文件过大、格式不支持等）
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
            except Exception as e:
                # 其他处理错误
                return jsonify({
                    'success': False,
                    'error': f'Image processing failed: {str(e)}, please try a different image or contact support'
                })
        else:
            return jsonify({
                'success': False,
                'error': f'Please upload a valid image file! Supported formats: {", ".join(ALLOWED_EXTENSIONS)}'
            })
    
    return render_template('index.html', filters=FILTERS, selected_filter=LAST_FILTER, filter_categories=FILTER_CATEGORIES)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# 不再需要下载路由，图片直接通过主路由返回

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Railway 会注入 PORT，本地默认 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # host='0.0.0.0' 允许外部访问