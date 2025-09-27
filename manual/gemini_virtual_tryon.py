#!/usr/bin/env python3
"""
Google Gemini Flash 2.5 Virtual Try-On Client
Uses Gemini's image generation capabilities to show how clothing products look on people
"""

import os
import sys
import json
import base64
import time
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import mimetypes
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

class GeminiVirtualTryOnClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini Virtual Try-On client"""
        self.api_key = api_key or os.getenv('GOOGLE_GEMINI_API_KEY') or os.getenv('GOOGLE_VEO2_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set GOOGLE_GEMINI_API_KEY environment variable or pass api_key parameter")
        
        # Google Gemini API endpoints
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model_name = "gemini-1.5-pro-latest"  # Use Gemini 1.5 Pro for image analysis
        
        # Supported image formats
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
        
    def encode_image_to_base64(self, image_path: str, max_size: Tuple[int, int] = (1024, 1024)) -> Tuple[str, str]:
        """Encode image to base64 string with compression and MIME type"""
        try:
            # Open and potentially resize the image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if image is too large
                original_size = img.size
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                if img.size != original_size:
                    print(f"📏 Resized {Path(image_path).name}: {original_size} → {img.size}")
                
                # Save to bytes with compression
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG', quality=85, optimize=True)
                img_bytes.seek(0)
                
                # Encode to base64
                encoded_string = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
                
                # Calculate size reduction
                original_size_kb = os.path.getsize(image_path) / 1024
                compressed_size_kb = len(encoded_string) * 3 / 4 / 1024  # Rough estimate
                print(f"💾 Compressed {Path(image_path).name}: {original_size_kb:.1f}KB → {compressed_size_kb:.1f}KB")
            
            return encoded_string, 'image/jpeg'
            
        except Exception as e:
            print(f"Error encoding image {image_path}: {e}")
            return None, None

    def create_virtual_tryon_prompt(self, 
                                  product_type: str = "clothing item",
                                  style_preference: str = "natural and realistic") -> str:
        """Create a detailed prompt for virtual try-on analysis"""
        
        base_prompt = f"""You are a fashion expert and virtual stylist. Analyze these two images:

1. First image: A {product_type} (clothing product)
2. Second image: A person

Please provide a detailed analysis of how this {product_type} would look when worn by this person. Consider:

VISUAL ANALYSIS:
- The person's body type, proportions, and build
- How the {product_type}'s size, cut, and style would complement their figure
- Color coordination with the person's skin tone and features
- Style compatibility with the person's apparent age and appearance

FIT ASSESSMENT:
- How well the garment would fit based on the person's visible proportions
- Areas where the fit would be excellent, good, or might need adjustment
- Size recommendations if the fit seems off

STYLING RECOMMENDATIONS:
- How to best style this {product_type} on this person
- Complementary pieces that would work well
- Styling tips to enhance the overall look
- Color combinations that would work best

OVERALL VERDICT:
- Rate the fit from 1-10 and explain why
- Whether this {product_type} is recommended for this person
- Any specific styling advice

Please be detailed, helpful, and constructive in your analysis. Focus on {style_preference} styling approach."""

        return base_prompt

    def create_gemini_request(self, 
                            clothing_image_path: str,
                            person_image_path: str,
                            product_type: str = "clothing item",
                            style_preference: str = "natural and realistic",
                            custom_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Create a Gemini API request for virtual try-on"""
        
        # Encode both images
        clothing_b64, clothing_mime = self.encode_image_to_base64(clothing_image_path)
        person_b64, person_mime = self.encode_image_to_base64(person_image_path)
        
        if not clothing_b64 or not person_b64:
            return None
        
        # Use custom prompt or generate one
        prompt = custom_prompt or self.create_virtual_tryon_prompt(product_type, style_preference)
        
        request_payload = {
            "contents": [{
                "parts": [
                    {
                        "text": prompt
                    },
                    {
                        "inline_data": {
                            "mime_type": clothing_mime,
                            "data": clothing_b64
                        }
                    },
                    {
                        "inline_data": {
                            "mime_type": person_mime,
                            "data": person_b64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        
        return request_payload

    def send_gemini_request(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to Gemini API"""
        try:
            endpoint = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            print(f"🔗 Sending request to: {self.model_name}")
            print(f"📦 Payload size: {len(str(request_payload))} characters")
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=request_payload,
                timeout=60
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                print(f"❌ Error response: {response.text[:200]}...")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            print(f"🚨 Connection error: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": None
            }

    def process_virtual_tryon(self,
                            clothing_image_path: str,
                            person_image_path: str,
                            product_type: str = "clothing item",
                            style_preference: str = "natural and realistic",
                            custom_prompt: Optional[str] = None,
                            output_dir: str = "virtual_tryons") -> Dict[str, Any]:
        """Process a virtual try-on request"""
        
        # Validate input files
        if not os.path.exists(clothing_image_path):
            return {"success": False, "error": f"Clothing image not found: {clothing_image_path}"}
        
        if not os.path.exists(person_image_path):
            return {"success": False, "error": f"Person image not found: {person_image_path}"}
        
        # Check image formats
        for path in [clothing_image_path, person_image_path]:
            ext = Path(path).suffix.lower()
            if ext not in self.supported_formats:
                return {"success": False, "error": f"Unsupported image format: {ext} in {path}"}
        
        print(f"👕 Clothing: {clothing_image_path}")
        print(f"👤 Person: {person_image_path}")
        print(f"📝 Product type: {product_type}")
        
        # Create request payload
        request_payload = self.create_gemini_request(
            clothing_image_path, 
            person_image_path, 
            product_type, 
            style_preference,
            custom_prompt
        )
        
        if not request_payload:
            return {"success": False, "error": "Failed to create request payload"}
        
        # Send request to API
        print("🚀 Sending virtual try-on request...")
        response = self.send_gemini_request(request_payload)
        
        # Save response to file
        os.makedirs(output_dir, exist_ok=True)
        clothing_name = Path(clothing_image_path).stem
        person_name = Path(person_image_path).stem
        response_file = os.path.join(output_dir, f"{clothing_name}_on_{person_name}_response.json")
        
        result_data = {
            "clothing_image": clothing_image_path,
            "person_image": person_image_path,
            "product_type": product_type,
            "style_preference": style_preference,
            "custom_prompt": custom_prompt,
            "response": response,
            "timestamp": time.time()
        }
        
        with open(response_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        print(f"💾 Response saved to: {response_file}")
        
        # Display results if successful
        if response["success"] and "data" in response:
            try:
                candidates = response["data"].get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        analysis_text = parts[0].get("text", "")
                        if analysis_text:
                            print("\n✨ Virtual Try-On Analysis:")
                            print("=" * 50)
                            print(analysis_text)
                            print("=" * 50)
            except Exception as e:
                print(f"⚠️ Could not display analysis: {e}")
        
        return response

    def batch_virtual_tryon(self,
                          clothing_images: List[str],
                          person_images: List[str],
                          product_types: Optional[Dict[str, str]] = None,
                          delay_between_requests: int = 2) -> List[Dict[str, Any]]:
        """Process multiple virtual try-on combinations"""
        
        results = []
        product_types = product_types or {}
        
        total_combinations = len(clothing_images) * len(person_images)
        current = 0
        
        print(f"🔄 Processing {total_combinations} virtual try-on combinations...")
        
        for clothing_path in clothing_images:
            for person_path in person_images:
                current += 1
                print(f"\n--- Combination {current}/{total_combinations} ---")
                
                # Determine product type
                product_type = product_types.get(clothing_path, self.detect_product_type(clothing_path))
                
                result = self.process_virtual_tryon(
                    clothing_path,
                    person_path,
                    product_type
                )
                
                results.append({
                    "clothing_image": clothing_path,
                    "person_image": person_path,
                    "product_type": product_type,
                    "result": result
                })
                
                # Add delay between requests
                if current < total_combinations and delay_between_requests > 0:
                    print(f"⏱️ Waiting {delay_between_requests} seconds...")
                    time.sleep(delay_between_requests)
        
        return results

    def detect_product_type(self, image_path: str) -> str:
        """Detect product type from image path/name"""
        path_lower = image_path.lower()
        
        if any(term in path_lower for term in ['shirt', 'tshirt', 't-shirt', 'polo', 'blouse', 'top']):
            return "shirt"
        elif any(term in path_lower for term in ['pant', 'trouser', 'jean', 'short']):
            return "pants"
        elif any(term in path_lower for term in ['dress', 'gown']):
            return "dress"
        elif any(term in path_lower for term in ['jacket', 'coat', 'blazer', 'hoodie', 'sweater']):
            return "outerwear"
        elif any(term in path_lower for term in ['shoe', 'sneaker', 'boot', 'sandal']):
            return "footwear"
        else:
            return "clothing item"

def find_images_by_type(directory: str, image_type: str) -> List[str]:
    """Find images in directory, optionally filtered by type"""
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
    image_paths = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                if image_type == "all" or image_type.lower() in file.lower() or image_type.lower() in root.lower():
                    image_paths.append(os.path.join(root, file))
    
    return sorted(image_paths)

def main():
    """Main function for virtual try-on processing"""
    
    # Initialize client
    try:
        client = GeminiVirtualTryOnClient()
        print("✅ Gemini Virtual Try-On Client initialized")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your Google Gemini API key:")
        print("export GOOGLE_GEMINI_API_KEY='your-api-key'")
        return
    
    # Example usage
    print("\n🔍 Looking for clothing and person images...")
    
    # Find clothing images in your products folder
    clothing_images = find_images_by_type("images", "all")[:3]  # Limit for testing
    
    # You'll need to add person photos to test with
    person_images_dir = "person_photos"
    if not os.path.exists(person_images_dir):
        os.makedirs(person_images_dir)
        print(f"📁 Created {person_images_dir} directory")
        print("🚶‍♂️ Please add person photos to this directory for virtual try-on")
        return
    
    person_images = find_images_by_type(person_images_dir, "all")
    
    if not clothing_images:
        print("❌ No clothing images found in images directory")
        return
    
    if not person_images:
        print("❌ No person images found in person_photos directory")
        print("🚶‍♂️ Please add person photos to the person_photos directory")
        return
    
    print(f"👕 Found {len(clothing_images)} clothing items")
    print(f"🚶‍♂️ Found {len(person_images)} person photos")
    
    # Process virtual try-ons
    if len(clothing_images) > 0 and len(person_images) > 0:
        # Test with first combination
        result = client.process_virtual_tryon(
            clothing_images[0],
            person_images[0],
            product_type=client.detect_product_type(clothing_images[0])
        )
        
        if result["success"]:
            print("✅ Virtual try-on completed successfully!")
        else:
            print(f"❌ Virtual try-on failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()