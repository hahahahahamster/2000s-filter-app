from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import random
import os

PROCESSED_FOLDER = 'static/processed'

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

def apply_filter(image_path, filter_name):
    img = Image.open(image_path).convert('RGB')

    # 古早像素缩放
    img = img.resize((img.width//2, img.height//2), Image.Resampling.NEAREST)
    img = img.resize((img.width*2, img.height*2), Image.Resampling.NEAREST)

    # 过滤器列表
    if filter_name == 'vintage':
        r, g, b = img.split()
        img = Image.merge("RGB", (
            r.point(lambda i:i*1.1),
            g.point(lambda i:i*1.05),
            b.point(lambda i:i*0.9)
        ))
        img = add_grain_pure_pil(img, intensity=30)

    elif filter_name == 'film':
        img = ImageOps.colorize(img.convert('L'), black="#222222", white="#f4e1d2")
        img = add_grain_pure_pil(img, intensity=32)

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

    elif filter_name == 'sepia': 
        img = ImageOps.colorize(img.convert('L'), black="#4a3528", white="#f0e2d5")
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

    elif filter_name == 'bw':
        img = img.convert('L').convert('RGB')
        img = add_grain_pure_pil(img, intensity=25)

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
        
    processed_path = os.path.join(PROCESSED_FOLDER, os.path.basename(image_path))
    img.save(processed_path)
    return processed_path