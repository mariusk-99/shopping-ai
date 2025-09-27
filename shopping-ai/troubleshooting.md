# Extension Not Visible - Troubleshooting Guide

## 🔍 **Debug Steps:**

### **1. Check Browser Console**
1. Open the target website (Nike or Shein)
2. Press F12 to open Developer Tools
3. Go to "Console" tab
4. Look for these messages:
   - `🔥 Slayy Extension - Script loaded!`
   - `🌐 Slayy Extension - Current URL: [url]`
   - `✅ Slayy Extension - Nike or Shein detected, showing extension`

### **2. If No Console Messages:**
- Extension script is not loading
- Check if extension is enabled in Chrome
- Try reloading the extension

### **3. If Script Loads but Extension Not Visible:**
- Check for `👻 Slayy Extension - Not visible, returning null`
- URL detection might be failing

## 🛠 **Quick Fixes:**

### **Fix 1: Extension Not Loading**
```bash
# Stop dev server
Ctrl+C

# Restart clean
pnpm dev
```

### **Fix 2: Reload Extension in Chrome**
1. Go to `chrome://extensions/`
2. Find "Shopping ai" extension
3. Click reload button 🔄
4. Refresh the webpage

### **Fix 3: Check URL Detection**
The extension should now show on ANY Nike or Shein page (temporary change for testing)

## 🎯 **Test URLs:**

### **Nike (Should Work):**
- Any page on nike.com
- Example: https://www.nike.com/gb/

### **Shein (Should Work):**
- Any page on shein.co.uk  
- Example: https://www.shein.co.uk/

## 🔧 **What I Changed:**

1. **More Debug Logs**: Added emoji-coded console logs
2. **Simplified Logic**: Now shows on ANY Nike/Shein page (not just specific products)
3. **Better Error Detection**: Logs at each step

## 📝 **Expected Console Output:**
```
🔥 Slayy Extension - Script loaded!
🌐 Slayy Extension - Current URL: https://www.nike.com/...
🔍 Slayy Extension - URL includes nike.com: true
🔍 Slayy Extension - URL includes shein.co.uk: false
🎯 Slayy Extension - Is target page: [true/false]
✅ Slayy Extension - Nike or Shein detected, showing extension
🎨 Slayy Extension - Render check, isVisible: true
🚀 Slayy Extension - Rendering extension!
```

If you don't see these messages, the extension isn't loading at all.
