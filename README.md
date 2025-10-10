# 2000s Filter Lab - Retro Photo Filter Generator

A nostalgic photo filter web application that transforms your photos with authentic 2000s-style effects including CCD camera aesthetics, VHS filters, Y2K vibes, and vintage film looks.

![2000s Filter Lab](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🎨 Multiple Filter Categories**:
  - **Basic**: CCD, Vintage, Lomo, Dreamy
  - **Vintage**: Kodachrome, Fuji Superia, Agfa, Retro Green, Dark Brown, VHS
  - **Y2K Style**: Cyberpunk, Neon Pop, Cyber Pink, Y2K Purple, Millennium Gold
  - **Special Effects**: Vaporwave, Glitch, Matrix Green, Disco Fever, Tech Silver
  - **Advanced**: Digital Cam, Retro Blue, Misty Gray, Cloudy Dream, Foggy Memory

- **📱 Interactive Features**:
  - Drag & drop image upload
  - Real-time preview
  - Interactive filter comparison sliders
  - Responsive design for all devices
  - Processing animation with rotating loader

- **🚀 Performance**:
  - Fast image processing
  - Support for multiple formats (JPEG, PNG, BMP, GIF, TIFF, WEBP)
  - Up to 50MB file size support
  - Up to 4K resolution processing

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Image Processing**: PIL (Pillow)
- **Styling**: Modern CSS with glassmorphism effects
- **Deployment**: Railway (with Docker support)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/2000s-filter-app-revised-4.git
   cd 2000s-filter-app-revised-4
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to `http://localhost:5000`

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t 2000s-filter-app .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 2000s-filter-app
   ```

## 📁 Project Structure

```
2000s-filter-app-revised-4/
├── app.py                 # Main Flask application
├── filters.py            # Image processing filters
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── Procfile             # Railway deployment config
├── railway.json         # Railway service configuration
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   ├── js/
│   │   └── script.js    # Frontend JavaScript
│   └── examples/        # Example images
├── templates/
│   ├── index.html       # Main page
│   ├── about.html       # About page
│   ├── contact.html     # Contact page
│   └── faq.html         # FAQ page
└── README.md            # This file
```

## 🎯 Usage

1. **Upload an Image**: Drag and drop or click to select an image file
2. **Choose a Filter**: Browse through different filter categories and select your preferred effect
3. **Generate**: Click the "Generate" button to apply the filter
4. **Download**: Save your filtered image to your device

## 🌟 Filter Categories

### Basic Filters
- **CCD**: Authentic CCD camera sensor look
- **Vintage**: Classic film photography aesthetic
- **Lomo**: Lomography-style effects
- **Dreamy**: Soft, ethereal appearance

### Vintage Collection
- **Kodachrome**: Iconic Kodak film simulation
- **Fuji Superia**: Fujifilm color palette
- **Agfa**: German film stock characteristics
- **VHS**: Retro video tape distortion effects

### Y2K Style
- **Cyberpunk**: Futuristic neon aesthetics
- **Neon Pop**: Bright, vibrant colors
- **Cyber Pink**: Hot pink and electric vibes
- **Millennium Gold**: Metallic gold tones

### Special Effects
- **Vaporwave**: Synthwave and retro-futuristic
- **Glitch**: Digital distortion effects
- **Matrix Green**: Classic green terminal look
- **Disco Fever**: 70s disco vibes

## 🔧 Configuration

The application can be configured through environment variables:

- `FLASK_ENV`: Set to 'production' for production deployment
- `PORT`: Port number for the application (default: 5000)

## 📱 Mobile Support

The application is fully responsive and works seamlessly on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the nostalgic aesthetics of the early 2000s
- Built with love for retro photography enthusiasts
- Thanks to the open-source community for the amazing tools and libraries

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact us through the website
- Check out our FAQ page

---

**Made with ❤️ for nostalgic memories**

*Transform your photos and relive the magic of the 2000s!*
