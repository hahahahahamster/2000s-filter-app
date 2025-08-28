const uploadInput = document.getElementById('upload');
const uploadBox = document.getElementById('upload-box');
const uploadForm = document.getElementById('upload-form');
const originalContainer = document.getElementById('original-container');
const processedContainer = document.getElementById('processed-container');
const flashMessage = document.querySelector('.flash');
const filterButtons = document.querySelectorAll('.filter-btn');
const generateButton = document.querySelector('.generate-btn');

// 处理文件拖拽
uploadBox.addEventListener('dragover', e => {
    e.preventDefault();
    uploadBox.style.borderColor = "#2c3e50";
});

uploadBox.addEventListener('dragleave', e => {
    e.preventDefault();
    uploadBox.style.borderColor = "#34495e";
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
        // 清除提示信息
        if (flashMessage) {
            flashMessage.style.display = 'none';
        }

        // 清空processed预览框并显示placeholder
        const processedImage = document.getElementById('preview-processed');
        const downloadBtn = document.querySelector('.download-btn');
        if (processedImage) processedImage.remove();
        if (downloadBtn) downloadBtn.remove();
        
        // 确保 placeholder 存在
        let placeholder = document.querySelector('.processed-placeholder');
        if (!placeholder) {
            processedContainer.innerHTML = '<h3>- Filtered -</h3><div class="processed-placeholder"><p>click the generate button to start the journey back to 2000s!</p></div>';
        }
        
        previewImage(uploadInput.files[0]);
    }
}

function previewImage(file) {
    const reader = new FileReader();
    reader.onload = e => {
        let preview = document.getElementById('preview-original');
        if (preview) {
            preview.src = e.target.result;
        } else {
            const imgDiv = document.createElement('div');
            imgDiv.innerHTML = `<h3>- Original -</h3><img id="preview-original" src="${e.target.result}">`;
            originalContainer.innerHTML = imgDiv.innerHTML;
        }
    }
    reader.readAsDataURL(file);
}

// 滤镜按钮和生成按钮点击事件
filterButtons.forEach(button => {
    button.addEventListener('click', e => {
        e.preventDefault();
        // 设置隐藏输入框的值
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'filter';
        hiddenInput.value = button.value;
        uploadForm.appendChild(hiddenInput);

        // 移除所有按钮的selected类
        filterButtons.forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');

        // 在生成之前显示“正在生成”的提示
        showGeneratingMessage();
        
        uploadForm.submit();
    });
});

generateButton.addEventListener('click', e => {
    e.preventDefault();
    showGeneratingMessage();
    uploadForm.submit();
});

function showGeneratingMessage() {
    const processedImage = document.getElementById('preview-processed');
    if (processedImage) processedImage.remove();
    const downloadBtn = document.querySelector('.download-btn');
    if (downloadBtn) downloadBtn.remove();
    
    processedContainer.innerHTML = '<h3>- Filtered -</h3><div class="generating-message"><p>generating...</p></div>';
}