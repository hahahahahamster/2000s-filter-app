const uploadInput = document.getElementById('upload');
const uploadBox = document.getElementById('upload-box');
const uploadForm = document.getElementById('upload-form');
const originalContainer = document.getElementById('original-container');
const processedContainer = document.getElementById('processed-container');
const flashMessage = document.querySelector('.flash');
const filterButtons = document.querySelectorAll('.filter-btn');
const generateButton = document.querySelector('.generate-btn');
const categoryTabs = document.querySelectorAll('.category-tab');
const filterButtonsContainer = document.getElementById('filter-buttons');

// 状态管理
let currentImageData = null;
let currentFilter = null;
let isProcessing = false;

// Filter categories mapping
const filterCategories = {
    'basic': ['ccd', 'vintage', 'lomo', 'dreamy', 'neon_glow', 'cyber_retro', 'synthwave', 'electric_blue', 'neon_pink', 'cyber_green', 'retro_orange'],
    'vintage': ['kodachrome', 'fuji_superia', 'agfa', 'retro_green', 'dark_brown', 'vhs', 'sepia_dust', 'polaroid_fade', 'film_grain', 'aged_paper'],
    'y2k': ['y2k', 'cyberpunk', 'neon_pop', 'cyber_pink', 'y2k_purple', 'millennium_gold', 'chrome_shine', 'bubble_pop', 'metallic_silver', 'neon_cyan'],
    'effects': ['vaporwave', 'glitch', 'matrix_green', 'disco_fever', 'tech_silver', 'glitch_art', 'holographic', 'digital_noise', 'rainbow_shift'],
    'advanced': ['digital_cam', 'retro_blue', 'misty_gray', 'cloudy_dream', 'foggy_memory', 'silver_mist', 'dusty_film', 'hazy_night', 'soft_focus', 'vintage_blur']
};

// Category tab functionality
categoryTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs
        categoryTabs.forEach(t => t.classList.remove('active'));
        // Add active class to clicked tab
        tab.classList.add('active');
        
        const category = tab.dataset.category;
        // 只更新UI显示，不触发任何处理
        filterByCategory(category);
    });
});

function filterByCategory(category) {
    const allFilterButtons = document.querySelectorAll('.filter-btn');
    
    // 只更新滤镜按钮的显示/隐藏状态
    allFilterButtons.forEach(button => {
        if (category === 'all') {
            button.style.display = 'inline-block';
        } else {
            const filterName = button.value;
            const shouldShow = filterCategories[category] && filterCategories[category].includes(filterName);
            button.style.display = shouldShow ? 'inline-block' : 'none';
        }
    });
    
    // 如果当前选中的滤镜被隐藏了，只移除选中状态，不自动选择新滤镜
    const selectedButton = document.querySelector('.filter-btn.selected');
    if (selectedButton && selectedButton.style.display === 'none') {
        // 只移除选中状态，不自动选择新滤镜
        selectedButton.classList.remove('selected');
    }
    
    // 确保不会自动触发任何处理
    // 分类切换只更新UI显示，不处理图片
    // 不自动选择任何滤镜，不触发任何事件
}

// 处理文件拖拽
uploadBox.addEventListener('dragover', e => {
    e.preventDefault();
    uploadBox.style.borderColor = "rgba(255, 255, 255, 0.8)";
});

uploadBox.addEventListener('dragleave', e => {
    e.preventDefault();
    uploadBox.style.borderColor = "rgba(255, 255, 255, 0.5)";
});

uploadBox.addEventListener('drop', e => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if(files.length){
        uploadInput.files = files;
        handleFileChange();
    }
});

// 处理文件选择
uploadInput.addEventListener('change', handleFileChange);

function handleFileChange() {
    if (uploadInput.files.length) {
        const file = uploadInput.files[0];
        
        // 重置状态
        currentImageData = null;
        currentFilter = null;
        isProcessing = false;
        
        // 清除提示信息
        if (flashMessage) {
            flashMessage.style.display = 'none';
        }
        
        // 验证文件
        const validation = validateFile(file);
        if (!validation.isValid) {
            showMessage(validation.error);
            uploadInput.value = ''; // 清空文件选择
            showPlaceholder();
            return;
        }
        
        // 显示原图预览
        previewImage(file);
        
        // 显示上传成功消息并滚动到滤镜分类
        showMessage('Upload successful! You can select a filter effect');
        scrollToFilterCategories();
        
        // 更新处理结果区域提示
        processedContainer.innerHTML = '<h3>- Filtered Result -</h3><div class="processed-placeholder"><p>Click the generate button to see your filtered image!</p></div>';
    }
}

function validateFile(file) {
    // 检查文件大小（50MB限制）
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        return {
            isValid: false,
            error: `File too large (${(file.size / (1024*1024)).toFixed(1)}MB). Maximum supported: 50MB`
        };
    }
    
    // 检查文件类型
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/gif', 'image/tiff', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        return {
            isValid: false,
            error: `Unsupported file format (${file.type}). Supported formats: JPEG, PNG, BMP, GIF, TIFF, WEBP`
        };
    }
    
    return { isValid: true };
}

function previewImage(file) {
    const reader = new FileReader();
    reader.onload = e => {
        originalContainer.innerHTML = `<h3>- Original Preview -</h3><img id="preview-original" src="${e.target.result}">`;
    }
    reader.readAsDataURL(file);
}

// 滤镜按钮点击事件
filterButtons.forEach(button => {
    button.addEventListener('click', e => {
        e.preventDefault();
        
        // 移除所有按钮的selected类
        filterButtons.forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
        
        // 只有在有图片上传时才处理
        if (uploadInput.files.length > 0) {
            if (button.value !== currentFilter) {
                processImage(button.value);
            } else {
                // 如果滤镜相同，显示提示信息
                showMessage('Same filter already applied - no processing needed');
            }
        }
        // 如果没有上传图片，只更新UI状态，不显示任何提示
    });
});

// 处理表单提交事件
uploadForm.addEventListener('submit', e => {
    e.preventDefault();
    
    if (uploadInput.files.length === 0) {
        showMessage("Please upload an image first!");
        return;
    }
    
    // 获取当前选中的滤镜
    const selectedFilter = document.querySelector('.filter-btn.selected');
    const filterName = selectedFilter ? selectedFilter.value : 'ccd';
    
    processImage(filterName);
});

generateButton.addEventListener('click', e => {
    e.preventDefault();
    
    if (uploadInput.files.length === 0) {
        showMessage("Please upload an image first!");
        return;
    }
    
    // 获取当前选中的滤镜
    const selectedFilter = document.querySelector('.filter-btn.selected');
    const filterName = selectedFilter ? selectedFilter.value : 'ccd';
    
    processImage(filterName);
});


function displayFilteredImage(imageData, filterName) {
    processedContainer.innerHTML = `
        <h3>- Filtered Result (${filterName.replace('_', ' ').toUpperCase()}) -</h3>
        <img id="preview-processed" src="${imageData}" alt="Filtered image">
        <div class="download-section">
            <a href="${imageData}" download="filtered_${filterName}.jpg" class="download-btn">Download</a>
        </div>
    `;
    
    // 保存当前图片数据
    currentImageData = imageData;
    
    // 显示生成成功消息
    showMessage('Photo generated successfully! You can download and save it');
}

function showGeneratingMessage() {
    processedContainer.innerHTML = '<h3>- Filtered Result -</h3><div class="generating-message"><p>Processing your image...</p><div class="rotating-circle"></div><p class="processing-subtitle">(This may only take a few seconds)</p></div>';
}

function showPlaceholder() {
    processedContainer.innerHTML = '<h3>- Filtered Result -</h3><div class="processed-placeholder"><p>Click the generate button to see your filtered image!</p></div>';
}

function showMessage(message) {
    const messageArea = document.getElementById('message-area');
    const messageText = document.getElementById('message-text');
    
    if (messageArea && messageText) {
        messageText.textContent = message;
        messageArea.style.display = 'block';
        
        // 自动隐藏消息（3秒后）
        setTimeout(() => {
            messageArea.style.display = 'none';
        }, 3000);
    }
}

function scrollToFilterCategories() {
    const filterCategories = document.getElementById('filters');
    if (filterCategories) {
        // 获取导航栏高度
        const navbar = document.querySelector('.navbar');
        const navbarHeight = navbar ? navbar.offsetHeight : 0;
        
        // 计算滚动位置，确保滤镜分类选项可见
        const targetPosition = filterCategories.offsetTop - navbarHeight - 20;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
}

function showFlashMessage(message, type = 'info') {
    if (flashMessage) {
        const className = type === 'error' ? 'flash-error' : 'flash';
        flashMessage.className = className;
        flashMessage.innerHTML = `<p>${message}</p>`;
        flashMessage.style.display = 'block';
        flashMessage.style.opacity = '0';
        flashMessage.style.transform = 'translateY(-10px)';
        
        // Animate in
        setTimeout(() => {
            flashMessage.style.transition = 'all 0.3s ease';
            flashMessage.style.opacity = '1';
            flashMessage.style.transform = 'translateY(0)';
        }, 10);
        
        setTimeout(() => {
            // Animate out
            flashMessage.style.opacity = '0';
            flashMessage.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                flashMessage.style.display = 'none';
            }, 300);
        }, type === 'error' ? 5000 : 3000);
    }
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const href = this.getAttribute('href');
        
        // 如果是Filter Categories链接，使用新的滚动函数
        if (href === '#filters') {
            scrollToFilterCategories();
        } else {
            const target = document.querySelector(href);
            if (target) {
                // Get the height of the fixed navbar
                const navbar = document.querySelector('.navbar');
                const navbarHeight = navbar ? navbar.offsetHeight : 0;
                
                // Calculate the position to scroll to (accounting for navbar height)
                const targetPosition = target.offsetTop - navbarHeight - 20; // 20px extra padding
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Add loading animation to generate button
function setGenerateButtonLoading(loading) {
    if (loading) {
        generateButton.innerHTML = 'Processing...';
        generateButton.disabled = true;
        generateButton.style.opacity = '0.7';
    } else {
        generateButton.innerHTML = 'Generate';
        generateButton.disabled = false;
        generateButton.style.opacity = '1';
    }
}

// Update processImage function to use loading state and avoid duplicate processing
function processImage(filterName) {
    if (!uploadInput.files.length) {
        showMessage("Please upload an image first!");
        return;
    }
    
    // 如果正在处理或滤镜相同，避免重复处理
    if (isProcessing || filterName === currentFilter) {
        return;
    }
    
    isProcessing = true;
    setGenerateButtonLoading(true);
    showGeneratingMessage();
    
    const formData = new FormData();
    formData.append('image', uploadInput.files[0]);
    formData.append('filter', filterName);
    
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        isProcessing = false;
        setGenerateButtonLoading(false);
        if (data.success) {
            currentFilter = filterName;
            displayFilteredImage(data.filtered_image, data.filter_name);
        } else {
            showMessage(data.error || 'Processing failed. Please try again');
            showPlaceholder();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        isProcessing = false;
        setGenerateButtonLoading(false);
        showMessage('Network error occurred, please try again');
        showPlaceholder();
    });
}

// Interactive Image Comparison Slider
function initImageComparison() {
    const sliderHandles = document.querySelectorAll('.slider-handle');
    const imageAfterWrappers = document.querySelectorAll('.image-after-wrapper');
    const containers = document.querySelectorAll('.image-compare-container');
    
    if (!sliderHandles.length || !imageAfterWrappers.length || !containers.length) return;
    
    // Initialize each comparison slider
    sliderHandles.forEach((sliderHandle, index) => {
        const imageAfterWrapper = imageAfterWrappers[index];
        const container = containers[index];
        
        if (!sliderHandle || !imageAfterWrapper || !container) return;
        
        let isDragging = false;
        
        // Mouse events
        sliderHandle.addEventListener('mousedown', (e) => {
            isDragging = true;
            document.body.style.userSelect = 'none';
            document.body.style.cursor = 'ew-resize';
            e.preventDefault();
        });
        
        const handleMouseMove = (e) => {
            if (!isDragging) return;
            
            const rect = container.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const containerWidth = rect.width;
            
            // Calculate percentage based on mouse position
            const percentage = Math.max(0, Math.min(100, (mouseX / containerWidth) * 100));
            
            // Update the width of the after image wrapper (this controls how much of the filtered image is visible)
            imageAfterWrapper.style.width = `${percentage}%`;
            
            // Update slider position
            sliderHandle.style.left = `${percentage}%`;
        };
        
        const handleMouseUp = () => {
            if (isDragging) {
                isDragging = false;
                document.body.style.userSelect = '';
                document.body.style.cursor = '';
            }
        };
        
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
        
        // Touch events for mobile
        sliderHandle.addEventListener('touchstart', (e) => {
            isDragging = true;
            e.preventDefault();
        });
        
        const handleTouchMove = (e) => {
            if (!isDragging) return;
            
            const rect = container.getBoundingClientRect();
            const touchX = e.touches[0].clientX - rect.left;
            const containerWidth = rect.width;
            
            // Calculate percentage based on touch position
            const percentage = Math.max(0, Math.min(100, (touchX / containerWidth) * 100));
            
            // Update the width of the after image wrapper
            imageAfterWrapper.style.width = `${percentage}%`;
            
            // Update slider position
            sliderHandle.style.left = `${percentage}%`;
            
            e.preventDefault();
        };
        
        const handleTouchEnd = () => {
            if (isDragging) {
                isDragging = false;
            }
        };
        
        document.addEventListener('touchmove', handleTouchMove);
        document.addEventListener('touchend', handleTouchEnd);
    });
}

// Initialize image comparison when page loads
document.addEventListener('DOMContentLoaded', initImageComparison);