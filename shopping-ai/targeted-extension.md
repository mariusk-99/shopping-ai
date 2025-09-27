# Targeted Shopping Extension

## 🎯 **Extension Now Targets Specific Product Pages**

The extension has been updated to only appear on the exact product pages you specified:

### **Target URLs:**
1. **Nike Product**: [Nike Club Open-Hem Fleece Trousers](https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063)
   - Price: £49.99
   - Premium brand, trusted retailer

2. **Shein Product**: [Franclia Elegant Fitted V-Neck Set](https://www.shein.co.uk/goods-p-158264809.html)
   - Price: £17.54
   - Fast fashion retailer

## 🔧 **Technical Changes Made:**

### **1. URL Matching Configuration**
```typescript
export const config = {
  matches: [
    "https://www.nike.com/*",
    "https://www.shein.co.uk/*"
  ],
  all_frames: false,
  run_at: "document_end"
};
```

### **2. Specific Page Detection**
```typescript
const isTargetProductPage = (url: string): boolean => {
  const targetUrls = [
    "https://www.nike.com/gb/t/club-open-hem-fleece-trousers-k62luLev/FN3730-063",
    "https://www.shein.co.uk/goods-p-158264809.html"
  ];
  
  return targetUrls.some(targetUrl => url.includes(targetUrl));
};
```

### **3. Shopping-Specific Safety Analysis**
- **Nike**: "Safe" - Trusted global brand with secure shopping
- **Shein**: "Caution" - Legitimate retailer but consider sustainability factors

### **4. Updated Content Sections**
- **Shopping Safety**: Brand reputation and security analysis
- **Style Check**: "Will you slay in this?" - Upload image for style analysis
- **Shopping Advice**: Price comparison, quality assessment, style compatibility

## 🚀 **How It Works:**

1. **Extension loads** only on Nike.com and Shein.co.uk domains
2. **Checks specific URLs** to ensure it's the exact product pages
3. **Shows extension** only on the target product pages
4. **Analyzes shopping safety** with brand-specific insights
5. **Provides shopping advice** tailored to fashion decisions

## 📱 **User Experience:**

- **Hidden by default** - Only appears on target pages
- **Shopping-focused** - Content relevant to fashion purchases
- **Brand-aware** - Different analysis for Nike vs Shein
- **Style-oriented** - "Slayy" branding for fashion decisions

## 🎨 **Extension Behavior:**

- **Nike Page**: Shows "Safe" status with premium brand confidence
- **Shein Page**: Shows "Caution" status with sustainability considerations
- **Other Pages**: Extension remains hidden
- **Style Analysis**: Upload image to check if you'll "slay" in the outfit

The extension now provides targeted shopping assistance specifically for these two product pages!
