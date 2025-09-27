# We'll parse multiple HTML files from a folder, extract image URLs, dedupe them,
# and categorize by Nike's CDN size presets (t_default vs t_PDP_*).
import re
import os
import glob
import hashlib
import requests
import time
import warnings
from urllib.parse import urlparse, unquote
from collections import defaultdict

# Disable SSL warnings for development
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

def create_output_folders(output_dir, website_name):
    """Create folder structure for organizing extracted URLs"""
    website_dir = os.path.join(output_dir, website_name)
    os.makedirs(website_dir, exist_ok=True)
    return website_dir

def create_images_folder(images_dir, website_name):
    """Create folder structure for organizing downloaded images"""
    website_images_dir = os.path.join(images_dir, website_name)
    os.makedirs(website_images_dir, exist_ok=True)
    return website_images_dir

def generate_image_filename(url, product_title, index=0):
    """Generate a unique filename for downloaded images"""
    # Parse URL to get original filename and extension
    parsed_url = urlparse(url)
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
        clean_title = re.sub(r'[^\w\s-]', '', product_title.strip())
        clean_title = re.sub(r'\s+', '_', clean_title)
        base_name = clean_title[:50]  # Limit length
    else:
        base_name = name
    
    # Add index if provided
    if index > 0:
        filename = f"{base_name}_{index}{ext}"
    else:
        filename = f"{base_name}{ext}"
    
    return filename

def download_image(url, filepath, max_retries=3, delay=1):
    """Download an image from URL with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            # Use verify=False to bypass SSL certificate issues
            response = requests.get(url, headers=headers, timeout=30, verify=False)
            response.raise_for_status()
            
            # Write the image to file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True, f"Downloaded successfully ({len(response.content)} bytes)"
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"    Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)[:50]}...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                return False, f"Failed after {max_retries} attempts: {str(e)[:50]}..."
    
    return False, "Download failed"

def download_images_for_category(website_name, category, items, images_base_dir="images", max_downloads=5):
    """Download all images for a specific category (limited for testing)"""
    if not items:
        return []
    
    website_images_dir = create_images_folder(images_base_dir, website_name)
    category_dir = os.path.join(website_images_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    
    downloaded_files = []
    failed_downloads = []
    
    # Limit downloads for testing
    items_to_download = items[:max_downloads]
    if len(items) > max_downloads:
        print(f"    Downloading first {max_downloads} of {len(items)} {category} images (limited for testing)...")
    else:
        print(f"    Downloading {len(items_to_download)} {category} images...")
    
    for index, item in enumerate(items_to_download):
        if isinstance(item, dict):
            url = item['url']
            product_title = item.get('product_title', 'Unknown Product')
        else:
            url = item
            product_title = 'Unknown Product'
        
        # Generate unique filename
        filename = generate_image_filename(url, product_title, index)
        filepath = os.path.join(category_dir, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"      Skipping {filename} (already exists)")
            downloaded_files.append(filepath)
            continue
        
        print(f"      Downloading {filename}...")
        success, message = download_image(url, filepath)
        
        if success:
            downloaded_files.append(filepath)
            print(f"        ✓ {message}")
        else:
            failed_downloads.append((url, message))
            print(f"        ✗ {message}")
    
    if failed_downloads:
        print(f"    Failed to download {len(failed_downloads)} images from {category}")
    
    return downloaded_files, failed_downloads

def save_urls_to_files(website_name, categories, output_dir="output"):
    """Save image URLs with product titles to separate files organized by website and category"""
    website_dir = create_output_folders(output_dir, website_name)
    
    saved_files = []
    
    for category, items in categories.items():
        if items:  # Only create files for categories that have URLs
            filename = f"{category}_images.txt"
            filepath = os.path.join(website_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for item in items:
                    if isinstance(item, dict):
                        # New format with product context
                        f.write(f"Product: {item['product_title']}\n")
                        f.write(f"URL: {item['url']}\n")
                        f.write("-" * 50 + "\n")
                    else:
                        # Fallback for old format
                        f.write(item + '\n')
            
            saved_files.append(filepath)
            print(f"  Saved {len(items)} {category} URLs with product info to: {filepath}")
    
    return saved_files

def extract_product_titles(text):
    """Extract potential product titles from text content"""
    # Simplified patterns for product titles
    product_patterns = [
        # Product names with common endings
        r'\b[A-Z][a-zA-Z\s]+(?:T-Shirt|Shirt|Jacket|Hoodie|Dress|Jeans|Shoes|Sneakers|Boots|Bag|Watch|Hat|Sweater|Coat|Pants|Shorts|Top)\b',
        # Brand + product combinations
        r'\b(?:Nike|Adidas|Puma|boohooMAN)\s+[A-Z][a-zA-Z\s]+',
        # Multi-word titles starting with descriptive words
        r'\b(?:Men\'s|Women\'s|Ladies|Oversized|Slim|Fitted|Premium|Classic|Vintage)\s+[A-Z][a-zA-Z\s]+',
        # Simple capitalized phrases (3+ words)
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,}\b',
        # Look for product names near size indicators
        r'[A-Z][a-zA-Z\s]+(?=\s+(?:Size|XS|S|M|L|XL|XXL))'
    ]
    
    titles = set()
    for pattern in product_patterns:
        try:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                title = match.strip()
                # Filter reasonable titles
                if 10 <= len(title) <= 80 and title.count(' ') >= 1:
                    titles.add(title)
        except re.error:
            continue  # Skip problematic patterns
    
    return list(titles)

def find_product_context_for_url(text, url):
    """Find product context around an image URL"""
    # Find the position of the URL in the text
    url_pos = text.find(url)
    if url_pos == -1:
        return None
    
    # Look for product titles in a window around the URL
    window_size = 500  # characters before and after
    start = max(0, url_pos - window_size)
    end = min(len(text), url_pos + len(url) + window_size)
    context = text[start:end]
    
    # Extract potential product titles from the context
    titles = extract_product_titles(context)
    
    # Return the first reasonable title found
    if titles:
        return titles[0]
    
    # Fallback: look for price patterns near the URL (might indicate product)
    price_pattern = r'[£$€]\d+\.?\d*'
    prices = re.findall(price_pattern, context)
    if prices:
        # Look for text between price and URL that might be a product name
        price_pos = context.find(prices[0])
        if price_pos != -1:
            between_text = context[price_pos:context.find(url[url_pos-start:])]
            simple_titles = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', between_text)
            if simple_titles:
                return simple_titles[-1]  # Take the last one (closest to URL)
    
    return None

def extract_image_urls_from_text(text):
    """Extract and categorize image URLs with product context from HTML text content."""
    # Extract all URLs
    url_pattern = re.compile(r'https?://[^\s\"\']+')
    urls = url_pattern.findall(text)
    
    # Filter image URLs (png/jpg/jpeg/webp/gif - here we see png)
    img_exts = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.svg')
    img_urls = [u for u in urls if u.lower().split('?')[0].endswith(img_exts)]
    
    # Dedupe preserving order and extract product context
    seen = set()
    deduped = []
    url_with_context = []
    
    for u in img_urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
            
            # Try to find product context for this URL
            context = find_product_context_for_url(text, u)
            url_with_context.append({
                'url': u,
                'product_title': context or 'Unknown Product'
            })
    
    # Categorize: Nike primary (t_default), PDP sizes (t_PDP_###), others
    categories = {"t_default": [], "t_PDP": [], "other": []}
    for item in url_with_context:
        url = item['url']
        if "/t_default/" in url:
            categories["t_default"].append(item)
        elif "/t_PDP_" in url:
            categories["t_PDP"].append(item)
        else:
            categories["other"].append(item)
    
    return deduped, categories, url_with_context
    """Extract and categorize image URLs from HTML text content."""
    # Extract all URLs
    url_pattern = re.compile(r'https?://[^\s\"\']+')
    urls = url_pattern.findall(text)
    
    # Filter image URLs (png/jpg/jpeg/webp/gif - here we see png)
    img_exts = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.svg')
    img_urls = [u for u in urls if u.lower().split('?')[0].endswith(img_exts)]
    
    # Dedupe preserving order
    seen = set()
    deduped = []
    for u in img_urls:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    
    # Categorize: Nike primary (t_default), PDP sizes (t_PDP_###), others
    categories = {"t_default": [], "t_PDP": [], "other": []}
    for u in deduped:
        if "/t_default/" in u:
            categories["t_default"].append(u)
        elif "/t_PDP_" in u:
            categories["t_PDP"].append(u)
        else:
            categories["other"].append(u)
    
    return deduped, categories

def process_html_file(filepath):
    """Process a single HTML file and extract image URLs."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        deduped, categories, url_with_context = extract_image_urls_from_text(content)
        return deduped, categories, url_with_context
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return [], {"t_default": [], "t_PDP": [], "other": []}, []

def process_html_files(folder_path="html", output_dir="output", download_images=True):
    """Process all text files in the specified folder and save URLs to organized files"""
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found!")
        return
    
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    if not html_files:
        print(f"No text files found in '{folder_path}'")
        return
    
    print(f"Found {len(html_files)} text files: {html_files}")
    print(f"Output directory: {output_dir}")
    if download_images:
        print("Image downloading: ENABLED")
    else:
        print("Image downloading: DISABLED")
    
    all_results = {}
    total_images = 0
    aggregate_categories = {"t_default": set(), "t_PDP": set(), "other": set()}
    all_saved_files = []
    all_downloaded_images = []
    total_download_failures = []
    
    for filename in html_files:
        filepath = os.path.join(folder_path, filename)
        # Extract website name from filename (remove .txt extension)
        website_name = os.path.splitext(filename)[0]
        
        print(f"\nProcessing: {filename}")
        
        deduped_images, categories, url_with_context = process_html_file(filepath)
        
        # Save URLs to files organized by website
        saved_files = []
        downloaded_images = []
        download_failures = []
        
        if deduped_images:
            saved_files = save_urls_to_files(website_name, categories, output_dir)
            all_saved_files.extend(saved_files)
            
            # Download images if enabled
            if download_images:
                print(f"  Starting image downloads for {website_name}...")
                for category, items in categories.items():
                    if items:
                        downloaded, failed = download_images_for_category(website_name, category, items)
                        downloaded_images.extend(downloaded)
                        download_failures.extend(failed)
                
                all_downloaded_images.extend(downloaded_images)
                total_download_failures.extend(download_failures)
                
                print(f"  Downloaded {len(downloaded_images)} images, {len(download_failures)} failed")
        
        all_results[filename] = {
            "images": deduped_images,
            "categories": categories,
            "image_count": len(deduped_images),
            "url_with_context": url_with_context,
            "saved_files": saved_files,
            "downloaded_images": downloaded_images,
            "download_failures": len(download_failures)
        }
        
        total_images += len(deduped_images)
        
        # Add to aggregate categories (using set to avoid duplicates across files)
        for key, items in categories.items():
            if isinstance(items, list) and items:
                if isinstance(items[0], dict):
                    # New format with context
                    aggregate_categories[key].update([item['url'] for item in items])
                else:
                    # Old format (just URLs)
                    aggregate_categories[key].update(items)
    
    # Convert sets back to lists for final result
    aggregate_categories = {k: list(v) for k, v in aggregate_categories.items()}
    
    all_results["_summary"] = {
        "total_files_processed": len(html_files),
        "total_unique_images": total_images,
        "aggregate_categories": aggregate_categories,
        "all_saved_files": all_saved_files,
        "total_downloaded_images": len(all_downloaded_images),
        "total_download_failures": len(total_download_failures),
        "downloaded_images": all_downloaded_images
    }
    
    return all_results

def display_results(results):
    """Display the results in a formatted way."""
    if not results:
        return
    
    summary = results.get("_summary", {})
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Files processed: {summary.get('total_files_processed', 0)}")
    print(f"Total unique images found: {summary.get('total_unique_images', 0)}")
    
    aggregate_cats = summary.get('aggregate_categories', {})
    print(f"t_default images: {len(aggregate_cats.get('t_default', []))}")
    print(f"t_PDP images: {len(aggregate_cats.get('t_PDP', []))}")
    print(f"Other images: {len(aggregate_cats.get('other', []))}")
    
    saved_files = summary.get('all_saved_files', [])
    if saved_files:
        print(f"Total output files created: {len(saved_files)}")
    
    # Show download statistics
    downloaded_count = summary.get('total_downloaded_images', 0)
    failed_count = summary.get('total_download_failures', 0)
    if downloaded_count > 0 or failed_count > 0:
        print(f"Images downloaded: {downloaded_count}")
        if failed_count > 0:
            print(f"Download failures: {failed_count}")
    
    print("\n" + "="*60)
    print("PER-FILE RESULTS")
    print("="*60)
    
    for filename, data in results.items():
        if filename == "_summary":
            continue
        
        print(f"\n{filename}:")
        print(f"  Total images: {data['image_count']}")
        cats = data['categories']
        print(f"  t_default: {len(cats.get('t_default', []))}")
        print(f"  t_PDP: {len(cats.get('t_PDP', []))}")
        print(f"  Other: {len(cats.get('other', []))}")
        
        saved_files = data.get('saved_files', [])
        if saved_files:
            print(f"  URL files created: {len(saved_files)}")
            for file in saved_files:
                print(f"    - {os.path.basename(file)}")
        
        downloaded_images = data.get('downloaded_images', [])
        if downloaded_images:
            print(f"  Images downloaded: {len(downloaded_images)}")
            
        download_failures = data.get('download_failures', 0)
        if download_failures > 0:
            print(f"  Download failures: {download_failures}")
    
    print("\n" + "="*60)
    print("FILES SAVED TO OUTPUT DIRECTORY")
    print("="*60)
    all_saved_files = summary.get('all_saved_files', [])
    if all_saved_files:
        for file in all_saved_files:
            rel_path = os.path.relpath(file)
            print(f"  {rel_path}")
    else:
        print("  No URL files were created (no images found)")
    
    # Show downloaded images summary
    downloaded_images = summary.get('downloaded_images', [])
    if downloaded_images:
        print("\n" + "="*60)
        print("IMAGES DOWNLOADED")
        print("="*60)
        print(f"Total images downloaded: {len(downloaded_images)}")
        
        # Group by website
        by_website = {}
        for img_path in downloaded_images:
            parts = img_path.split(os.sep)
            if 'images' in parts:
                idx = parts.index('images')
                if idx + 1 < len(parts):
                    website = parts[idx + 1]
                    if website not in by_website:
                        by_website[website] = []
                    by_website[website].append(img_path)
        
        for website, images in by_website.items():
            print(f"  {website}: {len(images)} images")
            # Show first few image paths as examples
            for img in images[:3]:
                rel_path = os.path.relpath(img)
                print(f"    - {rel_path}")
            if len(images) > 3:
                print(f"    ... and {len(images) - 3} more")
    
    else:
        print("\n" + "="*60)
        print("No images were downloaded")
        print("="*60)

# Main execution
if __name__ == "__main__":
    # Default to looking in the 'html' folder in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_folder = os.path.join(script_dir, "html")
    
    if os.path.exists(html_folder):
        results = process_html_files(html_folder)
        display_results(results)
    else:
        print(f"HTML folder not found at: {html_folder}")
        print("Please create the 'html' folder and add text files to process.")