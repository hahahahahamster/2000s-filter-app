# 示例图片说明

## 文件结构

请将您的示例图片按照以下命名规则放置在 `static/examples/` 文件夹中：

### 示例1 - CCD滤镜效果
- `original1.jpg` - 原始图片
- `ccd_filtered1.jpg` - 应用CCD滤镜后的效果

### 示例2 - 复古滤镜效果
- `original2.jpg` - 原始图片
- `vintage_filtered2.jpg` - 应用复古滤镜后的效果

### 示例3 - Y2K风格滤镜效果
- `original3.jpg` - 原始图片
- `y2k_filtered3.jpg` - 应用Y2K风格滤镜后的效果

### 示例4 - Vaporwave滤镜效果
- `original4.jpg` - 原始图片
- `vaporwave_filtered4.jpg` - 应用Vaporwave滤镜后的效果

## 图片要求

- **格式**: JPG, PNG, WEBP
- **尺寸**: 建议 400x400 到 800x800 像素
- **文件大小**: 建议每个文件不超过 500KB
- **质量**: 清晰、高质量的照片

## 添加更多示例

如果您想添加更多示例，可以：

1. 在 `templates/index.html` 中添加新的示例项
2. 按照命名规则添加对应的图片文件
3. 更新CSS样式以适应新的布局

## 注意事项

- 图片文件不存在时会自动隐藏，不会显示错误
- 建议使用相同尺寸的原始图片和滤镜效果图片
- 确保图片内容适合所有年龄段的用户
