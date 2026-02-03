from flask import Flask, request, render_template, flash, jsonify, redirect, url_for
import os
import sys
import io
import base64

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filters import apply_filter
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "2000sfiltersecret"

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp','gif','tiff','tif','webp','avif','heif'}

FILTERS = ['ccd', 'vintage', 'kodachrome', 'fuji_superia', 'agfa', 'retro_green', 'dark_brown', 'lomo', 'dreamy', 'vhs', 'vaporwave', 'glitch', 'y2k', 'cyberpunk', 'neon_pop', 'digital_cam', 'cyber_pink', 'retro_blue', 'millennium_gold', 'matrix_green', 'disco_fever', 'tech_silver', 'y2k_purple', 'misty_gray', 'cloudy_dream', 'foggy_memory', 'silver_mist', 'dusty_film', 'hazy_night', 'soft_focus', 'vintage_blur', 'neon_glow', 'cyber_retro', 'synthwave', 'sepia_dust', 'polaroid_fade', 'chrome_shine', 'bubble_pop', 'glitch_art', 'holographic', 'electric_blue', 'neon_pink', 'cyber_green', 'retro_orange', 'film_grain', 'aged_paper', 'metallic_silver', 'neon_cyan', 'digital_noise', 'rainbow_shift']

FILTER_CATEGORIES = {
    'basic': ['ccd', 'vintage', 'lomo', 'dreamy', 'neon_glow', 'cyber_retro', 'synthwave', 'electric_blue', 'neon_pink', 'cyber_green', 'retro_orange'],
    'vintage': ['kodachrome', 'fuji_superia', 'agfa', 'retro_green', 'dark_brown', 'vhs', 'sepia_dust', 'polaroid_fade', 'film_grain', 'aged_paper'],
    'y2k': ['y2k', 'cyberpunk', 'neon_pop', 'cyber_pink', 'y2k_purple', 'millennium_gold', 'chrome_shine', 'bubble_pop', 'metallic_silver', 'neon_cyan'],
    'effects': ['vaporwave', 'glitch', 'matrix_green', 'disco_fever', 'tech_silver', 'glitch_art', 'holographic', 'digital_noise', 'rainbow_shift'],
    'advanced': ['digital_cam', 'retro_blue', 'misty_gray', 'cloudy_dream', 'foggy_memory', 'silver_mist', 'dusty_film', 'hazy_night', 'soft_focus', 'vintage_blur']
}

LAST_FILTER = 'ccd'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    global LAST_FILTER

    if request.method == 'POST':
        filter_name = request.form.get('filter', LAST_FILTER)
        
        file = request.files.get('image')
        
        if file and allowed_file(file.filename):
            try:
                file_data = file.read()
                
                if len(file_data) == 0:
                    return jsonify({
                        'success': False,
                        'error': 'Uploaded file is empty, please select a valid image file'
                    })
                
                processed_data = apply_filter(file_data, filter_name)
                LAST_FILTER = filter_name
                
                processed_base64 = base64.b64encode(processed_data).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'filtered_image': f'data:image/jpeg;base64,{processed_base64}',
                    'filter_name': filter_name
                })
                
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
            except Exception as e:
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
