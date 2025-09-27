#!/usr/bin/env python3
"""
Webpage Product Image Scraper
Fetches HTML from product page URLs and extracts product images with titles.
"""

import re
import os
import requests
import time
import warnings
from urllib.parse import urlparse, urljoin, unquote
from bs4 import BeautifulSoup
from collections import defaultdict

# Disable SSL warnings for development
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

def fetch_webpage_html(url, max_retries=3):
    """Fetch HTML content from a webpage URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30, verify=False)
            response.raise_for_status()
            return response.text, None
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"    Attempt {attempt + 1} failed, retrying: {str(e)[:50]}...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return None, f"Failed after {max_retries} attempts: {str(e)[:100]}"
    
    return None, "Failed to fetch webpage"

def extract_product_title_from_html(html_content, url):
    """Extract product title from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common selectors for product titles (ordered by priority)
        title_selectors = [
            # E-commerce specific
            '[data-testid="product-title"]',
            '.product-title',
            '.product-name',
            '.pdp-title',
            '.product-details-title',
            '.item-title',
            '.merchandise-product-details__product-name',
            
            # Nike specific
            '.headline-5',
            '.product-title',
            '.nds-text',
            
            # Temu specific  
            '.goods-title',
            '.product-title-text',
            
            # Shein specific
            '.goods-detail-v3__title',
            '.product-intro__head-name',
            
            # Boohoo specific
            '.product-title',
            '.b-product_summary-title',
            
            # Generic selectors
            'h1.title',
            'h1.product',
            'h1[class*="title"]',
            'h1[class*="product"]',
            'h1[class*="name"]',
            '.title h1',
            '.product h1',
            '.name h1',
            
            # Fallback to any h1
            'h1',
            
            # Last resort - page title
            'title'
        ]
        
        for selector in title_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                # Filter out very short, very long, or generic titles
                if text and 5 <= len(text) <= 200 and not text.lower() in ['home', 'shop', 'products', 'search']:
                    # Clean up the title
                    cleaned_title = re.sub(r'\s+', ' ', text)
                    cleaned_title = re.sub(r'[^\w\s\-\&\.\,\!\?]', '', cleaned_title)
                    return cleaned_title.strip()
        
        # If no product title found, try to extract from URL
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        if path_parts:
            # Look for product-like path segments
            for part in reversed(path_parts):
                if len(part) > 5 and not part.isdigit():
                    # Convert URL slug to readable title
                    title = part.replace('-', ' ').replace('_', ' ').title()
                    return title[:100]  # Limit length
        
        return "Unknown Product"
        
    except Exception as e:
        print(f"    Error extracting title: {str(e)[:50]}")
        return "Unknown Product"

def extract_images_from_html(html_content, base_url):
    """Extract image URLs from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all img tags
        img_tags = soup.find_all('img')
        
        image_urls = set()
        
        for img in img_tags:
            # Get image URL from various attributes
            img_url = None
            for attr in ['src', 'data-src', 'data-lazy-src', 'data-original', 'data-zoom-image']:
                if img.get(attr):
                    img_url = img[attr]
                    break
            
            if img_url:
                # Convert relative URLs to absolute
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url
                elif img_url.startswith('/'):
                    img_url = urljoin(base_url, img_url)
                elif not img_url.startswith('http'):
                    img_url = urljoin(base_url, img_url)
                
                # Filter for actual product images (skip very small images, icons, etc.)
                if is_product_image(img_url, img):
                    image_urls.add(img_url)
        
        return list(image_urls)
        
    except Exception as e:
        print(f"    Error extracting images: {str(e)[:50]}")
        return []

def is_product_image(img_url, img_tag):
    """Determine if an image is likely a product image"""
    # Skip very small images (likely icons or UI elements)
    width = img_tag.get('width')
    height = img_tag.get('height')
    
    if width and height:
        try:
            w, h = int(width), int(height)
            if w < 100 or h < 100:
                return False
        except ValueError:
            pass
    
    # Skip common non-product image patterns
    skip_patterns = [
        'icon', 'logo', 'arrow', 'button', 'badge', 'star', 'rating',
        'social', 'facebook', 'twitter', 'instagram', 'pinterest',
        'cart', 'bag', 'wishlist', 'heart', 'share', 'zoom', 'play',
        'avatar', 'profile', 'user', 'account', 'search', 'menu',
        'footer', 'header', 'nav', 'banner', 'ad', 'promo',
        'tracking', 'pixel', 'analytics', 'gtm', 'facebook', 'google'
    ]
    
    img_url_lower = img_url.lower()
    img_alt = (img_tag.get('alt') or '').lower()
    img_class = ' '.join(img_tag.get('class', [])).lower()
    
    for pattern in skip_patterns:
        if pattern in img_url_lower or pattern in img_alt or pattern in img_class:
            return False
    
    # Must be a reasonable image format
    img_formats = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg']
    if not any(fmt in img_url_lower for fmt in img_formats):
        return False
    
    return True

def create_images_folder(images_dir, website_name):
    """Create folder structure for organizing downloaded images"""
    website_images_dir = os.path.join(images_dir, website_name)
    os.makedirs(website_images_dir, exist_ok=True)
    return website_images_dir

def generate_image_filename(img_url, product_title, index=0):
    """Generate a unique filename for downloaded images"""
    # Parse URL to get original filename and extension
    parsed_url = urlparse(img_url)
    path = unquote(parsed_url.path)
    
    # Extract original filename and extension
    original_name = os.path.basename(path)
    if '.' in original_name:
        name, ext = os.path.splitext(original_name)
        # Remove query parameters from extension if any
        ext = ext.split('?')[0]
    else:
        # Extract extension from query parameters if available
        query = parsed_url.query
        if 'format=' in query:
            ext = '.' + query.split('format=')[1].split('&')[0]
        else:
            ext = '.jpg'  # default extension
        name = original_name or 'image'
    
    # Create a clean product-based filename
    if product_title and product_title != 'Unknown Product':
        # Clean product title for filename
        clean_title = re.sub(r'[^\w\s\-]', '', product_title.strip())
        clean_title = re.sub(r'\s+', '_', clean_title)
        base_name = clean_title[:50]  # Limit length
    else:
        base_name = name[:50]
    
    # Add index if provided
    if index > 0:
        filename = f"{base_name}_{index}{ext}"
    else:
        filename = f"{base_name}{ext}"
    
    return filename

def download_image(url, filepath, max_retries=2):
    """Download an image from URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=20, verify=False)
            response.raise_for_status()
            
            # Write the image to file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True, f"Downloaded ({len(response.content)} bytes)"
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                return False, f"Failed: {str(e)[:50]}..."
    
    return False, "Download failed"

def process_webpage_url(url, website_name, images_dir="images"):
    """Process a single webpage URL to extract product info and images"""
    print(f"  Processing: {url}")
    
    # Fetch HTML content
    html_content, error = fetch_webpage_html(url)
    if not html_content:
        print(f"    ✗ Failed to fetch webpage: {error}")
        return {
            'url': url,
            'success': False,
            'error': error,
            'product_title': None,
            'images': [],
            'downloaded_images': []
        }
    
    # Extract product title
    product_title = extract_product_title_from_html(html_content, url)
    print(f"    Product: {product_title}")
    
    # Extract image URLs
    image_urls = extract_images_from_html(html_content, url)
    print(f"    Found {len(image_urls)} product images")
    
    # Download images
    downloaded_images = []
    if image_urls:
        website_images_dir = create_images_folder(images_dir, website_name)
        
        # Limit downloads for testing
        max_downloads = min(5, len(image_urls))
        for i, img_url in enumerate(image_urls[:max_downloads]):
            filename = generate_image_filename(img_url, product_title, i)
            filepath = os.path.join(website_images_dir, filename)
            
            if os.path.exists(filepath):
                print(f"      Skipping {filename} (exists)")
                downloaded_images.append(filepath)
                continue
            
            print(f"      Downloading {filename}...")
            success, message = download_image(img_url, filepath)
            
            if success:
                downloaded_images.append(filepath)
                print(f"        ✓ {message}")
            else:
                print(f"        ✗ {message}")
        
        if len(image_urls) > max_downloads:
            print(f"    Limited to {max_downloads} downloads (found {len(image_urls)} total)")
    
    return {
        'url': url,
        'success': True,
        'product_title': product_title,
        'images': image_urls,
        'downloaded_images': downloaded_images,
        'total_images_found': len(image_urls),
        'total_images_downloaded': len(downloaded_images)
    }

def process_url_file(file_path, output_dir="output", images_dir="images"):
    """Process a text file containing URLs"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    # Get website name from filename
    website_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"\nProcessing {website_name} URLs from {file_path}")
    
    # Read URLs from file
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and line.startswith('http'):
                    urls.append(line)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not urls:
        print("No valid URLs found in file")
        return
    
    print(f"Found {len(urls)} URLs to process")
    
    results = []
    total_images_downloaded = 0
    
    for url in urls[:3]:  # Limit to first 3 URLs for testing
        result = process_webpage_url(url, website_name, images_dir)
        results.append(result)
        total_images_downloaded += result.get('total_images_downloaded', 0)
        print()  # Add spacing between URLs
    
    # Summary
    successful = len([r for r in results if r['success']])
    print(f"Summary for {website_name}:")
    print(f"  URLs processed: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Total images downloaded: {total_images_downloaded}")
    
    return results

def main():
    """Main function to process URL files"""
    # Look for URL files in urls folder
    urls_folder = "urls"
    if not os.path.exists(urls_folder):
        print(f"Creating {urls_folder} folder...")
        os.makedirs(urls_folder, exist_ok=True)
        print(f"Please add text files with URLs to the {urls_folder} folder")
        return
    
    # Find text files in urls folder
    url_files = [f for f in os.listdir(urls_folder) if f.endswith('.txt')]
    
    if not url_files:
        print(f"No .txt files found in {urls_folder} folder")
        print("Please add text files containing URLs (one per line)")
        return
    
    print(f"Found {len(url_files)} URL files: {url_files}")
    
    # Process each file
    for url_file in url_files:
        file_path = os.path.join(urls_folder, url_file)
        process_url_file(file_path)

if __name__ == "__main__":
    main()