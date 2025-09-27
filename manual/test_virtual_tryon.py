#!/usr/bin/env python3
"""
Simple test script for Gemini Virtual Try-On
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_virtual_tryon import GeminiVirtualTryOnClient

def test_virtual_tryon():
    """Test virtual try-on with sample images"""
    
    # Initialize client
    try:
        client = GeminiVirtualTryOnClient()
        print("✅ Gemini Virtual Try-On Client initialized")
    except ValueError as e:
        print(f"❌ {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Get your Google API key from: https://aistudio.google.com/app/apikey")
        print("2. Add it to your .env file:")
        print("   echo 'GOOGLE_GEMINI_API_KEY=your-api-key-here' >> .env")
        return
    
    # Look for sample images
    clothing_images = []
    for root, dirs, files in os.walk("images"):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                clothing_images.append(os.path.join(root, file))
                break  # Just get one for testing
        if clothing_images:
            break
    
    if not clothing_images:
        print("❌ No clothing images found in images directory")
        return
    
    # Check for person photos
    person_photos_dir = "person_photos"
    if not os.path.exists(person_photos_dir):
        os.makedirs(person_photos_dir)
        print(f"📁 Created {person_photos_dir} directory")
    
    person_images = []
    if os.path.exists(person_photos_dir):
        for file in os.listdir(person_photos_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                person_images.append(os.path.join(person_photos_dir, file))
                break  # Just get one for testing
    
    if not person_images:
        print("🚶‍♂️ No person photos found!")
        print(f"\n📸 Please add person photos to: {person_photos_dir}/")
        print("Examples:")
        print("- person1.jpg (front-facing photo of a person)")
        print("- model.png (person in casual pose)")
        print("\n💡 Tips for best results:")
        print("- Use clear, well-lit photos")
        print("- Person should be facing the camera")
        print("- Avoid busy backgrounds")
        print("- Higher resolution is better")
        return
    
    # Test virtual try-on
    clothing_path = clothing_images[0]
    person_path = person_images[0]
    
    print(f"\n🧪 Testing virtual try-on:")
    print(f"👕 Clothing: {clothing_path}")
    print(f"🚶‍♂️ Person: {person_path}")
    
    # Detect product type from clothing image
    product_type = client.detect_product_type(clothing_path)
    print(f"🏷️ Detected product type: {product_type}")
    
    # Process virtual try-on
    result = client.process_virtual_tryon(
        clothing_path,
        person_path,
        product_type=product_type,
        style_preference="natural and realistic"
    )
    
    if result["success"]:
        print("\n🎉 Virtual try-on completed successfully!")
        print("📁 Check virtual_tryons/ folder for detailed results")
    else:
        print(f"\n❌ Virtual try-on failed:")
        print(f"Error: {result.get('error', 'Unknown error')}")
        if result.get('status_code'):
            print(f"Status code: {result['status_code']}")

if __name__ == "__main__":
    test_virtual_tryon()