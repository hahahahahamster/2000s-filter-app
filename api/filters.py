from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import random
import io
import logging

# 尝试导入HEIF/AVIF支持
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_SUPPORT = True
    logging.info("HEIF/AVIF support enabled")
except ImportError:
    HEIF_SUPPORT = False
    logging.info("pillow-heif not available, HEIF/AVIF support disabled")
except Exception as e:
    HEIF_SUPPORT = False
    logging.warning(f"Error initializing HEIF support: {e}")

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 图片处理配置
MAX_IMAGE_SIZE = (4096, 4096)  # 最大支持4K图片
MAX_FILE_SIZE = 50 * 1024 * 1024  # 最大文件大小50MB
SUPPORTED_FORMATS = ['JPEG', 'PNG', 'BMP', 'GIF', 'TIFF', 'WEBP', 'AVIF', 'HEIF']

def validate_image(image_data):
    """验证图片数据"""
    try:
        # 检查文件大小
        if len(image_data) > MAX_FILE_SIZE:
            return False, f"Image file too large ({len(image_data) / (1024*1024):.1f}MB), maximum supported: {MAX_FILE_SIZE / (1024*1024):.0f}MB"
        
        # 尝试打开图片
        img = Image.open(io.BytesIO(image_data))
        
        # 检查图片格式
        if img.format not in SUPPORTED_FORMATS:
            # 如果没有HEIF支持，但格式是HEIF/AVIF，给出特殊提示
            if img.format in ['HEIF', 'AVIF'] and not HEIF_SUPPORT:
                return False, f"HEIF/AVIF format detected but pillow-heif not installed. Please install: pip install pillow-heif"
            return False, f"Unsupported image format ({img.format}), supported formats: {', '.join(SUPPORTED_FORMATS)}"
        
        # 检查图片尺寸
        if img.size[0] > MAX_IMAGE_SIZE[0] or img.size[1] > MAX_IMAGE_SIZE[1]:
            return False, f"Image dimensions too large ({img.size[0]}x{img.size[1]}), maximum supported: {MAX_IMAGE_SIZE[0]}x{MAX_IMAGE_SIZE[1]}"
        
        return True, "Image validation passed"
        
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}")
        return False, f"Image file corrupted or format error: {str(e)}"

def smart_resize(img):
    """智能缩放图片，保持宽高比"""
    original_size = img.size
    
    # 如果图片尺寸在合理范围内，直接返回
    if img.size[0] <= MAX_IMAGE_SIZE[0] and img.size[1] <= MAX_IMAGE_SIZE[1]:
        return img, False
    
    # 计算缩放比例
    ratio = min(MAX_IMAGE_SIZE[0] / img.size[0], MAX_IMAGE_SIZE[1] / img.size[1])
    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
    
    # 使用高质量缩放
    resized_img = img.resize(new_size, Image.LANCZOS)
    
    logger.info(f"图片已缩放：{original_size} -> {new_size}")
    return resized_img, True

def add_grain_pure_pil(img, intensity=30):
    """在图片上加颗粒噪点（纯 PIL，不依赖 numpy）"""
    img = img.convert('RGB')
    pixels = img.load()
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = pixels[i, j]
            noise = lambda: random.randint(-intensity, intensity)
            r = max(0, min(255, r + noise()))
            g = max(0, min(255, g + noise()))
            b = max(0, min(255, b + noise()))
            pixels[i, j] = (r, g, b)
    return img

def apply_filter(image_data, filter_name):
    """直接在内存中处理图片，不保存文件"""
    try:
        # 验证图片
        is_valid, message = validate_image(image_data)
        if not is_valid:
            raise ValueError(message)
        
        # 打开图片
        img = Image.open(io.BytesIO(image_data))
        original_format = img.format
        
        # 转换为RGB模式（处理RGBA、P等模式）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 智能缩放（如果需要）
        img, was_resized = smart_resize(img)
        
        # 古早像素缩放（保持2000s风格）
        original_size = img.size
        img = img.resize((img.width//2, img.height//2), Image.NEAREST)
        img = img.resize(original_size, Image.NEAREST)

        # 过滤器列表
        if filter_name == 'vintage':
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*1.1),
                g.point(lambda i:i*1.05),
                b.point(lambda i:i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=30)

        elif filter_name == 'ccd':
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*0.8),
                g.point(lambda i:i*0.85),
                b.point(lambda i:i*1.15)
            ))
            img = add_grain_pure_pil(img, intensity=35)

        elif filter_name == 'kodachrome':
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*1.05),
                g.point(lambda i:i*0.95),
                b.point(lambda i:i*1.0)
            ))
            img = add_grain_pure_pil(img, intensity=28)

        elif filter_name == 'fuji_superia':
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*0.95),
                g.point(lambda i:i*1.0),
                b.point(lambda i:i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=28)

        elif filter_name == 'agfa':
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*0.9),
                g.point(lambda i:i*0.95),
                b.point(lambda i:i*1.0)
            ))
            img = add_grain_pure_pil(img, intensity=30)
        
        elif filter_name == 'retro_green': 
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*0.85),
                g.point(lambda i:i*0.9),
                b.point(lambda i:i*0.85)
            ))
            img = add_grain_pure_pil(img, intensity=28)

        elif filter_name == 'dark_brown': 
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*0.7),
                g.point(lambda i:i*0.65),
                b.point(lambda i:i*0.6)
            ))
            img = ImageEnhance.Color(img).enhance(0.8)
            img = add_grain_pure_pil(img, intensity=32)
            
        elif filter_name == 'lomo':
            img = ImageEnhance.Color(img).enhance(1.5)
            img = ImageEnhance.Contrast(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.05),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=35)
            
        elif filter_name == 'dreamy':
            img = ImageEnhance.Brightness(img).enhance(1.1)
            img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i:i*1.1),
                g.point(lambda i:i*1.1),
                b.point(lambda i:i*1.05)
            ))
            img = add_grain_pure_pil(img, intensity=30)
            
        elif filter_name == 'vhs':
            img = ImageEnhance.Brightness(img).enhance(0.9)
            img = ImageEnhance.Contrast(img).enhance(1.1)
            r, g, b = img.split()
            r = r.point(lambda i: i * 1.05)
            b = b.point(lambda i: i * 0.95)
            img = Image.merge("RGB", (r, g, b))
            img = add_grain_pure_pil(img, intensity=40)

        # 新增滤镜
        elif filter_name == 'vaporwave':
            img = ImageEnhance.Color(img).enhance(1.8)
            img = ImageEnhance.Brightness(img).enhance(1.1)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.1),
                g.point(lambda i: i*1.2),
                b.point(lambda i: i*1.5)
            ))
            img = add_grain_pure_pil(img, intensity=45)

        elif filter_name == 'glitch':
            img = ImageEnhance.Contrast(img).enhance(1.3)
            img = ImageEnhance.Brightness(img).enhance(0.9)
            
            offset = 5
            r, g, b = img.split()
            new_g = g.crop((offset, 0, img.width, img.height))
            new_b = b.crop((0, 0, img.width - offset, img.height))
            
            r_img = Image.new('L', img.size)
            r_img.paste(r, (0, 0))
            
            g_img = Image.new('L', img.size)
            g_img.paste(new_g, (0, 0))
            
            b_img = Image.new('L', img.size)
            b_img.paste(new_b, (offset, 0))
            
            img = Image.merge("RGB", (r_img, g_img, b_img))
            img = add_grain_pure_pil(img, intensity=50)

        elif filter_name == 'y2k':
            img = ImageEnhance.Color(img).enhance(1.4)
            img = ImageEnhance.Contrast(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.1),
                g.point(lambda i: i*1.0),
                b.point(lambda i: i*1.1)
            ))
            img = img.filter(ImageFilter.SHARPEN)
            img = add_grain_pure_pil(img, intensity=30)

        # 新增10个2000s风格滤镜
        elif filter_name == 'cyberpunk':
            # 赛博朋克风格 - 高对比度，蓝紫色调
            img = ImageEnhance.Contrast(img).enhance(1.4)
            img = ImageEnhance.Color(img).enhance(1.3)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.8),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*1.3)
            ))
            img = add_grain_pure_pil(img, intensity=40)

        elif filter_name == 'neon_pop':
            # 霓虹流行 - 高饱和度，粉紫色调
            img = ImageEnhance.Color(img).enhance(1.8)
            img = ImageEnhance.Brightness(img).enhance(1.1)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.2),
                g.point(lambda i: i*1.0),
                b.point(lambda i: i*1.4)
            ))
            img = add_grain_pure_pil(img, intensity=35)

        elif filter_name == 'digital_cam':
            # 早期数码相机 - 低饱和度，偏绿
            img = ImageEnhance.Color(img).enhance(0.7)
            img = ImageEnhance.Contrast(img).enhance(1.1)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.9),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*0.8)
            ))
            img = add_grain_pure_pil(img, intensity=45)

        elif filter_name == 'cyber_pink':
            # 赛博粉 - 粉色调，高对比度
            img = ImageEnhance.Contrast(img).enhance(1.3)
            img = ImageEnhance.Color(img).enhance(1.5)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.3),
                g.point(lambda i: i*0.9),
                b.point(lambda i: i*1.1)
            ))
            img = add_grain_pure_pil(img, intensity=30)

        elif filter_name == 'retro_blue':
            # 复古蓝 - 蓝色调，低亮度
            img = ImageEnhance.Brightness(img).enhance(0.8)
            img = ImageEnhance.Contrast(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.7),
                g.point(lambda i: i*0.9),
                b.point(lambda i: i*1.2)
            ))
            img = add_grain_pure_pil(img, intensity=38)

        elif filter_name == 'millennium_gold':
            # 千禧金 - 金色调，温暖感
            img = ImageEnhance.Brightness(img).enhance(1.1)
            img = ImageEnhance.Color(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.2),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*0.8)
            ))
            img = add_grain_pure_pil(img, intensity=32)

        elif filter_name == 'matrix_green':
            # 矩阵绿 - 绿色调，电影感
            img = ImageEnhance.Contrast(img).enhance(1.3)
            img = ImageEnhance.Brightness(img).enhance(0.9)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.6),
                g.point(lambda i: i*1.2),
                b.point(lambda i: i*0.7)
            ))
            img = add_grain_pure_pil(img, intensity=42)

        elif filter_name == 'disco_fever':
            # 迪斯科狂热 - 高饱和度，紫红色调
            img = ImageEnhance.Color(img).enhance(1.6)
            img = ImageEnhance.Brightness(img).enhance(1.05)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.3),
                g.point(lambda i: i*0.8),
                b.point(lambda i: i*1.2)
            ))
            img = add_grain_pure_pil(img, intensity=35)

        elif filter_name == 'tech_silver':
            # 科技银 - 银色调，冷感
            img = ImageEnhance.Contrast(img).enhance(1.2)
            img = ImageEnhance.Brightness(img).enhance(0.95)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.9),
                g.point(lambda i: i*0.95),
                b.point(lambda i: i*1.0)
            ))
            img = ImageEnhance.Color(img).enhance(0.8)
            img = add_grain_pure_pil(img, intensity=40)

        elif filter_name == 'y2k_purple':
            # Y2K紫 - 紫色调，未来感
            img = ImageEnhance.Color(img).enhance(1.4)
            img = ImageEnhance.Contrast(img).enhance(1.25)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.1),
                g.point(lambda i: i*0.8),
                b.point(lambda i: i*1.3)
            ))
            img = add_grain_pure_pil(img, intensity=33)

        # 新增8个更清晰、灰色调的Y2K风格滤镜
        elif filter_name == 'misty_gray':
            # 迷雾灰 - 轻微模糊，柔和灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
            img = ImageEnhance.Brightness(img).enhance(0.9)
            img = ImageEnhance.Color(img).enhance(0.5)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.9),
                g.point(lambda i: i*0.9),
                b.point(lambda i: i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=20)

        elif filter_name == 'cloudy_dream':
            # 云梦 - 轻度模糊，淡雅灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
            img = ImageEnhance.Brightness(img).enhance(1.0)
            img = ImageEnhance.Color(img).enhance(0.6)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.95),
                g.point(lambda i: i*0.95),
                b.point(lambda i: i*0.95)
            ))
            img = add_grain_pure_pil(img, intensity=18)

        elif filter_name == 'foggy_memory':
            # 雾忆 - 中度模糊，怀旧灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.8))
            img = ImageEnhance.Brightness(img).enhance(0.85)
            img = ImageEnhance.Color(img).enhance(0.4)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.85),
                g.point(lambda i: i*0.85),
                b.point(lambda i: i*0.85)
            ))
            img = add_grain_pure_pil(img, intensity=25)

        elif filter_name == 'silver_mist':
            # 银雾 - 轻微模糊，银色灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.0))
            img = ImageEnhance.Brightness(img).enhance(0.95)
            img = ImageEnhance.Color(img).enhance(0.7)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.0),
                g.point(lambda i: i*1.0),
                b.point(lambda i: i*1.0)
            ))
            img = add_grain_pure_pil(img, intensity=15)

        elif filter_name == 'dusty_film':
            # 尘封胶片 - 中度模糊，复古灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.6))
            img = ImageEnhance.Brightness(img).enhance(0.8)
            img = ImageEnhance.Color(img).enhance(0.5)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.9),
                g.point(lambda i: i*0.9),
                b.point(lambda i: i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=28)

        elif filter_name == 'hazy_night':
            # 朦胧夜 - 轻度模糊，夜晚灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.3))
            img = ImageEnhance.Brightness(img).enhance(0.7)
            img = ImageEnhance.Color(img).enhance(0.6)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.95),
                g.point(lambda i: i*0.95),
                b.point(lambda i: i*0.95)
            ))
            img = add_grain_pure_pil(img, intensity=22)

        elif filter_name == 'soft_focus':
            # 柔焦 - 轻微模糊，柔和灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.1))
            img = ImageEnhance.Brightness(img).enhance(1.0)
            img = ImageEnhance.Color(img).enhance(0.7)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.0),
                g.point(lambda i: i*1.0),
                b.point(lambda i: i*1.0)
            ))
            img = add_grain_pure_pil(img, intensity=16)

        elif filter_name == 'vintage_blur':
            # 复古模糊 - 中度模糊，老照片灰色调
            img = img.filter(ImageFilter.GaussianBlur(radius=1.7))
            img = ImageEnhance.Brightness(img).enhance(0.85)
            img = ImageEnhance.Color(img).enhance(0.4)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.85),
                g.point(lambda i: i*0.85),
                b.point(lambda i: i*0.85)
            ))
            img = add_grain_pure_pil(img, intensity=26)

        # 新增9个爆款Y2K风格滤镜
        elif filter_name == 'neon_glow':
            # 霓虹发光 - Basic类别，高亮度高对比度，霓虹灯效果
            img = ImageEnhance.Brightness(img).enhance(1.3)
            img = ImageEnhance.Contrast(img).enhance(1.4)
            img = ImageEnhance.Color(img).enhance(1.6)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.2),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*1.3)
            ))
            img = add_grain_pure_pil(img, intensity=25)

        elif filter_name == 'cyber_retro':
            # 赛博复古 - Basic类别，冷色调，未来复古感
            img = ImageEnhance.Contrast(img).enhance(1.3)
            img = ImageEnhance.Color(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.9),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*1.2)
            ))
            img = add_grain_pure_pil(img, intensity=35)

        elif filter_name == 'synthwave':
            # 合成波 - Basic类别，粉紫色调，80年代电子音乐风格
            img = ImageEnhance.Color(img).enhance(1.7)
            img = ImageEnhance.Brightness(img).enhance(1.1)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.3),
                g.point(lambda i: i*0.9),
                b.point(lambda i: i*1.4)
            ))
            img = add_grain_pure_pil(img, intensity=30)

        elif filter_name == 'sepia_dust':
            # 深褐色复古 - Vintage类别，深褐色调，增加颗粒感
            img = ImageEnhance.Color(img).enhance(0.6)
            img = ImageEnhance.Brightness(img).enhance(0.8)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.7),
                g.point(lambda i: i*0.6),
                b.point(lambda i: i*0.5)
            ))
            img = add_grain_pure_pil(img, intensity=45)

        elif filter_name == 'polaroid_fade':
            # 宝丽来褪色 - Vintage类别，降低饱和度，淡黄色调
            img = ImageEnhance.Color(img).enhance(0.7)
            img = ImageEnhance.Brightness(img).enhance(1.05)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.1),
                g.point(lambda i: i*1.05),
                b.point(lambda i: i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=32)

        elif filter_name == 'chrome_shine':
            # 金属光泽 - Y2K类别，增加金属光泽和高光
            img = ImageEnhance.Contrast(img).enhance(1.5)
            img = ImageEnhance.Brightness(img).enhance(1.2)
            img = ImageEnhance.Color(img).enhance(1.3)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.1),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*1.1)
            ))
            img = img.filter(ImageFilter.SHARPEN)
            img = add_grain_pure_pil(img, intensity=20)

        elif filter_name == 'bubble_pop':
            # 泡泡流行 - Y2K类别，明亮色彩，高对比度
            img = ImageEnhance.Color(img).enhance(1.8)
            img = ImageEnhance.Brightness(img).enhance(1.15)
            img = ImageEnhance.Contrast(img).enhance(1.3)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.2),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*1.3)
            ))
            img = add_grain_pure_pil(img, intensity=28)

        elif filter_name == 'glitch_art':
            # 故障艺术 - Special Effects类别，模拟数字信号干扰
            img = ImageEnhance.Contrast(img).enhance(1.6)
            img = ImageEnhance.Brightness(img).enhance(0.9)
            
            # 创建RGB通道偏移效果
            offset = 8
            r, g, b = img.split()
            
            # 红色通道向右偏移
            new_r = r.crop((offset, 0, img.width, img.height))
            r_img = Image.new('L', img.size)
            r_img.paste(new_r, (0, 0))
            
            # 蓝色通道向左偏移
            new_b = b.crop((0, 0, img.width - offset, img.height))
            b_img = Image.new('L', img.size)
            b_img.paste(new_b, (offset, 0))
            
            img = Image.merge("RGB", (r_img, g, b_img))
            img = add_grain_pure_pil(img, intensity=55)

        elif filter_name == 'holographic':
            # 全息图 - Special Effects类别，彩虹色调和光斑效果
            img = ImageEnhance.Color(img).enhance(2.0)
            img = ImageEnhance.Brightness(img).enhance(1.1)
            img = ImageEnhance.Contrast(img).enhance(1.4)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.3),
                g.point(lambda i: i*1.2),
                b.point(lambda i: i*1.4)
            ))
            # 添加彩虹色偏移效果
            offset = 3
            r, g, b = img.split()
            new_g = g.crop((offset, 0, img.width, img.height))
            g_img = Image.new('L', img.size)
            g_img.paste(new_g, (0, 0))
            img = Image.merge("RGB", (r, g_img, b))
            img = add_grain_pure_pil(img, intensity=40)

        # 新增10个爆款Y2K风格滤镜
        elif filter_name == 'electric_blue':
            # 电蓝色调 - Basic类别，高对比度蓝色调
            img = ImageEnhance.Contrast(img).enhance(1.5)
            img = ImageEnhance.Color(img).enhance(1.4)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.7),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*1.4)
            ))
            img = add_grain_pure_pil(img, intensity=30)

        elif filter_name == 'neon_pink':
            # 霓虹粉色 - Basic类别，高饱和度粉色调
            img = ImageEnhance.Color(img).enhance(1.8)
            img = ImageEnhance.Brightness(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.4),
                g.point(lambda i: i*0.8),
                b.point(lambda i: i*1.2)
            ))
            img = add_grain_pure_pil(img, intensity=35)

        elif filter_name == 'cyber_green':
            # 赛博绿色 - Basic类别，科技感绿色调
            img = ImageEnhance.Contrast(img).enhance(1.4)
            img = ImageEnhance.Color(img).enhance(1.3)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.6),
                g.point(lambda i: i*1.3),
                b.point(lambda i: i*0.8)
            ))
            img = add_grain_pure_pil(img, intensity=32)

        elif filter_name == 'retro_orange':
            # 复古橙色 - Basic类别，温暖橙色调
            img = ImageEnhance.Brightness(img).enhance(1.1)
            img = ImageEnhance.Color(img).enhance(1.2)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.3),
                g.point(lambda i: i*1.1),
                b.point(lambda i: i*0.7)
            ))
            img = add_grain_pure_pil(img, intensity=28)

        elif filter_name == 'film_grain':
            # 胶片颗粒 - Vintage类别，复古胶片质感
            img = ImageEnhance.Color(img).enhance(0.8)
            img = ImageEnhance.Brightness(img).enhance(0.9)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.9),
                g.point(lambda i: i*0.85),
                b.point(lambda i: i*0.8)
            ))
            img = add_grain_pure_pil(img, intensity=50)

        elif filter_name == 'aged_paper':
            # 老化纸张 - Vintage类别，怀旧纸张效果
            img = ImageEnhance.Color(img).enhance(0.7)
            img = ImageEnhance.Brightness(img).enhance(1.05)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.1),
                g.point(lambda i: i*1.05),
                b.point(lambda i: i*0.9)
            ))
            img = add_grain_pure_pil(img, intensity=45)

        elif filter_name == 'metallic_silver':
            # 金属银色 - Y2K类别，未来感银色调
            img = ImageEnhance.Contrast(img).enhance(1.6)
            img = ImageEnhance.Brightness(img).enhance(1.1)
            img = ImageEnhance.Color(img).enhance(0.6)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.0),
                g.point(lambda i: i*1.0),
                b.point(lambda i: i*1.0)
            ))
            img = add_grain_pure_pil(img, intensity=25)

        elif filter_name == 'neon_cyan':
            # 霓虹青色 - Y2K类别，Y2K风格青色调
            img = ImageEnhance.Color(img).enhance(1.7)
            img = ImageEnhance.Brightness(img).enhance(1.15)
            img = ImageEnhance.Contrast(img).enhance(1.3)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*0.8),
                g.point(lambda i: i*1.2),
                b.point(lambda i: i*1.3)
            ))
            img = add_grain_pure_pil(img, intensity=30)

        elif filter_name == 'digital_noise':
            # 数字噪点 - Special Effects类别，故障噪点效果
            img = ImageEnhance.Contrast(img).enhance(1.7)
            img = ImageEnhance.Brightness(img).enhance(0.95)
            
            # 创建数字噪点效果
            offset = 6
            r, g, b = img.split()
            
            # 红色通道向右偏移
            new_r = r.crop((offset, 0, img.width, img.height))
            r_img = Image.new('L', img.size)
            r_img.paste(new_r, (0, 0))
            
            # 蓝色通道向左偏移
            new_b = b.crop((0, 0, img.width - offset, img.height))
            b_img = Image.new('L', img.size)
            b_img.paste(new_b, (offset, 0))
            
            img = Image.merge("RGB", (r_img, g, b_img))
            img = add_grain_pure_pil(img, intensity=60)

        elif filter_name == 'rainbow_shift':
            # 彩虹偏移 - Special Effects类别，全息彩虹效果
            img = ImageEnhance.Color(img).enhance(2.2)
            img = ImageEnhance.Brightness(img).enhance(1.1)
            img = ImageEnhance.Contrast(img).enhance(1.5)
            r, g, b = img.split()
            img = Image.merge("RGB", (
                r.point(lambda i: i*1.4),
                g.point(lambda i: i*1.3),
                b.point(lambda i: i*1.5)
            ))
            # 添加彩虹色偏移效果
            offset = 4
            r, g, b = img.split()
            new_r = r.crop((offset, 0, img.width, img.height))
            r_img = Image.new('L', img.size)
            r_img.paste(new_r, (0, 0))
            
            new_b = b.crop((0, 0, img.width - offset, img.height))
            b_img = Image.new('L', img.size)
            b_img.paste(new_b, (offset, 0))
            
            img = Image.merge("RGB", (r_img, g, b_img))
            img = add_grain_pure_pil(img, intensity=45)
        
        # 将处理后的图片转换为字节数据返回，不保存文件
        img_io = io.BytesIO()
        
        # 根据原始格式选择输出格式和质量
        if original_format in ['PNG', 'BMP', 'TIFF']:
            img.save(img_io, format='PNG', optimize=True)
        else:
            img.save(img_io, format='JPEG', quality=90, optimize=True)
        
        img_io.seek(0)
        return img_io.getvalue()
        
    except ValueError as e:
        # 用户输入错误（文件过大、格式不支持等）
        logger.error(f"User input error: {str(e)}")
        raise e
    except Exception as e:
        # 其他处理错误
        logger.error(f"Image processing failed: {str(e)}")
        raise ValueError(f"Image processing failed, please try a different image: {str(e)}")
