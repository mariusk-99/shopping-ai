# Virtual Try-On Photo Guidelines

## 📸 Person Photos for Best Virtual Try-On Results

Place person photos in this directory for virtual try-on processing.

### ✅ Best Practices for Person Photos:

**Pose & Position:**
- 📐 Person should face the camera directly (front-facing)
- 🤲 Arms should be slightly away from body (not pressed against sides)
- 🦵 Standing straight with feet slightly apart
- 👀 Good lighting on face and body

**Image Quality:**
- 📷 High resolution (at least 512x512, preferably 1024x1024 or higher)
- 🌟 Clear, sharp focus (not blurry)
- 💡 Well-lit with even lighting
- 🎯 Person should fill a good portion of the frame

**Background & Clothing:**
- 🏠 Simple, neutral background (white, gray, or plain wall)
- 👔 Person can be wearing simple, fitted clothing
- 🚫 Avoid busy patterns or logos on current clothing
- ✨ Clean, uncluttered scene

**File Formats:**
- ✅ Supported: .jpg, .jpeg, .png, .webp
- 💾 File size: Under 10MB per image
- 📝 Descriptive names: person1.jpg, model_female.png, etc.

### 📋 Example Filenames:
- `person1.jpg` - Generic person photo
- `model_female.png` - Female model
- `model_male.jpg` - Male model  
- `casual_person.webp` - Person in casual pose

### 🎯 Virtual Try-On Process:
1. Add person photos to this directory
2. Run: `python3 test_virtual_tryon.py`
3. The system will combine your clothing products with these person photos
4. Results saved to `virtual_tryons/` directory

### 💡 Tips:
- Multiple person photos allow testing different body types
- Different poses can show how clothing drapes differently
- Consider diversity in your person photos for inclusive results