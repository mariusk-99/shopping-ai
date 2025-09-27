# 🌟 Virtual Try-On Web Application

A beautiful, user-friendly web interface for AI-powered virtual try-on using Google Gemini.

## 🚀 Quick Start

### 1. Navigate to the correct directory
```bash
cd /Users/mariuskornovan/hackathon-tomoro/shopping-ai/manual
```

### 2. Install dependencies (if not already installed)
```bash
python3 -m pip install Flask python-dotenv Pillow requests
```

### 3. Start the web application
```bash
cd webapp
python3 app.py
```

### 4. Open in your browser
- **Local access:** http://localhost:5000
- **Network access:** http://0.0.0.0:5000

## 🎨 Features

### ✨ Modern Web Interface
- **Drag & Drop Upload**: Easy photo upload with visual feedback
- **URL Input**: Paste clothing image links directly  
- **Live Preview**: See images before processing
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Professional Styling**: Clean, modern UI with Tailwind CSS

### 🤖 AI-Powered Analysis
- **Smart Product Detection**: Automatically identifies clothing types
- **Detailed Fashion Analysis**: Comprehensive fit and style assessment
- **Professional Results**: Detailed analysis with styling recommendations
- **Error Handling**: Graceful error handling with helpful messages

### 📱 User Experience
- **Step-by-Step Guide**: Clear instructions for best results
- **Photo Guidelines**: Tips for optimal photo quality
- **Loading States**: Visual feedback during processing
- **Print Support**: Save or print results

## 📁 File Structure
```
webapp/
├── app.py                  # Main Flask application
├── templates/
│   ├── index.html         # Upload form page
│   └── results.html       # Results display page
├── static/                # CSS, JS, images (auto-created)
├── uploads/              # User uploaded files (auto-created)
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
GOOGLE_GEMINI_API_KEY=your-api-key-here
FLASK_SECRET_KEY=your-secret-key-here  # Optional
```

### API Key Setup
1. Get your Google Gemini API key from: https://aistudio.google.com/app/apikey
2. Add it to your `.env` file in the `manual/` directory
3. The app will automatically load the configuration

## 🖼️ How to Use

### Step 1: Upload Your Photo
- Click the upload area or drag & drop your photo
- Use a clear, front-facing photo with good lighting
- Supported formats: PNG, JPG, JPEG, WebP, GIF
- Maximum file size: 16MB

### Step 2: Add Clothing URL
- Paste a direct image URL of the clothing item
- Works with most e-commerce sites (Nike, Zara, H&M, etc.)
- Right-click on product images and "Copy image address"
- The system will download and process the image automatically

### Step 3: Get AI Analysis
- Click "Create Virtual Try-On"
- Wait 30-60 seconds for AI processing
- View detailed analysis with fit assessment and recommendations

## 🛠️ Technical Details

### Backend Features
- **Flask Web Framework**: Lightweight and fast
- **Secure File Handling**: Safe file uploads with validation
- **Image Processing**: Automatic resizing and optimization
- **API Integration**: Seamless connection to Gemini API
- **Error Recovery**: Robust error handling and logging

### Frontend Features
- **Tailwind CSS**: Modern, responsive styling
- **Font Awesome Icons**: Professional iconography  
- **Vanilla JavaScript**: Fast, lightweight interactions
- **Progressive Enhancement**: Works without JavaScript
- **Print Styling**: Optimized for printing results

## 📊 API Endpoints

### Web Routes
- `GET /` - Main upload form
- `POST /upload` - Handle file uploads and processing
- `GET /process/<person_file>/<clothing_file>` - Process virtual try-on
- `GET /uploads/<filename>` - Serve uploaded files

### API Routes (Future)
- `POST /api/tryon` - JSON API for virtual try-on

## 🔍 Troubleshooting

### Common Issues

**"API key not found"**
- Ensure `GOOGLE_GEMINI_API_KEY` is set in your `.env` file
- Check that the `.env` file is in the `manual/` directory

**"Connection error"**
- Check your internet connection
- Verify the API key is valid and has proper permissions
- Try with smaller image files

**"File upload failed"**
- Check file format (PNG, JPG, JPEG, WebP, GIF only)
- Ensure file size is under 16MB
- Try with different images

**"Clothing image download failed"**
- Ensure the URL is a direct image link
- Try right-clicking and "Copy image address"
- Some sites block direct image access

## 🎯 Best Practices

### For Person Photos
- Face the camera directly
- Use natural or bright, even lighting
- Keep arms slightly away from body
- Use simple, uncluttered background
- Higher resolution images work better

### For Clothing URLs
- Use direct image URLs ending in .jpg, .png, etc.
- Right-click on product images for best results
- Avoid URLs with redirects or parameters
- Test the URL by opening it in a new tab

## 🔒 Security Features
- Secure file name generation
- File type validation
- Size limits on uploads
- Automatic cleanup of temporary files
- CSRF protection with secret keys

## 🚀 Deployment Ready
- Production-ready Flask configuration
- Environment variable management
- Error logging and handling
- Scalable architecture
- Docker-friendly structure

This web application provides a professional, user-friendly interface for your AI virtual try-on system! 🎨✨