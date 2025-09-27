#!/usr/bin/env python3
"""
Test script for debugging image URL downloads
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from webapp.app import download_image_from_url, validate_image_url
import tempfile

def test_url(url):
    """Test downloading an image from a URL"""
    print(f"\n🔍 Testing URL: {url}")
    
    # Test URL validation
    is_valid, message = validate_image_url(url)
    print(f"📋 Validation: {'✅ PASS' if is_valid else '❌ FAIL'} - {message}")
    
    if not is_valid:
        print("⏭️  Skipping download due to validation failure")
        return False
    
    # Test download
    try:
        temp_filename = f"test_{os.urandom(4).hex()}.jpg"
        result_filename = download_image_from_url(url, temp_filename)
        print(f"✅ Download successful: {result_filename}")
        
        # Check if file exists and has content
        filepath = os.path.join("webapp/uploads", result_filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"📁 File size: {size} bytes")
            if size > 0:
                print("✅ File appears to be valid")
                return True
            else:
                print("❌ File is empty")
                return False
        else:
            print(f"❌ File not found: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return False

def main():
    """Test various types of URLs"""
    
    # Create uploads directory if it doesn't exist
    os.makedirs("webapp/uploads", exist_ok=True)
    
    print("🧪 Image URL Download Tester")
    print("=" * 50)
    
    # Test URLs
    test_urls = [
        # Direct image URLs
        "https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco/61734ec7-dad8-40f3-9b95-c7500939150a/dri-fit-form-mens-18cm-brief-lined-running-shorts-d9r0kw.png",
        
        # Common e-commerce image patterns
        "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/8f93f6cdbdc74c8b95fdbecaa8ed09cc_9366/Essentials_French_Terry_3-Stripes_Pants_Black_H12024_21_model.jpg",
        
        # User input (you can add your problematic URL here)
        # "paste_your_problematic_url_here"
    ]
    
    if len(sys.argv) > 1:
        # Test URL provided as command line argument
        test_urls = [sys.argv[1]]
    
    successful = 0
    total = len(test_urls)
    
    for url in test_urls:
        success = test_url(url)
        if success:
            successful += 1
    
    print(f"\n📊 Results: {successful}/{total} URLs processed successfully")
    
    if successful < total:
        print("\n💡 Tips for better results:")
        print("• Right-click on product images and select 'Copy image address'")
        print("• Avoid using page URLs - use direct image URLs instead")
        print("• Look for URLs ending in .jpg, .png, .webp, etc.")
        print("• Some websites block automated downloads")

if __name__ == "__main__":
    main()