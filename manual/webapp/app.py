#!/usr/bin/env python3
"""
Virtual Try-On Web Application
A Flask web interface for the Gemini Virtual Try-On system
"""

import os
import sys
import json
import time
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import requests
from PIL import Image
import uuid

# Add parent directory to path to import our virtual try-on client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_virtual_tryon import GeminiVirtualTryOnClient

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'webapp/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_url(url):
    """Basic validation for image URLs"""
    if not url or not isinstance(url, str):
        return False, "Empty URL"
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    
    # Check for common image extensions
    url_lower = url.lower()
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp']
    
    # Direct image URL
    if any(ext in url_lower for ext in image_extensions):
        return True, "Direct image URL detected"
    
    # Some product URLs might work even without extensions
    if any(site in url_lower for site in ['nike.com', 'zara.com', 'h&m.com', 'uniqlo.com']):
        return True, "Known retailer URL"
    
    return False, "URL may not be a direct image link"

def download_image_from_url(url, filename):
    """Download image from URL and save to uploads folder"""
    try:
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print(f"📥 Downloading image from: {url}")
        response = requests.get(url, timeout=30, verify=False, headers=headers, stream=True)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '').lower()
        print(f"📄 Content-Type: {content_type}")
        
        if not any(img_type in content_type for img_type in ['image/', 'jpeg', 'png', 'webp', 'gif']):
            raise Exception(f"URL does not point to an image. Content-Type: {content_type}")
        
        # Save the raw image first
        temp_filepath = os.path.join(UPLOAD_FOLDER, f"temp_{filename}")
        with open(temp_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"💾 Downloaded {os.path.getsize(temp_filepath)} bytes")
        
        # Validate it's a real image by opening it
        try:
            with Image.open(temp_filepath) as img:
                print(f"🖼️  Image format: {img.format}, Size: {img.size}, Mode: {img.mode}")
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    print("🔄 Converting to RGB...")
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    print(f"🔄 Converting from {img.mode} to RGB...")
                    img = img.convert('RGB')
                
                # Resize if too large
                original_size = img.size
                if img.size[0] > 1024 or img.size[1] > 1024:
                    img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    print(f"📏 Resized: {original_size} → {img.size}")
                
                # Save as JPEG for consistency
                jpeg_filename = filename.rsplit('.', 1)[0] + '.jpg'
                jpeg_filepath = os.path.join(UPLOAD_FOLDER, jpeg_filename)
                img.save(jpeg_filepath, 'JPEG', quality=85, optimize=True)
                print(f"✅ Saved as: {jpeg_filename}")
                
                # Remove temp file
                os.remove(temp_filepath)
                
                return jpeg_filename
                
        except Exception as img_error:
            # Remove temp file on error
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            raise Exception(f"Invalid image file: {str(img_error)}")
            
    except requests.RequestException as req_error:
        raise Exception(f"Failed to download image: {str(req_error)}")
    except Exception as e:
        raise Exception(f"Image processing error: {str(e)}")

@app.route('/')
def index():
    """Main page with upload forms"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and clothing URL"""
    try:
        person_file = None
        clothing_url = request.form.get('clothing_url', '').strip()
        
        # Handle person photo upload
        if 'person_photo' not in request.files:
            flash('No person photo uploaded', 'error')
            return redirect(url_for('index'))
        
        file = request.files['person_photo']
        if file.filename == '':
            flash('No person photo selected', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            person_filename = f"person_{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            person_filepath = os.path.join(UPLOAD_FOLDER, person_filename)
            file.save(person_filepath)
            
            # Process and optimize the person image
            with Image.open(person_filepath) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                if img.size[0] > 1024 or img.size[1] > 1024:
                    img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                img.save(person_filepath, 'JPEG', quality=90, optimize=True)
            
            person_file = person_filepath
        else:
            flash('Invalid person photo format. Use PNG, JPG, JPEG, WebP, or GIF', 'error')
            return redirect(url_for('index'))
        
        # Handle clothing URL
        clothing_file = None
        if clothing_url:
            try:
                print(f"🔗 Processing clothing URL: {clothing_url}")
                
                # Validate URL
                is_valid, validation_message = validate_image_url(clothing_url)
                if not is_valid:
                    raise Exception(validation_message)
                
                print(f"✅ URL validation: {validation_message}")
                
                clothing_filename = f"clothing_{uuid.uuid4().hex[:8]}.jpg"
                actual_filename = download_image_from_url(clothing_url, clothing_filename)
                clothing_file = os.path.join(UPLOAD_FOLDER, actual_filename)
                
                print(f"✅ Successfully processed clothing image: {actual_filename}")
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Clothing processing error: {error_msg}")
                
                # Provide more helpful error messages
                if "cannot identify image file" in error_msg:
                    flash('❌ The downloaded file is not a valid image. Please use a direct image URL (right-click on image → "Copy image address").', 'error')
                elif "Content-Type" in error_msg:
                    flash('❌ The URL does not point to an image file. Please use a direct link to an image.', 'error')
                elif "URL must start with" in error_msg:
                    flash('❌ Please enter a complete URL starting with http:// or https://', 'error')
                elif "Failed to download" in error_msg:
                    flash(f'❌ Could not download the image. Please check the URL and your internet connection.', 'error')
                elif "URL may not be a direct image link" in error_msg:
                    flash('⚠️ This URL may not be a direct image link. Try right-clicking on the image and selecting "Copy image address" instead.', 'error')
                else:
                    flash(f'❌ Error processing image: {error_msg}', 'error')
                
                return redirect(url_for('index'))
        else:
            flash('❌ Please provide a clothing image URL', 'error')
            return redirect(url_for('index'))
        
        # Process virtual try-on
        if person_file and clothing_file:
            return redirect(url_for('process_tryon', 
                                  person_file=os.path.basename(person_file),
                                  clothing_file=os.path.basename(clothing_file)))
        
    except Exception as e:
        flash(f'Upload error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/process/<person_file>/<clothing_file>')
def process_tryon(person_file, clothing_file):
    """Process virtual try-on and display results"""
    person_path = os.path.join(UPLOAD_FOLDER, person_file)
    clothing_path = os.path.join(UPLOAD_FOLDER, clothing_file)
    
    # Verify files exist
    if not os.path.exists(person_path) or not os.path.exists(clothing_path):
        flash('Required files not found', 'error')
        return redirect(url_for('index'))
    
    try:
        # Initialize Gemini client
        client = GeminiVirtualTryOnClient()
        
        # Detect product type
        product_type = client.detect_product_type(clothing_path)
        
        # Process virtual try-on
        result = client.process_virtual_tryon(
            clothing_path,
            person_path,
            product_type=product_type,
            style_preference="natural and realistic"
        )
        
        # Parse the result
        analysis_text = "Virtual try-on processing failed."
        if result["success"] and "data" in result:
            candidates = result["data"].get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    analysis_text = parts[0].get("text", "No analysis available.")
        
        return render_template('results.html',
                             person_image=person_file,
                             clothing_image=clothing_file,
                             product_type=product_type,
                             analysis=analysis_text,
                             success=result["success"],
                             error=result.get("error") if not result["success"] else None)
    
    except Exception as e:
        return render_template('results.html',
                             person_image=person_file,
                             clothing_image=clothing_file,
                             product_type="unknown",
                             analysis="",
                             success=False,
                             error=str(e))

@app.route('/api/tryon', methods=['POST'])
def api_tryon():
    """API endpoint for virtual try-on"""
    try:
        data = request.get_json()
        clothing_url = data.get('clothing_url')
        person_image = data.get('person_image')  # base64 encoded
        
        if not clothing_url or not person_image:
            return jsonify({"success": False, "error": "Missing required parameters"})
        
        # TODO: Implement API processing
        return jsonify({"success": True, "message": "API endpoint under development"})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/debug/test-url', methods=['POST'])
def debug_test_url():
    """Debug endpoint to test URL downloads"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"success": False, "error": "No URL provided"})
        
        print(f"🔍 Debug testing URL: {url}")
        
        # Test validation
        is_valid, validation_message = validate_image_url(url)
        
        result = {
            "url": url,
            "validation": {
                "is_valid": is_valid,
                "message": validation_message
            }
        }
        
        if is_valid:
            try:
                # Test download
                test_filename = f"debug_{uuid.uuid4().hex[:8]}.jpg"
                actual_filename = download_image_from_url(url, test_filename)
                
                filepath = os.path.join(UPLOAD_FOLDER, actual_filename)
                file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
                
                result["download"] = {
                    "success": True,
                    "filename": actual_filename,
                    "file_size": file_size
                }
                
                # Clean up debug file
                if os.path.exists(filepath):
                    os.remove(filepath)
                
            except Exception as download_error:
                result["download"] = {
                    "success": False,
                    "error": str(download_error)
                }
        
        return jsonify({"success": True, "result": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash("File is too large. Maximum size is 16MB.", 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🌟 Starting Virtual Try-On Web Application")
    print("🔗 Access the application at: http://localhost:5000")
    print("📁 Uploads will be saved to:", UPLOAD_FOLDER)
    
    # Check if API key is configured
    try:
        client = GeminiVirtualTryOnClient()
        print("✅ Gemini API key configured successfully")
    except ValueError:
        print("⚠️  Warning: Gemini API key not found. Please configure GOOGLE_GEMINI_API_KEY in .env")
    
    app.run(debug=True, host='0.0.0.0', port=5000)