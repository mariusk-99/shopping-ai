# 🐛 Image URL Troubleshooting Guide

## Common Issues and Solutions

### ❌ "Cannot identify image file" Error

**Problem**: The downloaded file is not a valid image.

**Solutions**:
1. **Use direct image URLs**: Right-click on the product image and select "Copy image address" instead of copying the webpage URL
2. **Check the URL**: Make sure it ends with `.jpg`, `.png`, `.webp`, etc.
3. **Avoid webpage URLs**: Don't use URLs like `https://site.com/product/123` - use the actual image URL

### ❌ "Content-Type" Error  

**Problem**: The URL doesn't point to an image file.

**Solutions**:
1. **Find the actual image**: Many product pages show thumbnails - click on the image to get the full-size version
2. **Inspect the image**: Right-click → "Inspect Element" → look for `<img src="...">` and copy that URL
3. **Try different image sizes**: Some sites have multiple image sizes available

### ❌ Download Failed Error

**Problem**: Unable to download the image from the URL.

**Solutions**:
1. **Check your internet connection**
2. **Try a different image**: Some websites block automated downloads
3. **Use images from supported sites**: Nike, Adidas, Zara, H&M usually work well

## ✅ Best Practices

### How to Get Direct Image URLs:

**Method 1: Right-click (Easiest)**
1. Go to the product page
2. Right-click on the main product image
3. Select "Copy image address" or "Copy image URL"
4. Paste into the webapp

**Method 2: Developer Tools**
1. Right-click on the image → "Inspect Element"
2. Look for `<img src="https://...">` in the HTML
3. Copy the URL from the `src` attribute

**Method 3: Open Image in New Tab**
1. Right-click on image → "Open image in new tab"
2. Copy the URL from the address bar

### Supported Image Formats:
- ✅ `.jpg` / `.jpeg`
- ✅ `.png` 
- ✅ `.webp`
- ✅ `.gif`
- ✅ `.bmp`

### Example Good URLs:
```
✅ https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco/product.png
✅ https://assets.adidas.com/images/h_840,f_auto,q_auto/product.jpg  
✅ https://images.asos-media.com/products/item.webp
```

### Example Bad URLs:
```
❌ https://nike.com/product/air-max-97 (webpage, not image)
❌ https://site.com/thumbnail.jpg?width=50 (too small)
❌ ftp://server.com/image.jpg (not HTTP/HTTPS)
```

## 🧪 Testing URLs

Use the test script to debug problematic URLs:

```bash
python3 test_image_download.py "https://your-image-url-here"
```

## 🌐 Website-Specific Tips

### Nike
- ✅ Look for URLs like `static.nike.com/a/images/...`
- ✅ Usually end in `.png` or `.jpg`

### Adidas  
- ✅ Look for URLs like `assets.adidas.com/images/...`
- ✅ Usually have size parameters like `h_840,f_auto`

### Zara
- ✅ Look for URLs with `static.zara.net`
- ⚠️ Sometimes requires specific headers

### H&M
- ✅ Look for URLs with `www2.hm.com/content/dam`
- ✅ Usually work reliably

### General E-commerce
- ✅ Look for CDN URLs (amazonaws, cloudfront, etc.)
- ✅ Product images are usually high resolution
- ⚠️ Avoid thumbnail or preview images

## 🔧 If Nothing Works

1. **Try a different image**: Some websites are harder to work with
2. **Download and upload**: Save the image to your computer, then upload it as a person photo instead
3. **Use our test images**: We have sample product images in the `images/` folder
4. **Check the console**: Look for detailed error messages in the terminal

## 📞 Getting Help

If you're still having issues:
1. Note the exact error message
2. Share the URL you're trying to use
3. Check if the URL works in your browser first
4. Try the test script to get more detailed debugging info

Remember: The webapp works best with direct image URLs from major retailers! 🛍️