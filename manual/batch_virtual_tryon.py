#!/usr/bin/env python3
"""
Batch Virtual Try-On Script
Process multiple clothing items with multiple people
"""

import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gemini_virtual_tryon import GeminiVirtualTryOnClient

def batch_process():
    """Process multiple virtual try-on combinations"""
    
    # Initialize client
    try:
        client = GeminiVirtualTryOnClient()
        print("✅ Gemini Virtual Try-On Client initialized")
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    # Find clothing images (limit to prevent too many API calls)
    clothing_images = []
    for root, dirs, files in os.walk("images"):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                clothing_images.append(os.path.join(root, file))
                if len(clothing_images) >= 3:  # Limit for testing
                    break
        if len(clothing_images) >= 3:
            break
    
    # Find person photos
    person_images = []
    person_photos_dir = "person_photos"
    if os.path.exists(person_photos_dir):
        for file in os.listdir(person_photos_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                person_images.append(os.path.join(person_photos_dir, file))
                if len(person_images) >= 2:  # Limit for testing
                    break
    
    if not clothing_images:
        print("❌ No clothing images found")
        return
    
    if not person_images:
        print("❌ No person images found in person_photos directory")
        return
    
    print(f"👕 Processing {len(clothing_images)} clothing items")
    print(f"🚶‍♂️ With {len(person_images)} people")
    print(f"🔢 Total combinations: {len(clothing_images) * len(person_images)}")
    
    # Custom product types for better results
    product_types = {}
    for clothing_path in clothing_images:
        product_types[clothing_path] = client.detect_product_type(clothing_path)
        print(f"🏷️ {Path(clothing_path).name} → {product_types[clothing_path]}")
    
    # Process batch
    results = client.batch_virtual_tryon(
        clothing_images,
        person_images,
        product_types,
        delay_between_requests=3  # 3 second delay between requests
    )
    
    # Summary
    successful = sum(1 for r in results if r["result"]["success"])
    failed = len(results) - successful
    
    print(f"\n📊 Batch Processing Summary:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Results saved in: virtual_tryons/")
    
    if failed > 0:
        print("\n⚠️ Failed combinations:")
        for r in results:
            if not r["result"]["success"]:
                clothing = Path(r["clothing_image"]).name
                person = Path(r["person_image"]).name
                error = r["result"].get("error", "Unknown")
                print(f"  {clothing} + {person}: {error}")

if __name__ == "__main__":
    batch_process()