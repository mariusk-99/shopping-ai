# 👕 Google Gemini Virtual Try-On System

Transform your e-commerce experience by showing customers how clothing looks on real people!

## 🚀 Quick Start

### 1. Setup API Key
Your API key is already configured in `.env`. If you need to change it:
```bash
# Edit your .env file
nano .env
# Update GOOGLE_GEMINI_API_KEY with your key from https://aistudio.google.com/app/apikey
```

### 2. Add Person Photos
```bash
# Add person photos to the person_photos directory
# See person_photos/README.md for photo guidelines
```

### 3. Run Virtual Try-On
```bash
# Test with one clothing item + one person
python3 test_virtual_tryon.py

# Process multiple combinations
python3 batch_virtual_tryon.py

# Full processing script
python3 gemini_virtual_tryon.py
```

## 📁 File Structure
```
manual/
├── gemini_virtual_tryon.py     # Main virtual try-on client
├── test_virtual_tryon.py       # Simple single test
├── batch_virtual_tryon.py      # Multiple combinations
├── person_photos/              # Person photos for try-on
│   ├── README.md              # Photo guidelines
│   ├── person1.jpg            # Add your person photos here
│   └── model_female.png       
├── images/                     # Your clothing product images
├── virtual_tryons/            # Generated results (auto-created)
└── .env                       # API keys (already configured)
```

## ✨ Features

### 🎯 Smart Product Detection
Automatically detects clothing type from image paths:
- **Shirts**: t-shirt, polo, blouse, top
- **Pants**: trousers, jeans, shorts  
- **Dresses**: dress, gown
- **Outerwear**: jacket, coat, hoodie, blazer
- **Footwear**: shoes, sneakers, boots

### 🧠 AI-Powered Analysis
Each virtual try-on includes:
- **Fit Assessment**: How well the clothing would fit (excellent/good/fair/poor)
- **Style Analysis**: Detailed description of how it looks
- **Recommendations**: Sizing suggestions and styling tips

### 📊 Comprehensive Results
- **JSON Responses**: Detailed API responses saved for analysis
- **Batch Processing**: Handle multiple clothing items with multiple people
- **Error Handling**: Robust error handling and retry logic
- **Rate Limiting**: Configurable delays to respect API limits

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
GOOGLE_GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp
MAX_REQUESTS_PER_MINUTE=10
DEFAULT_STYLE_PREFERENCE=natural and realistic
```

### Product Type Mapping
```python
# Custom product types for specific items
product_types = {
    "images/nike/shirt.png": "athletic shirt",
    "images/formal/dress.jpg": "formal dress"
}
```

## 📝 Usage Examples

### Single Virtual Try-On
```python
from gemini_virtual_tryon import GeminiVirtualTryOnClient

client = GeminiVirtualTryOnClient()
result = client.process_virtual_tryon(
    clothing_image_path="images/nike/shirt.png",
    person_image_path="person_photos/model1.jpg",
    product_type="athletic shirt",
    style_preference="sporty and dynamic"
)
```

### Custom Prompts
```python
custom_prompt = """
Show how this elegant evening dress would look on the person. 
Focus on:
- How the fabric drapes naturally
- The fit around the waist and shoulders  
- Overall elegance and sophistication
- Realistic lighting and shadows
"""

result = client.process_virtual_tryon(
    clothing_image_path="dress.jpg",
    person_image_path="model.jpg",
    custom_prompt=custom_prompt
)
```

### Batch Processing
```python
clothing_items = [
    "images/nike/shirt1.png",
    "images/nike/shirt2.png", 
    "images/temu/pants.jpg"
]

people = [
    "person_photos/person1.jpg",
    "person_photos/person2.jpg"
]

results = client.batch_virtual_tryon(
    clothing_items, 
    people,
    delay_between_requests=2
)
```

## 🎨 Customization

### Style Preferences
- `"natural and realistic"` - Default natural look
- `"sporty and dynamic"` - Athletic/active wear
- `"elegant and sophisticated"` - Formal wear
- `"casual and relaxed"` - Everyday clothing
- `"trendy and fashionable"` - Fashion-forward styles

### Product-Specific Prompts
```python
def create_custom_prompt(product_type):
    prompts = {
        "athletic shirt": "Show dynamic sports movement with this athletic wear",
        "formal dress": "Display elegance and sophistication with perfect draping",
        "casual pants": "Show comfortable, everyday fit with natural movement"
    }
    return prompts.get(product_type, "Show realistic fit and style")
```

## 📊 Response Analysis

### Successful Response Structure
```json
{
  "analysis": "The shirt fits well on the person, highlighting their athletic build...",
  "generated_image_description": "Person wearing the Nike athletic shirt in a natural pose...",
  "fit_assessment": "excellent",
  "recommendations": "This size looks perfect. Consider the matching shorts for a complete outfit."
}
```

### Processing Multiple Results
```python
# Analyze batch results
for result in results:
    if result["result"]["success"]:
        data = result["result"]["data"]
        # Extract and analyze fit assessments
        # Generate recommendations
        # Create comparison reports
```

## 🔍 Troubleshooting

### Common Issues

**"API key not found"**
```bash
# Check your .env file
cat .env
# Verify GOOGLE_GEMINI_API_KEY is set
```

**"No person photos found"**
```bash
# Add photos to person_photos directory
ls person_photos/
# See person_photos/README.md for guidelines
```

**"Unsupported image format"**
```bash
# Convert images to supported formats
convert image.tiff image.jpg
```

**Rate Limiting**
```python
# Increase delay between requests
results = client.batch_virtual_tryon(
    clothing_items, 
    people,
    delay_between_requests=5  # Increase delay
)
```

## 🌟 Best Practices

### For Clothing Images
- Clear product shots on neutral backgrounds
- Multiple angles if available
- High resolution for better analysis
- Good lighting showing fabric details

### For Person Photos  
- Front-facing pose with arms slightly away from body
- Even lighting on face and body
- Simple background
- Person should fill good portion of frame
- Multiple body types for diverse testing

### For API Usage
- Start with single tests before batch processing
- Use appropriate delays between requests
- Save all responses for analysis
- Monitor API usage and costs
- Use descriptive filenames for organization

## 📈 Advanced Features

### Integration with E-commerce
```python
# Integrate with product catalog
def process_product_catalog(products, models):
    for product in products:
        for model in models:
            result = client.process_virtual_tryon(
                product['image_path'],
                model['image_path'], 
                product['category']
            )
            # Save to product database
            save_tryon_result(product['id'], model['id'], result)
```

### A/B Testing
```python
# Test different styles for same product
style_tests = [
    "natural and realistic",
    "trendy and fashionable", 
    "elegant and sophisticated"
]

for style in style_tests:
    result = client.process_virtual_tryon(
        product_image, person_image, 
        style_preference=style
    )
    # Analyze which style performs better
```

This system is ready for production use in e-commerce applications! 🛍️✨